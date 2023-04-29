Introduction by Example
=======================

We shortly introduce usage basics of AMPy through several self-contained examples. Up to this momemnt, you can follow this tutorial in the format of `Colab Notebook <https://colab.research.google.com/drive/1hiCGXoDtOEO3LOm6RG12111Kiwofh069?usp=sharing>`_ or check out corresponding video:

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="//www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

|

Essentially, AMPy allows you to perform the following processing procedures:

.. contents::
    :local:

Extract Kinematics from Raw Video
-----------------------

We will show a simple example of extracting trajectories from the predefined video:

.. image:: ../../../materials/ampy_test_video_1.gif
  :align: left
  :width: 100%
  
|

To extract the robots' trajectories from the video, we import the `Processor` class from `ampy.processing` and create the corresponding object:convert 

.. code-block:: python

	from ampy.processing import Processor

	VP = Processor()

Firstly, to process a video fragment, you must pass the path to the video file. Use the `set_filename` method for this:

.. code-block:: python

	from amtoolkit.processing import Processor

	VP = Processor()
	filename = 'C:/examplefolder/examplefilename.mp4'
	VP.set_filename(filename)


Next, extract the Cartesian kinematics (each marker in the video is frame-by-frame associated with its rotation angle and position in the frame) using the `cartesian_kinematics` method.

.. code-block:: python

	from amtoolkit.processing import Processor

	VP = Processor()
	filename = 'C:/examplefolder/examplefilename.mp4'
	VP.set_filename(filename)
	kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
						      get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))

This method returns a list in which each frame is associated with a list of data about robots in this frame. The data for each robot consists of its marker ID, rotation angle, and position in the frame. In the example, the video recording contains 45 robots, processing is carried out from the 120th to the 6000th frame of the recording, and every fifth frame is selected for processing. At the same time, marker codes with IDs 12 and 14 are ignored. The `scale_parameters` values correspond to the $\alpha$ and $\beta$ parameters of the linear transformation of pixel values to change the brightness and contrast of the image. Finding the right `scale_parameters` is an exploratory task and is highly dependent on the lighting conditions in which the video was recorded.

To calculate some statistical functions, in addition to the Cartesian representation of the kinematics of the system, it is also necessary to have its polar representation. To do this, use the `polar_kinematics` method, which will complement the data about each robot with a polar angle and distance from the field center (`field_center`):

.. code-block:: python

	from amtoolkit.processing import Processor

	VP = Processor()
	filename = 'C:/examplefolder/examplefilename.mp4'
	VP.set_filename(filename)
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
						      get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))

All kinematics of the system is stored in pixels. In some cases it is necessary to convert distances from pixels to centimeters, using the `metric_constant` method:

.. code-block:: python

	from amtoolkit.processing import Processor

	VP = Processor()
	filename = 'C:/examplefolder/examplefilename.mp4'
	VP.set_filename(filename)
	metric_constant = VP.metric_constant(marker_size=3, scale_parameters=(0.8, -30))


.. Note::
	If you are lucky to have your own tracking software, you can still use AMPy to evaluate various statistical characteristics. In 	order to do that, it is required converting your data to the following format:

	- :obj:``: 
	- :obj:``: 
	- etc.	

Evaluate Group Dynamics
-----------------------

This module allows to extrat two-dimensional characteristics of the previously obtained kinematics. 

- Mean dispacement of robots from the center of the field can be calculated via the `mean_distances_from_center` function:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import mean_distance_from_center


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
	distance = mean_distance_from_center(kinematics=polar_kinematics)
	

- Common mean polar angle:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import mean_polar_angle


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
	polar_angle = mean_polar_angle(kinematics=polar_kinematics)


- Mean polar angle in sense of the angular path of a system:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import mean_polar_angle_absolute


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	polar_kinematics = VP.polar_kinematics(cartesian_kinematics=cartesian_kinematics, field_center=(960, 540))
	polar_angle_absolute = mean_polar_angle_absolute(kinematics=polar_kinematics)


- Mean squared distance from the initial position:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import mean_cartesian_displacements


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartessian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	cartesian_displacement = mean_cartesian_displacements(kinematics=cartesian_kinematics)


- Bond-orientational order parameter $\psi_N$:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import bond_orientation


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	boo = bond_orientation(kinematics=cartesian_kinematics, neighbours_number=6, folds_number=6)


- Spatio-temporal correlation parameter $\chi_4$:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import chi_4


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	t_corr = chi_4(kinematics=cartesian_kinematics, tau=60, a=100)
	```


- Average clustering coefficient of a collision graph:

.. code-block:: python


	from amtoolkit.processing import Processor
	from amtoolkit.statistics2d import cluster_dynamics


	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
							    get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	clustering_coefficient = cluster_dynamics(kinematics=cartesian_kinematics)


Also you can specify detection of collision between robots by changing `collide_function` argument of `cluster_dynamics`.

<a name="stats3d"/>

## statistics3d.py

This module allows to extract three-dimensional statistical characteristics of obtained kinematics:

- Positional pair correlation is realized by `position_correlation`:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics3d import position_correlation

	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
								get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	position_correlation = position_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)


- Orientation correlation function can be computed via `orientation_correlation`:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics3d import orientation_correlation

	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
								get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	orientation_correlation = orientation_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)


- Velocity correlation can be computed as fit is based on the `velocity_correlation` function:

.. code-block:: python

	from amtoolkit.processing import Processor
	from amtoolkit.statistics3d import velocity_correlation

	VP = Processor()
	VP.set_filename(filename='C:/examplefolder/examplefilename.mp4')
	cartesian_kinematics = VP.cartesian_kinematics(bots_number=45, begin_frame=120, end_frame=6000,
								get_each=5, ignore_codes=(12, 14), scale_parameters=(0.8, -30))
	velocity_correlation = velocity_correlation(kinematics=cartesian_kinematics, x_size=400, y_size=400)
