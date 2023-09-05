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

**[Website](https://swarmtronics.com)** | **[Documentation](https://ampy.readthedocs.io/en/latest/)** | **[Paper](https://arxiv.org/abs/2305.13510)** | **[Video Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)** (TBD) | **[Colab Notebook](https://colab.research.google.com/drive/1hiCGXoDtOEO3LOm6RG12111Kiwofh069?usp=sharing)**

**AMPy** is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems. Our library turns the processing of experiment recordings into a cakewalk, considerably accelerating extraction of system dynamics.

## Overview

The library is comprised of 4 components: `processing.py`, `statistic2d.py`, `statistic3d.py`, and `animation.py`. 

- `processing.py` handles the initial processing of experimental video recordings and tracks the ArUco markers placed on the robots' upper surfaces. 

- `statistics2d.py` extracts various two-dimensional statistical measures from obtained kinematics (such as Cartesian displacement or order parameters). 

- `statistics3d.py` evaluates position, orientation, and velocity correlation maps for the entire platform.
 
- `animation.py` generates .gif with the simultaneous evolution of parameters from `statistics2d.py` along with the input video.
  
If you want a brief introduction into library capabilities, we prepared [a Colab tutorial](https://colab.research.google.com/drive/1hiCGXoDtOEO3LOm6RG12111Kiwofh069?usp=sharing) for that occasion.

## Installation

AMPy is available at [the Python Package Index](https://pypi.org/project/ampy/):

```
$ pip install ampy
```

## Preparing markers

For users' convenience, we provide [the .ipynb notebook](https://github.com/swarmtronics/AMPy/tree/master/marker_generator) allowing to generate ArUco- and AprilTag-based markers for tracking of their own robots.

## Contact us

If you have some questions about the code, you are welcome to open an issue, we will respond to that as soon as possible. Contributions towards extension of AMPy functionality are more than welcome!

## License

Established code released as open-source software under the GPLv3 license.

## Citation

```
@misc{
      dmitriev2023swarmobot,
      title={Swarmodroid 1.0: A Modular Bristle-Bot Platform for Robotic Active Matter}, 
      author={Alexey A. Dmitriev and Alina D. Rozenblit and Vadim A. Porvatov and
              Mikhail K. Buzakov and Anastasia A. Molodtsova and Daria V. Sennikova and
              Vyacheslav A. Smirnov and Oleg I. Burmistrov and Ekaterina M. Puhtina and
              Nikita A. Olekhno},
      year={2023},
      eprint={2305.13510},
      archivePrefix={arXiv},
      primaryClass={cond-mat.soft}
}
```
