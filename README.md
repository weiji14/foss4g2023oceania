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

## License

All code in this repository is licensed under
GNU Lesser General Public License 3.0
[(LGPL-3.0)](https://www.gnu.org/licenses/lgpl-3.0.en.html).
All other non-code content is licensed under
Creative Commons Attribution-ShareAlike 4.0 International
[(CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0).
