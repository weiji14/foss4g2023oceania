# [FOSS4G SotM Oceania 2023 presentation](https://talks.osgeo.org/foss4g-sotm-oceania-2023/talk/YP3KPT)

The ecosystem of geospatial machine learning tools in the
[Pangeo](https://pangeo.io) world.

**Presenter**: [Wei Ji Leong](https://github.com/weiji14)

**When**: [Wednesday, 18 October 2023, 13:50–14:15 (NZDT)](https://2023.foss4g-oceania.org/#/program)

**Where**: [Te Iringa (Wave Room - WG308), Auckland University of Technology (AUT)](https://2023.foss4g-oceania.org/#/attend/our-conference-venue), Auckland, New Zealand

**Website**: https://2019.foss4g-oceania.org/schedule/2019-11-12?sessionId=SPGUQV

## Abstract

Several open source tools are enabling the shift to cloud-native geospatial
Machine Learning workflows. Stream data from STAC APIs, generate Machine
Learning ready chips on-the-fly and train models for different downstream
tasks! Find out about advances in the Pangeo ML community towards scalable
GPU-native workflows.

### Long description

An overview of open source Python packages in the Pangeo (big data geoscience)
Machine Learning community will be presented. On read/write,
[kvikIO](https://github.com/rapidsai/kvikio) allows low-latency data transfers
from Zarr archives via NVIDIA GPU Direct Storage. With tensors loaded in xarray
data structures, [xbatcher](https://github.com/xarray-contrib/xbatcher) enables
efficient slicing of arrays in an iterative fashion. To connect the pieces,
[zen3geo](https://github.com/weiji14/zen3geo) acts as the glue between
geospatial libraries - from reading [STAC](https://stacspec.org) items and
rasterizing vector geometries to stacking multi-resolution datasets for custom
data pipelines. Learn more as the Pangeo community develops tutorials at
[Project Pythia](https://cookbooks.projectpythia.org), and join in to hear
about the challenges and ideas on scaling machine learning in the geosciences
with the [Pangeo ML Working Group](https://pangeo.io/meeting-notes.html#working-group-meetings).


# Getting started

## Installation

### NVIDIA GPU Direct Storage

Follow instructions at
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#install-gpudirect-storage
to install NVIDIA GPU Direct Storage (GDS).

Verify that NVIDIA GDS has been installed properly following
https://docs.nvidia.com/gpudirect-storage/troubleshooting-guide/index.html#verify-suc-install.
E.g. if you are on Linux and have CUDA 12.2 installed, run:

    /usr/local/cuda-12.2/gds/tools/gdscheck.py -p

Alternatively, if you have your conda environment setup below, follow
https://xarray.dev/blog/xarray-kvikio#appendix-ii--making-sure-gds-is-working
and run:

    mamba activate foss4g2023oceania
    curl -s https://raw.githubusercontent.com/rapidsai/kvikio/branch-23.08/python/benchmarks/single-node-io.py | python

### Basic

To help out with development, start by cloning this [repo-url](/../../)

    git clone <repo-url>

Then I recommend [using mamba](https://mamba.readthedocs.io/en/latest/installation.html)
to install the dependencies.
A virtual environment will also be created with Python and
[JupyterLab](https://github.com/jupyterlab/jupyterlab) installed.

    cd foss4g2023oceania
    mamba env create --file environment.yml

Activate the virtual environment first.

    mamba activate foss4g2023oceania

Finally, double-check that the libraries have been installed.

    mamba list

### Advanced

This is for those who want full reproducibility of the virtual environment.
Create a virtual environment with just Python and conda-lock installed first.

    mamba create --name foss4g2023oceania python=3.10 conda-lock=2.3.0
    mamba activate foss4g2023oceania

Generate a unified [`conda-lock.yml`](https://github.com/conda/conda-lock) file
based on the dependency specification in `environment.yml`. Use only when
creating a new `conda-lock.yml` file or refreshing an existing one.

    conda-lock lock --mamba --file environment.yml --platform linux-64 --with-cuda=11.8

Installing/Updating a virtual environment from a lockile. Use this to sync your
dependencies to the exact versions in the `conda-lock.yml` file.

    conda-lock install --mamba --name foss4g2023oceania conda-lock.yml

See also https://conda.github.io/conda-lock/output/#unified-lockfile for more
usage details.


# References

## Links

- https://xarray.dev/blog/xarray-kvikio

## License

All code in this repository is licensed under
GNU Lesser General Public License 3.0
[(LGPL-3.0)](https://www.gnu.org/licenses/lgpl-3.0.en.html).
All other non-code content is licensed under
Creative Commons Attribution-ShareAlike 4.0 International
[(CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0).
