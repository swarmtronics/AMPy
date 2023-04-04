<p align="center">
  <img height="150" src="https://raw.githubusercontent.com/dobrychever/ST_lib/master/materials/image.jpg?token=GHSAT0AAAAAACBADUDASDFWM7LQXI2MHDCEZBMOFGQ" />
</p>

# AMARETTO

**AMARETTO** (*Active MAtter Researc Emulation & Tracking TOolkit*) is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems.
Библиотека превращает обработку видеозаписей экспериментов из тяжкого труда в лёгкую прогулку и многократно ускоряет процесс написания кода с целью извлечения из видео полезных характеристик.

# Library content
## Overview
The library is comprised of three components: `processing.py`, `statistic2d.py`, and `statistic3d.py`. 

The `processing.py` module handles the processing of experimental video recordings and identifies ArUco markers placed on the robots' upper surfaces. 

The `statistic2d.py` module deals with the analysis of robot positions and orientations in each frame, calculating various two-dimensional statistical measures such as Cartesian displacement, order parameter, and spatial-temporal correlation parameter. 

Lastly, the `statistic3d.py` module is dedicated to generating correlation maps for position, orientation, and velocity.

## processing.py
This module implements a simple interface for using the *OpenCV* library to explore robotic systems.
Working with the functionality of the module is carried out through the class `Processor`:

```python
from amtoolkit.processing import Processor


VP = Processor()
```

Сперва для обработки видеофрагмента необходимо передать в обработчик путь к видеофайлу. Это делается с помощью метода `set_filename`:

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
```

Далее производится извлечение декартовой кинематики (каждому маркеру в видео покадрово сопостовляется его угол поворота и положение в кадре) с помощью метода `cartesian_kinematics`. 

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
```

Данный метод возвращает список, в котором каждому кадру сопоставлен список из данных о роботах в этом кадре. Данные о каждом роботе состоят из ID его маркера, угла поворота и положения в кадре. В примере видеозапись содержит в себе 45 роботов, обработка ведётся с 120 по 6000 кадр записи, при этом для обработки выбирается каждый пятый кадр. При этом при распознавании коды маркеров с ID 12 и 14 игнорируются. Значения `scale_parameters` отвечают параметрам $\alpha$ и $\beta$ линейного преобразования значений пикселей для изменения яркости и контрастности изображения. Подбор правильных `scale_parameters` является исследовательской задачей и сильно зависит от условий освещения, в которых делалась видеозапись

Для расчёта некоторых статистических величин необходимо кроме декартового представления кинематики системы иметь так же её полярное представление. Для этого нужно воспользоваться методом `polar_kinematics`, который дополнит данные о каждом роботе полярным углом и расстоянием от центра поля (`field_center`):

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
```

Вся кинематика системы записывается в пикселях. Если для каких-то вычислений необходимо перевести расстояния из пикселей в сантиметры, метод `metric_constant`:

```python
from amtoolkit.processing import Processor


VP = Processor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
metric_constant = VP.metric_constant(marker_size=3, scale_parameters=(0.8, -30))
```

## statistics2d.py

Этот модуль реализует вычисления двумерных статистических величин на предварительно извлечённой из видео кинематике.

- Среднее удаление роботов от центра поля. Реализуется функцией `mean_distances_from_center`.

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

- Средний полярный угол роботов. Реализуется функцией `mean_polar_angle`.

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

- Средний полярный угол роботов в смысле углового пути системы. Реализуется функцией `mean_polar_angle_absolute`.

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

- Среднеквадратичное удаление от начального положения. Реализуется функцией `mean_cartesian_displacements`.

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import mean_cartesian_displacements


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
cartesian_displacement = mean_cartesian_displacements(kinematics=cartesian_kinematics)
```

- Bond-orientational order parameter $\psi_N$. Реализуется функцией `bond_orientation`. 

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import bond_orientation


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
boo = bond_orientation(kinematics=cartesian_kinematics, neighbours_number=6, folds_number=6)
```

- Spatio-temporal correlation parameter $\chi_4$. Реализуется функцией `chi_4`.

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import chi_4


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
t_corr = chi_4(kinematics=cartesian_kinematics, tau=60, a=100)
```

- Collision graph average clustering coefficient. Реализуется функцией `cluster_dynamics`. Also you can specify detection of collision between robots by changing `collide_function` argument of `cluster_dynamics`

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics2d import cluster_dynamics


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
clustering_coefficient = cluster_dynamics(kinematics=cartesian_kinematics)
```



## statistics3d.py

Этот модуль реализует вычисления трёхмерных статистических величин на предварительно извлечённой из видео кинематике.

- Two-dimensional pair correlation. Реализуется функцией `position_correlation`.

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics3d import position_correlation


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
pos_corr = position_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Orientation correlation function. Реализуется функцией `mean_polar_angle`.

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics3d import orientation_correlation


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
orient_corr = orientation_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Velocity correlation function. Реализуется функцией `mean_polar_angle_absolute`.

```python
from amtoolkit.processing import Processor
from amtoolkit.statistics3d import get_velocity_correlation


VP = Processor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
vel_corr = velocity_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

