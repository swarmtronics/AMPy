<p align="center">
  <img height="150" src="https://raw.githubusercontent.com/dobrychever/ST_lib/master/materials/image.jpg?token=GHSAT0AAAAAACBADUDASDFWM7LQXI2MHDCEZBMOFGQ" />
</p>

# AMARETTO

**AMARETTO** (*Active MAtter Researc Emulation & Tracking TOolkit*) is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems.
Библиотека превращает обработку видеозаписей экспериментов из тяжкого труда в лёгкую прогулку и многократно ускоряет процесс написания кода с целью извлечения из видео полезных характеристик.

# Library content
## Overview
Библиотека состоит из трёх модулей: `video_processor.py`, `two_dimensional_statistics.py` и `three_dimensional_statistics.py`.
Модуль `video_processor.py` отвечает за работу с видеозаписями экспериментов и выполняет распознавание [ArUco](https://www.uco.es/investiga/grupos/ava/portfolio/aruco/) маркеров, расположенных на верхней поверхности роботов. 
Модуль `two_dimensional_statistics.py` отвечает за обработку положений и ориентаций роботов на каждом кадре и реализует вычисления двумерных статистических функций (например декартово смещение, параметр порядка  $\psi_6$, параметр пространственно-временной корреляции $\chi_4$).
Модуль `three_dimensional_statistics.py` отвечает за вычисление корреляционных карт (*position*, *orientation* and *velocity* correlation maps)

## video_processor.py
Этот модуль реализует простой интерфейс для использования библиотеки *OpenCV* для изучения роботизированных систем.
Работа с функционалом модуля осуществляется посредством класса `VideoProcessor`:

```python
from amtoolkit.video_processor import VideoProcessor


def main():
    VP = VideoProcessor()
    

if __name__ == '__main__':
    main()
```

:warning: 
Многие функции из модулей `two_dimensional_statistics.py` и `three_dimensional_statistics.py` содежат фрагменты кода с использованием библиотеки модуля `multiprocessing`, поэтому мы рекомендуем по умолчанию писать код внутри выражения ` if __name__ == '__main__':`.
:warning:

Сперва для обработки видеофрагмента необходимо передать в обработчик путь к видеофайлу. Это делается с помощью метода `set_filename`:

```python
from amtoolkit.video_processor import VideoProcessor


def main():
    VP = VideoProcessor()
    filename = 'C:/examplefolder/examplefilename.mp4'
    VP.set_filename(filename)

if __name__ == '__main__':
    main()
```

Далее производится извлечение декартовой кинематики (каждому маркеру в видео покадрово сопостовляется его угол поворота и положение в кадре) с помощью метода `extract_cartesian_kinematics`. 

```python
from amtoolkit.video_processor import VideoProcessor


def main():
    VP = VideoProcessor()
    filename = 'C:/examplefolder/examplefilename.mp4'
    VP.set_filename(filename)
    kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))

if __name__ == '__main__':
    main()
```

Данный метод возвращает список, в котором каждому кадру сопоставлен список из данных о роботах в этом кадре. Данные о каждом роботе состоят из ID его маркера, угла поворота и положения в кадре. В примере видеозапись содержит в себе 45 роботов, обработка ведётся с 120 по 6000 кадр записи, при этом для обработки выбирается каждый пятый кадр. При этом при распознавании коды маркеров с ID 12 и 14 игнорируются. Значения `scale_parameters` отвечают параметрам $\alpha$ и $\beta$ линейного преобразования значений пикселей для изменения яркости и контрастности изображения. Подбор правильных `scale_parameters` является исследовательской задачей и сильно зависит от условий освещения, в которых делалась видеозапись

Для расчёта некоторых статистических величин необходимо кроме декартового представления кинематики системы иметь так же её полярное представление. Для этого нужно воспользоваться методом `extend_kinematics`, который дополнит данные о каждом роботе полярным углом и расстоянием от центра поля (`field_center`):

```python
from amtoolkit.video_processor import VideoProcessor


def main():
    VP = VideoProcessor()
    filename = 'C:/examplefolder/examplefilename.mp4'
    VP.set_filename(filename)
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))


if __name__ == '__main__':
    main()
```

Вся кинематика системы записывается в пикселях. Если для каких-то вычислений необходимо перевести расстояния из пикселей в сантиметры, метод `get_metric_constant`:

```python
from amtoolkit.video_processor import VideoProcessor


def main():
    VP = VideoProcessor()
    filename = 'C:/examplefolder/examplefilename.mp4'
    VP.set_filename(filename)
    metric_constant = VP.get_metric_constant(marker_size=3, scale_parameters=(0.8, -30))


if __name__ == '__main__':
    main()
```

## two_dimensional_statistics.py

Этот модуль реализует вычисления двумерных статистических величин на предварительно извлечённой из видео кинематике.

- Среднее удаление роботов от центра поля. Реализуется функцией `get_mean_distances_from_center`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_distance_from_center


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
    mean_distance_from_center = get_mean_distance_from_center(kinematics=extended_kinematics)


if __name__ == '__main__':
    main()
```

- Средний полярный угол роботов. Реализуется функцией `get_mean_polar_angle`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_polar_angle


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
    mean_polar_angle = get_mean_polar_angle(kinematics=extended_kinematics)


if __name__ == '__main__':
    main()
```

- Средний полярный угол роботов в смысле углового пути системы. Реализуется функцией `get_mean_polar_angle_absolute`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_polar_angle_absolute


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    extended_kinematics = VP.extend_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
    mean_polar_angle_absolute = get_mean_polar_angle_absolute(kinematics=extended_kinematics)


if __name__ == '__main__':
    main()
```

- Среднеквадратичное удаление от начального положения. Реализуется функцией `get_mean_cartesian_displacements`.

```python
from amtoolkit.two_dimensional_statistics import get_mean_cartesian_displacements


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    mean_cartesian_displacements = get_mean_cartesian_displacements(kinematics=cartesian_kinematics)


if __name__ == '__main__':
    main()
```

- Bond-orientational order parameter $\psi_N$. Реализуется функцией `get_bond_orientation`. 

```python
from amtoolkit.two_dimensional_statistics import get_bond_orientation


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    boo = get_bond_orientation(kinematics=cartesian_kinematics, neighbours_number=6, folds_number=6)


if __name__ == '__main__':
    main()
```

- Spatio-temporal correlation parameter $\chi_4$. Реализуется функцией `get_chi_4`.

```python
from amtoolkit.two_dimensional_statistics import get_chi_4


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    chi_4 = get_chi_4(kinematics=cartesian_kinematics, tau=60, a=100)


if __name__ == '__main__':
    main()
```

- Collision graph average clustering coefficient. Реализуется функцией `get_cluster_dynamics`. Also you can specify detection of collision between robots by changing `collide_function` argument of `get_cluster_dynamics`

```python
from amtoolkit.two_dimensional_statistics import get_cluster_dynamics


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    clustering_coefficient = get_cluster_dynamics(kinematics=cartesian_kinematics)


if __name__ == '__main__':
    main()
```



## three_dimensional_statistics.py

Этот модуль реализует вычисления трёхмерных статистических величин на предварительно извлечённой из видео кинематике.

- Two-dimensional pair correlation. Реализуется функцией `get_position_correlation`.

```python
from amtoolkit.three_dimensional_statistics import get_position_correlation


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    position_correlation = get_position_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)


if __name__ == '__main__':
    main()
```

- Orientation correlation function. Реализуется функцией `get_mean_polar_angle`.

```python
from amtoolkit.three_dimensional_statistics import get_orientation_correlation


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    orientation_correlation = get_orientation_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)


if __name__ == '__main__':
    main()
```

- Velocity correlation function. Реализуется функцией `get_mean_polar_angle_absolute`.

```python
from amtoolkit.three_dimensional_statistics import get_velocity_correlation


def main():
    VP = VideoProcessor()
    VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
    cartesian_kinematics = VP.extract_cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
                                                  			get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
    velocity_correlation = get_velocity_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)


if __name__ == '__main__':
    main()
```

