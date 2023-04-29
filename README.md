[pypi-version-image]: https://badge.fury.io/py/ampy.svg?
[pypi-version-url]: https://badge.fury.io/py/ampy

[docs-image]: https://readthedocs.org/projects/ampy/badge/?version=latest
[docs-url]: https://ampy.readthedocs.io/en/latest

[linting-image]: https://github.com/swarmtronics/AMPy/actions/workflows/pylint.yml/badge.svg
[linting-url]: https://github.com/swarmtronics/AMPy/actions/workflows/pylint.yml

[coverage-image]: https://coveralls.io/repos/github/swarmtronics/AMPy/badge.svg?service=github&kill_cache=0
[coverage-url]: https://coveralls.io/github/swarmtronics/AMPy

[pypi-license-image]: https://img.shields.io/pypi/l/ampy

![Pipeline_image](materials/logo_header_bl_font.png#gh-light-mode-only)
![Pipeline_image](materials/logo_header_wh_font.png#gh-dark-mode-only)


[![Python](https://img.shields.io/badge/python-3.8%20--%203.11-blue)](https://www.python.org)
[![PyPI version][pypi-version-image]][pypi-version-url]
[![Docs Status][docs-image]][docs-url]
[![Coverage Status][coverage-image]][coverage-url]
[![Linting Status][linting-image]][linting-url]
![PyPI - License][pypi-license-image]

**[Website](swarmtronics.com)** (TBD) | **[Documentation](https://ampy.readthedocs.io/en/latest/)** | **[Paper](TBD)** (TBD) | **[Video Tutorial](TBD)** (TBD) | **[Colab Notebook](https://colab.research.google.com/drive/1hiCGXoDtOEO3LOm6RG12111Kiwofh069?usp=sharing)**

**AMPy** is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems. Our library turns the processing of experiment recordings into a cakewalk, considerably accelerating extraction of system dynamics.

## Overview

The library is comprised of three components: `processing.py`, `statistic2d.py`, and `statistic3d.py`. 

- `processing.py` handles the initial processing of experimental video recordings and tracks the ArUco markers placed on the robots' upper surfaces. 

- `statistic2d.py` deals with the analysis of robot positions and orientations in each frame, calculating various two-dimensional statistical measures (e.g., Cartesian displacement, order parameter). 

- `statistic3d.py` evaluates position, orientation, and velocity correlation maps for the entire platform.

If you want a brief introduction into library capabilities, we prepared [a Colab tutorial](https://colab.research.google.com/drive/1hiCGXoDtOEO3LOm6RG12111Kiwofh069?usp=sharing) for that occasion.

## Installation

AMPy is available at [the Python Package Index](https://pypi.org/project/ampy/):

```
$ pip install ampy
```

# Contact us

If you have some questions about the code, you are welcome to open an issue, we will respond to that as soon as possible. Contributions towards extension of AMPy functionality are more than welcome!

# License

Established code released as open-source software under the GPLv3 license.

# Citation

To be updated.

```
@misc{
      dmitriev2023swarmobot,
      title={Swarmobot 1.0: A Modular Bristle-Bot Platform for Robotic Active Matter}, 
      author={Alexey A. Dmitriev and Alina D. Rozenblit and Vadim A. Porvatov and
              Mikhail K. Buzakov and Anastasia A. Molodtsova and Daria V. Sennikova and
              Vyacheslav A. Smirnov and Oleg I. Burmistrov and Ekaterina M. Puhtina and
              Nikita A. Olekhno},
      year={2023},
      eprint={TBD},
      archivePrefix={arXiv},
      primaryClass={TBD}
}
```
