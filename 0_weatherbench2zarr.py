"""
Saving a one year subset (with select data variables) of
[WeatherBench2](https://weatherbench2.readthedocs.io/en/latest/data-guide.html)
to a local Zarr store.

    python 0_weatherbench2zarr.py

Full dataset(s) can be downloaded from
https://console.cloud.google.com/storage/browser/weatherbench2
"""
import os

import xarray as xr

# %%
# Temporal subset of WeatherBench2 dataset to 2 years
store_name: str = "2020-full_37-6h-0p25deg-chunk-1_zuv500.zarr"
if not os.path.exists(path=store_name):
    # Open WeatherBench2 Zarr store from Google Cloud Storage
    ds: xr.Dataset = xr.open_dataset(
        filename_or_obj="gs://weatherbench2/datasets/era5/1959-2022-full_37-6h-0p25deg-chunk-1.zarr-v2",
        engine="zarr",
        chunks="auto",
        consolidated=True,
    )

    # Subset to year 2000, 500hPa pressure level
    ds_500hpa = ds.sel(time=slice("2000-01-01", "2000-12-31"), level=500, drop=True)

    # Get data variable z500, u500, v500
    ds_500hpa_zuv = ds_500hpa.get(
        key=["geopotential", "u_component_of_wind", "v_component_of_wind"]
    )

    # Disable LZ4 compression, since cupy-xarray cannot handle it yet
    for var in ds_500hpa_zuv.variables:
        ds_500hpa_zuv[var].encoding["compressor"] = None

    # Save to Zarr with chunks of size 1 along time dimension
    # Can take about 1 hour to save 10.7GB of data at 40MB/s
    ds_rechunked: xr.Dataset = ds_500hpa_zuv.chunk(
        time=1,
        latitude=len(ds_500hpa_zuv.latitude),
        longitude=len(ds_500hpa_zuv.longitude),
    )
    ds_rechunked.to_zarr(store=store_name, consolidated=True, zarr_version=2)

# Read back Zarr store using kvikIO engine to
# ensure things were saved correctly and can be loaded into GPU directly
ds_zarr: xr.Dataset = xr.open_dataset(
    filename_or_obj=store_name, engine="kvikio", consolidated=False
)
print(ds_zarr)
print(ds_zarr.u_component_of_wind)
print(f"Loaded as {ds_zarr.u_component_of_wind.isel(time=0).data.__class__}")
