"""
Module provides analysis of robots positions and each frame, calculating various
two-dimensional statistical measures
"""

import multiprocessing as mp
import os

import numpy as np


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


def _orientation_angles(kinematics: list) -> list: # pragma: no cover
    angles = list(np.array(kinematics, dtype=object)[:, :, 1])
    return angles


def _positions(kinematics: list) -> list:
    positions = list(np.array(kinematics, dtype=object)[:, :, 2])
    return positions


def _polar_angles(kinematics: list) -> list:
    polar_angles = list(np.array(kinematics, dtype=object)[:, :, 3])
    return polar_angles


def _distances_from_center(kinematics: list) -> list:
    distances = list(np.array(kinematics, dtype=object)[:, :, 4])
    return distances


def _sum_points(p1: tuple, p2: tuple, scale: float = 1) -> tuple: # pragma: no cover
    return (p1[0] + p2[0] * scale,
            p1[1] + p2[1] * scale)


def _cross_product(v: tuple, u: tuple) -> float: # pragma: no cover
    return v[0]*u[1] - v[1]*u[0]


def calc_angle(point_a: tuple, point_b: tuple) -> float:
    """
    Returns angle in degrees between OX-axis and (b-a) vector direction

    :param point_a: vector's begin point
    :param point_b: vector's end point
    :return: scalar value
    """

    return RAD2DEG * np.arctan2(point_b[1] - point_a[1], point_b[0] - point_a[0])


def calc_distance(point_a: tuple, point_b: tuple) -> float:
    """
    Returns Euclidean distance between two points

    :param point_a: first point
    :param point_b: vector end point
    :return: scalar value
    """

    return ((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)**0.5


def mean_distance_from_center(kinematics: list) -> list:
    """
    Returns average particles' distance from center for each frame

    :param kinematics: system's kinematics extended by polar coordinates
    :return: scalar value for each frame
    """

    mean_distance = np.array(_distances_from_center(kinematics), dtype=float).mean(axis=1).tolist()
    return mean_distance


def mean_polar_angle(kinematics: list) -> list:
    """
    Returns average particles' polar angle for each frame. Angle for certain frame calculating
    by accumulating all angle changes in previous frames

    :param kinematics: system's kinematics extended by polar coordinates
    :return: list of scalar values
    """

    angles = _polar_angles(kinematics)
    mean_angles_raw = np.array(angles, dtype=float).mean(axis=1)
    mean_angles_corrected = [mean_angles_raw[0]]
    for i_frame in range(1, len(mean_angles_raw)):
        difference = mean_angles_raw[i_frame] - mean_angles_raw[i_frame - 1]
        if abs(difference) < 100: # pragma: no cover
            mean_angles_corrected.append(mean_angles_corrected[-1] + difference)
        else:
            if difference > 0: # pragma: no cover
                mean_angles_corrected.append(mean_angles_corrected[-1] + difference - 360)
            else: # pragma: no cover
                mean_angles_corrected.append(mean_angles_corrected[-1] - difference + 360)
    return mean_angles_corrected


def mean_polar_angle_absolute(kinematics: list):
    """
    Returns average particles' polar angle for each frame. Angle for certain frame calculating
    by accumulating absolute values of all angle changes in previous frames

    :param kinematics: system's kinematics extended by polar coordinates
    :return: list of scalar values
    """

    angles = _polar_angles(kinematics)
    mean_angles_raw = np.array(angles, dtype=float).mean(axis=1)
    mean_angles_accumulated = [mean_angles_raw[0]]
    for i_frame in range(1, len(mean_angles_raw)):
        absolute_difference = abs(mean_angles_raw[i_frame] - mean_angles_raw[i_frame - 1])
        if absolute_difference < 100: # pragma: no cover
            mean_angles_accumulated.append(mean_angles_accumulated[-1] + absolute_difference)
        else: # pragma: no cover
            mean_angles_accumulated.append(mean_angles_accumulated[-1] - absolute_difference + 360)
    return mean_angles_accumulated


def mean_cartesian_displacements(kinematics: list):
    """
    Returns average particles' cartesian displacement for each frame

    :param kinematics: system's kinematics
    :return: list of scalar values
    """

    positions = _positions(kinematics)
    first_frame_positions = positions[0]
    mcd = []
    for i_frame in range(len(positions)):
        current_frame_positions = positions[i_frame]
        current_total_cartesian_displacement = 0
        for i_bot in range(len(first_frame_positions)):
            current_total_cartesian_displacement += \
                calc_distance(current_frame_positions[i_bot], first_frame_positions[i_bot])
        current_mcd = \
            current_total_cartesian_displacement / len(first_frame_positions)
        mcd.append(current_mcd)
    return mcd


def _local_bond_orientation(folds_number: int, bot_position: tuple, neighbours_positions: list):
    p = 0
    for neighbour_index in range(len(neighbours_positions)):
        p += np.exp(1j * folds_number *
                    calc_angle(bot_position, neighbours_positions[neighbour_index]) * DEG2RAD)
    return np.absolute(p) / len(neighbours_positions)


def bond_orientation(kinematics: list,
                     neighbours_number: int,
                     folds_number: int,
                     get_each: int = 1) -> list:
    """
    Returns bond orientation order parameter

    :param kinematics: system's kinematics
    :param neighbours_number: number of neighbours to use in calculations
    :param folds_number: number of folds to use in calculations
    :param get_each: frames decimation frequency
    :return: list of scalar values
    """

    boo = []
    positions = _positions(kinematics)
    for i_frame in range(0, len(kinematics), get_each):
        current_frame_boo = 0
        current_frame_positions = positions[i_frame]
        for i_bot in range(len(kinematics[i_frame])):
            reference_bot_position = current_frame_positions[i_bot]
            neighbours_positions = list(current_frame_positions.copy())
            neighbours_positions.sort(key=lambda pos: calc_distance(reference_bot_position, pos))
            neighbours_positions = neighbours_positions[:neighbours_number]
            local_boo = \
                _local_bond_orientation(folds_number, reference_bot_position, neighbours_positions)
            current_frame_boo += local_boo
        current_frame_boo /= len(kinematics[i_frame])
        boo.append(current_frame_boo)
    return boo


def chi_4(kinematics: list,
          tau: int,
          a: float) -> float:
    """
    Returns spatio-temporal correlation parameter chi_4 for given time and space gape

    :param kinematics: system's kinematics
    :param tau: characteristic time in frames
    :param a: characteristic distance in pixels
    :return: scalar value
    """

    q_sequence = []
    N = len(kinematics[0])
    for i_frame in range(len(kinematics) - tau):
        q = 0
        for i_bot in range(N):
            q += int(a - calc_distance(kinematics[i_frame + tau][i_bot][2],
                                       kinematics[i_frame][i_bot][2]) >= 0)
        q /= N
        q_sequence.append(q)
    t_corr = N * np.std(q_sequence)
    return t_corr


def _is_collide(bot_1: list, bot_2: list, d: int = 300) -> bool:  # pragma: no cover
    return calc_distance(bot_1[2], bot_2[2]) <= d


def _adjacency_matrix(kinematics_frame: list, collide_function) -> list: # pragma: no cover
    N = len(kinematics_frame)
    adj_matrix = [[0 for i in range(N)] for j in range(N)]
    for i_bot in range(N):
        for j_bot in range(N):
            if i_bot == j_bot:
                continue
            adj_matrix[i_bot][j_bot] = \
                int(collide_function(kinematics_frame[i_bot], kinematics_frame[j_bot]))
    return adj_matrix


def _clustering_coefficient_frame(data_frame: tuple) -> float: # pragma: no cover
    kinematics_frame, collide_function = data_frame
    N = len(kinematics_frame)
    adj_matrix = _adjacency_matrix(kinematics_frame, collide_function)
    cl_coeff = 0
    for i in range(N):
        k_i = sum(adj_matrix[i][j] for j in range(N))
        if k_i in (0, 1):
            continue
        c_i = 0
        for j in range(N):
            for k in range(N):
                c_i += adj_matrix[i][j] * adj_matrix[j][k] * adj_matrix[k][i]
        c_i /= k_i * (k_i - 1)
        cl_coeff += c_i
    cl_coeff /= N
    return cl_coeff


def cluster_dynamics(kinematics: list,
                     collide_function=_is_collide) -> list:
    """
    Returns collision graph average clustering coefficient

    :param kinematics: system's kinematics
    :param collide_function: collision detection function
    :return: list of scalar values
    """

    cl_coeff_seq = []
    data = [(kinematics[i_frame], collide_function) for i_frame in range(len(kinematics))]
    with mp.Pool(max(os.cpu_count() - 1, 1)) as pool:
        cl_coeff_seq = pool.map(_clustering_coefficient_frame, data)
    return cl_coeff_seq
