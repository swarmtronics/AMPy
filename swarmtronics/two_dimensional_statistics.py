import numpy as np


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


# TODO add docstring
def _extract_orientation_angles(kinematics: list) -> list:
    angles = list(np.arrat(kinematics, dtype = object)[:, :, 1])
    return angles


# TODO add docstring
def _extract_positions(kinematics: list) -> list:
    positions = list(np.arrat(kinematics, dtype = object)[:, :, 2])
    return positions


# TODO add docstring
def _extract_polar_angles(kinematics: list) -> list:
    polar_angles = list(np.array(kinematics, dtype = object)[:, :, 3])
    return polar_angles


# TODO add docstring
def _extract_distances_from_center(kinematics: list) -> list:
    distances = list(np.array(kinematics, dtype = object)[:, :, 4])
    return distances


def calculate_angle(point_a: tuple, point_b: tuple) -> float:
    """
    Returns angle in degrees between OX-axis and (b-a) vector direction

    :param point_a: vector's begin point
    :param point_b: vector's end point
    :return: angle in degrees
    """

    return RAD2DEG * np.arctan2(point_b[1] - point_a[1], point_b[0] - point_a[0])


def calculate_distance(point_a: tuple, point_b: tuple) -> float:
    """
    Returns euclidean distance between two points

    :param point_a: first point
    :param point_b: vector end point
    :return: distance between points
    """

    return ((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)**0.5


def calculate_mean_distance_from_center(kinematics: list) -> list:
    """
    Returns average particles' distance from center for each frame

    :param kinematics: system's kinematics extended by polar coordinates
    :return: average distance from center
    """

    mean_distance = np.array(_extract_distances_from_center(kinematics), dtype=float).mean(axis=1)
    return mean_distance


def calculate_mean_polar_angle(kinematics: list) -> list:
    """
    Returns average particles' polar angle for each frame. Angle for certain frame calculating by accumulating
    all angle changes in previous frames

    :param kinematics: system's kinematics extended by polar coordinates
    :return: average polar angle (from -inf to +inf degrees clockwise in relation to X-axis)
    """

    angles = _extract_polar_angles(kinematics)
    mean_angles_raw = angles.mean(axis=1)
    mean_angles_corrected = [mean_angles_raw[0]]
    for i_frame in range(1, len(mean_angles_raw)):
        difference = mean_angles_raw[i_frame] - mean_angles_raw[i_frame - 1]
        if abs(difference) < 100:
            mean_angles_corrected.append(mean_angles_corrected[-1] + difference)
        else:
            if difference > 0:
                mean_angles_corrected.append(mean_angles_corrected[-1] + difference - 360)
            else:
                mean_angles_corrected.append(mean_angles_corrected[-1] - difference + 360)
    return mean_angles_corrected


def calculate_mean_polar_angle_absolute(kinematics: list):
    """
    Returns average particles' polar angle for each frame. Angle for certain frame calculating by accumulating
    absolute values of all angle changes in previous frames

    :param kinematics: system's kinematics extended by polar coordinates
    :return: system's polar angle route length
    """

    angles = _extract_polar_angles(kinematics)
    mean_angles_raw = angles.mean(axis=1)
    mean_angles_accumulated = [mean_angles_raw[0]]
    for i_frame in range(1, len(mean_angles_raw)):
        absolute_difference = abs(mean_angles_raw[i_frame] - mean_angles_raw[i_frame - 1])
        if absolute_difference < 100:
            mean_angles_accumulated.append(mean_angles_accumulated[-1] + absolute_difference)
        else:
            mean_angles_accumulated.append(mean_angles_accumulated[-1] - absolute_difference + 360)
    return mean_angles_accumulated


def calculate_mean_cartesian_displacements(kinematics: list):
    """
    Returns average particles' cartesian displacement for each frame
    :param kinematics: system's kinematics
    :return: average cartesian displacement for each frame
    """

    positions = _extract_positions(kinematics)
    first_frame_positions = positions[0]
    mean_cartesian_displacements = []
    for i_frame in range(len(positions)):
        current_frame_positions = positions[i_frame]
        current_total_cartesian_displacement = 0
        for i_bot in range(len(first_frame_positions)):
            current_total_cartesian_displacement += calculate_distance(current_frame_positions[i_bot], first_frame_positions[i_bot])
        current_mean_cartesian_displacement = current_total_cartesian_displacement / len(first_frame_positions)
        mean_cartesian_displacements.append(current_mean_cartesian_displacement)
    return mean_cartesian_displacements


def _calculate_local_boo(folds_number: int, bot_position: tuple, neighbours_positions: list):
    p = 0
    for neighbour_index in range(len(neighbours_positions)):
        p += np.exp(1j * folds_number * calculate_angle(bot_position, neighbours_positions[neighbour_index]) * DEG2RAD)
    return np.absolute(p) / len(neighbours_positions)


def calculate_boo(kinematics: list, neighbours_number: int, folds_number: int, get_each: int = 1) -> list:
    """
    Returns bond orientation order parameter for each frame
    :param kinematics: system's kinematics
    :param neighbours_number: number of neighbours to use in calculations
    :param folds_number: number of folds to use in calculations
    :param get_each: frames decimation frequency
    :return: Bond orientation order parameter for each frame
    """

    boo = []
    positions = _extract_positions(kinematics)
    for i_frame in range(0, len(kinematics), get_each):
        current_frame_boo = 0
        current_frame_positions = positions[i_frame]
        for i_bot in range(len(kinematics[i_frame])):
            reference_bot_position = current_frame_positions[i_bot]
            neighbours_positions = current_frame_positions.copy()
            neighbours_positions.sort(key=lambda pos: calculate_distance(reference_bot_position, pos))
            local_boo = _calculate_local_boo(folds_number, reference_bot_position, neighbours_positions)
            current_frame_boo += local_boo
        current_frame_boo /= len(kinematics[i_frame])
        boo.append(current_frame_boo)
    return boo



