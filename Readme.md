# AM Toolkit

**AM Toolkit** is a *baseline* library built upon [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) to easily process experimental video data for active matter and disordered systems.
Библиотека превращает обработку видеозаписей экспериментов из тяжкого труда в лёгкую прогулку и многократно ускоряет процесс написания кода с целью извлечения из видео полезных характеристик.

# Library content
## Overview
Библиотека состоит из трёх модулей: `video_processor.py`, `two_dimensional_statistics.py` и `three_dimensional_statistics.py`.
Модуль `video_processor.py` отвечает за работу с видеозаписями экспериментов и выполняет распознавание [ArUco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) маркеров, расположенных на верхней поверхности роботов. 
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

Данный метод возвращает список, в котором каждому кадру сопоставлен список из данных о роботах в этом кадре. Данные о каждом роботе состоят из ID его маркера, угла поворота и положения в кадре. В примере видеозапись содержит в себе 45 роботов, обработка ведётся с 120 по 6000 кадр записи, при этом для обработки выбирается каждый пятый кадр. При этом при распознавании коды маркеров с ID 12 и 14 игнорируются. Значения `scale_parameters` отвечают параметрам $\alpha$ и $\beta$ линейного преобразования значений пикселей для изменения яркости и контрастности изображения.

Для расчёта некоторых статистических величин необходимо кроме декартового представления кинематики системы иметь так же её полярное представление

