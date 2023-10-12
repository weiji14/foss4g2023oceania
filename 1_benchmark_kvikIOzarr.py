"""
Experiments on WeatherBench2, loading with kvikIO or Zarr engine.

    python 1_benchmark_kvikIOzarr.py

References:
- https://weatherbench2.readthedocs.io/en/latest/index.html
"""
import time

import cupy
import lightning as L
import numpy as np
import torch
import torchdata
import torchdata.dataloader2
import xarray as xr
import zen3geo
from tqdm.auto import tqdm, trange


# %%
def sel_datavars(
    dataset: xr.Dataset,
    data_vars: list = ["geopotential", "u_component_of_wind", "v_component_of_wind"],
) -> xr.Dataset:
    """
    Select specific data variables from an xarray.Dataset object.
    """
    return dataset.get(key=data_vars)  # .sel(level=500)


def xarray_to_tensor_collate_fn(
    samples: torchdata.datapipes.DataChunk,
) -> (torch.Tensor, torch.Tensor, list[dict]):
    """
    Converts individual xarray.Dataset objects to torch.Tensor (float32 dtype),
    and stack them all into a single torch.Tensor. Also outputs a metadata list
    of dictionaries that contains the timestamp of the xarray.Dataset's data
    variable.
    """
    tensor_t0: torch.Tensor = torch.stack(
        tensors=[
            torch.as_tensor(data=sample.isel(time=0).to_array().data, device="cuda")
            for sample in samples
        ]
    )
    tensor_t1: torch.Tensor = torch.stack(
        tensors=[
            torch.as_tensor(data=sample.isel(time=1).to_array().data, device="cuda")
            for sample in samples
        ]
    )
    metadata: list[dict] = [
        {
            "unixtime0": torch.as_tensor(
                data=sample.time.isel(time=0).astype(dtype="int64").data, device="cuda"
            ),
            "unixtime1": torch.as_tensor(
                data=sample.time.isel(time=1).astype(dtype="int64").data, device="cuda"
            ),
        }
        for sample in samples
    ]

    return tensor_t0, tensor_t1, metadata


# %%
class WeatherBench2DataModule(L.LightningDataModule):
    """
    LightningDataModule to load WeatherBench2 data from Zarr.
    """

    def __init__(
        self,
        zarr_store: str = "2020-full_37-6h-0p25deg-chunk-1_zuv500.zarr",
        # zarr_store: str = "gs://weatherbench2/datasets/era5/1959-2022-full_37-6h-0p25deg-chunk-1.zarr-v2",
        engine: str = "kvikio",
        batch_size: int = 32,
    ):
        """
        Go from a Zarr datacube to 6-hourly time-slice chips!

        Also does mini-batching.

        Parameters
        ----------
        zarr_stores : str
            A path or URL to a Zarr stores to read from. E.g. ``store1.zarr``.
            See list of available WeatherBench2 Zarr stores at
            https://weatherbench2.readthedocs.io/en/latest/data-guide.html

        engine : str
            The engine to use in `xr.open_dataset`. E.g. ``kvikio``, ``zarr``.
            Default is ``kvikio``.

        batch_size : int
            Size of each mini-batch. Default is 32.

        Returns
        -------
        datapipe : torchdata.datapipes.iter.IterDataPipe
            A torch DataPipe that can be passed into a torch DataLoader.
        """
        super().__init__()
        self.zarr_store: str = zarr_store
        self.engine: str = engine
        self.batch_size: int = batch_size

        print(f"Loading data using {self.engine} engine")

    def setup(self, stage: str | None = None) -> torchdata.datapipes.iter.IterDataPipe:
        """
        Data operations to perform on every GPU.
        Split data into training and test sets, etc.

        Returns
        -------
        datapipes : IterDataPipe
            The torch DataPipe object to iterate over the training set.
        """
        # Step 0 - Iterate through all the Zarr stores
        dp_source: torchdata.datapipes.iter.IterDataPipe = (
            torchdata.datapipes.iter.IterableWrapper(iterable=[self.zarr_store])
        )

        # Step 1 - Create WeatherBench2 xarray.Dataset chips (full metadata)
        dp_weather_chips: torchdata.datapipes.iter.IterDataPipe = (
            # Step 1.0 - Open each Zarr store using xarray
            dp_source.read_from_xpystac(
                engine=self.engine, chunks=None, consolidated=False
            )
            # Step 1.1 - Select desired data variables at 500hPa
            .map(fn=sel_datavars)
            # Step 1.2 - Slice datacube along time-dimension into 12 hour chunks (2x 6-hourly)
            .slice_with_xbatcher(
                input_dims={"latitude": 721, "longitude": 1440, "time": 2},
                preload_batch=False,
            )
        )

        # Step 2 - Train/validation split each chip based on geography
        # TODO

        # Step 3 - Batch and split ERA5 chips into Machine Learning format
        self.datapipe_train = (
            # Step 3.1 - Create mini-batches (default is 32)
            dp_weather_chips.batch(batch_size=self.batch_size)
            # Step 3.2 - Convert xarray.Dataset to torch.Tensor and stack
            .collate(collate_fn=xarray_to_tensor_collate_fn)
        )

    def train_dataloader(self) -> torchdata.dataloader2.DataLoader2:
        """
        Loads the data used in the training loop.
        """
        return torchdata.dataloader2.DataLoader2(datapipe=self.datapipe_train)


# %%
if __name__ == "__main__":
    # Optimize torch performance
    torch.set_float32_matmul_precision(precision="medium")

    # Setup data
    datamodule: L.LightningDataModule = WeatherBench2DataModule(engine="kvikio")
    datamodule.setup()
    train_dataloader = datamodule.train_dataloader()

    # Training loop
    num_epochs: int = 10
    epoch_timings: list = []
    for epoch in trange(num_epochs):
        # Start timing
        tic: float = time.perf_counter()

        # Mini-batch processing
        for i, batch in tqdm(iterable=enumerate(train_dataloader), total=23):
            input, target, metadata = batch
            # Compute Mean Squared Error loss between t=0 and t=1, just for fun
            loss: torch.Tensor = torch.functional.F.mse_loss(input=input, target=target)
            # print(f"Batch {i}, MSE Loss: {loss}")

        # Stop timing
        toc: float = time.perf_counter()
        epoch_timings.append(toc - tic)

    total_time: float = np.sum(a=epoch_timings)
    median_time: float = np.median(a=epoch_timings)
    mean_time: float = np.mean(a=epoch_timings)
    std_time: float = np.std(a=epoch_timings)
    print(
        f"Total: {total_time:0.4f} seconds, "
        f"Median: {median_time:0.4f} seconds/epoch, "
        f"Mean: {mean_time:0.4f} ± {std_time:0.4f} seconds/epoch"
    )
