![Pipeline_image](materials/amaretto_logo_header_wh.png#gh-light-mode-only)
![Pipeline_image](materials/amaretto_logo_header_bl.png#gh-dark-mode-only)

**AMARETTO** (*Active MAtter Researc Emulation & Tracking TOolkit*) is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems.
The library turns the processing of video recordings of experiments from hard work into an cakewalk and greatly speeds up the process of writing code in order to extract useful characteristics from videos.

# Library content
## Overview
The library is comprised of three components: `processing.py`, `statistic2d.py`, and `statistic3d.py`. 

The `processing.py` module handles the processing of experimental video recordings and identifies ArUco markers placed on the robots' upper surfaces. 

The `statistic2d.py` module deals with the analysis of robot positions and orientations in each frame, calculating various two-dimensional statistical measures such as Cartesian displacement, order parameter, and spatial-temporal correlation parameter. 

Lastly, the `statistic3d.py` module is dedicated to generating position, orientation, and velocity correlation maps for the entire platform.

## processing.py
This module implements a simple interface for using the *OpenCV* library to explore robotic systems.
Working with the functionality of the module is carried out through the class `Processor`:

```python
from amtoolkit.processing import Processor


VP = Processor()
```

Firstly, to process a video fragment, you must pass the path to the video file. Use the `set_filename` method for this:

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
```

Next, extract the Cartesian kinematics (each marker in the video is frame-by-frame associated with its rotation angle and position in the frame) using the `cartesian_kinematics` method.

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
```

This method returns a list in which each frame is associated with a list of data about robots in this frame. The data for each robot consists of its marker ID, rotation angle, and position in the frame. In the example, the video recording contains 45 robots, processing is carried out from the 120th to the 6000th frame of the recording, and every fifth frame is selected for processing. At the same time marker codes with ID 12 and 14 are ignored. The `scale_parameters` values correspond to the $\alpha$ and $\beta$ parameters of the linear transformation of pixel values to change the brightness and contrast of the image. Finding the right `scale_parameters` is an exploratory task and is highly dependent on the lighting conditions in which the video was recorded.

To calculate some statistical functions, in addition to the Cartesian representation of the kinematics of the system, it is also necessary to have its polar representation. To do this, use the `polar_kinematics` method, which will complement the data about each robot with a polar angle and distance from the field center (`field_center`):

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
```

All kinematics of the system is stored in pixels. In some cases it is necessary to convert distances from pixels to centimeters, using the `metric_constant` method:

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
metric_constant = VP.metric_constant(marker_size=3, scale_parameters=(0.8, -30))
```

## statistics2d.py

This module allows to extrat two-dimensional characteristics of the previously obtained kinematics. 

- Mean dispacement of robots from the center of the field can be calculated via the `mean_distances_from_center` function:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import mean_distance_from_center


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
distance = mean_distance_from_center(kinematics=polar_kinematics)
```

- Common mean polar angle:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import mean_polar_angle


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
polar_angle = mean_polar_angle(kinematics=polar_kinematics)
```

- Mean polar angle in sense of the angular path of a system:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import mean_polar_angle_absolute


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
polar_angle_absolute = mean_polar_angle_absolute(kinematics=polar_kinematics)
```

- Mean squared distance from the initial position:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import mean_cartesian_displacements


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
cartesian_displacement = mean_cartesian_displacements(kinematics=cartesian_kinematics)
```

- Bond-orientational order parameter $\psi_N$:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import bond_orientation


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
boo = bond_orientation(kinematics=cartesian_kinematics, neighbours_number=6, folds_number=6)
```

- Spatio-temporal correlation parameter $\chi_4$:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import chi_4


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
t_corr = chi_4(kinematics=cartesian_kinematics, tau=60, a=100)
```

- Average clustering coefficient of a collision graph:

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import cluster_dynamics


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
clustering_coefficient = cluster_dynamics(kinematics=cartesian_kinematics)
```
Also you can specify detection of collision between robots by changing `collide_function` argument of `cluster_dynamics`.


## three_dimensional_statistics.py

This module allows to extract three-dimensional statistical characteristics of obtained kinematics:

- Positional pair correlation is realized by `get_position_correlation`:

```python
from amtoolkit.three_dimensional_statistics import get_position_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
position_correlation = get_position_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Orientation correlation function can be computed via `get_mean_polar_angle`:

```python
from amtoolkit.three_dimensional_statistics import get_orientation_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
orientation_correlation = get_orientation_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Velocity correlation can be computed as fit is based on the `get_velocity_correlation` function:

```python
from amtoolkit.three_dimensional_statistics import get_velocity_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
velocity_correlation = get_velocity_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```
