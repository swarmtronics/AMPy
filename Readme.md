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

## video_processor.py
Этот модуль реализует простой интерфейс для использования библиотеки *OpenCV* для изучения роботизированных систем.
Работа с функционалом модуля осуществляется посредством класса `VideoProcessor`:

```python
from amtoolkit.video_processor import VideoProcessor


VP = VideoProcessor()
```

Сперва для обработки видеофрагмента необходимо передать в обработчик путь к видеофайлу. Это делается с помощью метода `set_filename`:

```python
from amtoolkit.video_processor import VideoProcessor


VP = VideoProcessor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
```

Далее производится извлечение декартовой кинематики (каждому маркеру в видео покадрово сопостовляется его угол поворота и положение в кадре) с помощью метода `extract_cartesian_kinematics`. 

```python
from amtoolkit.video_processor import VideoProcessor


VP = VideoProcessor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
```

Данный метод возвращает список, в котором каждому кадру сопоставлен список из данных о роботах в этом кадре. Данные о каждом роботе состоят из ID его маркера, угла поворота и положения в кадре. В примере видеозапись содержит в себе 45 роботов, обработка ведётся с 120 по 6000 кадр записи, при этом для обработки выбирается каждый пятый кадр. При этом при распознавании коды маркеров с ID 12 и 14 игнорируются. Значения `scale_parameters` отвечают параметрам $\alpha$ и $\beta$ линейного преобразования значений пикселей для изменения яркости и контрастности изображения. Подбор правильных `scale_parameters` является исследовательской задачей и сильно зависит от условий освещения, в которых делалась видеозапись

Для расчёта некоторых статистических величин необходимо кроме декартового представления кинематики системы иметь так же её полярное представление. Для этого нужно воспользоваться методом `extend_kinematics`, который дополнит данные о каждом роботе полярным углом и расстоянием от центра поля (`field_center`):

```python
from amtoolkit.video_processor import VideoProcessor


VP = VideoProcessor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                              get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
```

Вся кинематика системы записывается в пикселях. Если для каких-то вычислений необходимо перевести расстояния из пикселей в сантиметры, метод `get_metric_constant`:

```python
from amtoolkit.video_processor import VideoProcessor


VP = VideoProcessor()
filename = 'C:/examplefolder/examplefilename.mp4'
VP.set_filename(filename)
metric_constant = VP.get_metric_constant(marker_size=3, scale_parameters=(0.8, -30))
```

## two_dimensional_statistics.py

Этот модуль реализует вычисления двумерных статистических величин на предварительно извлечённой из видео кинематике.

- Среднее удаление роботов от центра поля. Реализуется функцией `get_mean_distances_from_center`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_distance_from_center


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
mean_distance_from_center = get_mean_distance_from_center(kinematics=extended_kinematics)
```

- Средний полярный угол роботов. Реализуется функцией `get_mean_polar_angle`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_polar_angle


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
mean_polar_angle = get_mean_polar_angle(kinematics=extended_kinematics)
```

- Средний полярный угол роботов в смысле углового пути системы. Реализуется функцией `get_mean_polar_angle_absolute`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_polar_angle_absolute


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
mean_polar_angle_absolute = get_mean_polar_angle_absolute(kinematics=extended_kinematics)
```

- Среднеквадратичное удаление от начального положения. Реализуется функцией `get_mean_cartesian_displacements`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_cartesian_displacements


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
mean_cartesian_displacements = get_mean_cartesian_displacements(kinematics=cartesian_kinematics)
```

- Bond-orientational order parameter $\psi_N$. Реализуется функцией `get_bond_orientation`. 

```python
from amtoolkit.two_dimensional_statistics import get_bond_orientation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
boo = get_bond_orientation(kinematics=cartesian_kinematics, neighbours_number=6, folds_number=6)
```

- Spatio-temporal correlation parameter $\chi_4$. Реализуется функцией `get_chi_4`.

```python
from amtoolkit.two_dimensional_statistics import get_chi_4


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
chi_4 = get_chi_4(kinematics=cartesian_kinematics, tau=60, a=100)
```

- Collision graph average clustering coefficient. Реализуется функцией `get_cluster_dynamics`. Also you can specify detection of collision between robots by changing `collide_function` argument of `get_cluster_dynamics`

```python
from amtoolkit.two_dimensional_statistics import get_cluster_dynamics


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
clustering_coefficient = get_cluster_dynamics(kinematics=cartesian_kinematics)
```



## three_dimensional_statistics.py

Этот модуль реализует вычисления трёхмерных статистических величин на предварительно извлечённой из видео кинематике.

- Two-dimensional pair correlation. Реализуется функцией `get_position_correlation`.

```python
from amtoolkit.three_dimensional_statistics import get_position_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
position_correlation = get_position_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Orientation correlation function. Реализуется функцией `get_mean_polar_angle`.

```python
from amtoolkit.three_dimensional_statistics import get_orientation_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
orientation_correlation = get_orientation_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

- Velocity correlation function. Реализуется функцией `get_mean_polar_angle_absolute`.

```python
from amtoolkit.three_dimensional_statistics import get_velocity_correlation


VP = VideoProcessor()
VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
velocity_correlation = get_velocity_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
```

