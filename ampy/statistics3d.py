"""
Module provides analysis of robots positions and each frame, calculating various
three-dimensional statistical measures
"""

from multiprocessing.pool import Pool
import os

import numpy as np

RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


def _position_correlation_frame(data_frame: tuple): # pragma: no cover
    kinematics_frame, x_size, y_size = data_frame

    matrix = [[0 for x in range(x_size)] for y in range(y_size)]

    N = len(kinematics_frame)
    distance_matrix = [[(0, 0) for i in range(N)] for j in range(N)]
    for i_ref_bot in range(N):
        sina = np.sin(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        cosa = np.cos(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        for i_bot in range(N):
            if i_bot == i_ref_bot:
                continue
            dx = kinematics_frame[i_bot][2][0] - kinematics_frame[i_ref_bot][2][0]
            dy = kinematics_frame[i_bot][2][1] - kinematics_frame[i_ref_bot][2][1]
            X = round(dy * cosa - dx * sina)
            Y = round(+ dy * sina + dx * cosa)
            distance_matrix[i_ref_bot][i_bot] = (X, Y)

    for i_ref_bot in range(N):
        for i_bot in range(N):
            x, y = distance_matrix[i_ref_bot][i_bot]
            if (0 < x < x_size) and (0 < y < y_size):
                matrix[y][x] += 1 / N**2

    return matrix


def position_correlation(kinematics: list,
                         x_size: int,
                         y_size: int,
                         ) -> list:
    """
    Returns position correlation matrix

    :param kinematics: system's kinematics
    :param x_size: window size for X-axis
    :param y_size: window size for Y-axis
    :return: matrix of scalar values per frame
    """

    data = [(kinematics_frame, x_size, y_size) for kinematics_frame in kinematics]

    with Pool(max(os.cpu_count() - 1, 1)) as pool:
        pc_matrices = pool.map(_position_correlation_frame, data)

    return pc_matrices


def _orientation_correlation_frame(data_frame: tuple): # pragma: no cover
    kinematics_frame, x_size, y_size = data_frame

    matrix = [[0 for x in range(x_size)] for y in range(y_size)]

    N = len(kinematics_frame)
    distance_matrix = [[(0, 0) for i in range(N)] for j in range(N)]
    for i_ref_bot in range(N):
        sina = np.sin(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        cosa = np.cos(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        for i_bot in range(N):
            if i_bot == i_ref_bot:
                continue
            dx = kinematics_frame[i_bot][2][0] - kinematics_frame[i_ref_bot][2][0]
            dy = kinematics_frame[i_bot][2][1] - kinematics_frame[i_ref_bot][2][1]
            X = round(dy * cosa - dx * sina)
            Y = round(+ dy * sina + dx * cosa)
            distance_matrix[i_ref_bot][i_bot] = (X, Y)

    for i_ref_bot in range(N):
        for i_bot in range(N):
            x, y = distance_matrix[i_ref_bot][i_bot]
            if (0 < x < x_size) and (0 < y < y_size):
                matrix[y][x] += np.cos((kinematics_frame[i_bot][1] - kinematics_frame[i_ref_bot][1])
                                       * DEG2RAD) / N**2

    return matrix


def orientation_correlation(kinematics: list,
                            x_size: int,
                            y_size: int,
                            ) -> list:
    """
    Returns orientation correlation matrix

    :param kinematics: system's kinematics
    :param x_size: window size for X-axis
    :param y_size: window size for Y-axis
    :return: matrix of scalar values per frame
    """

    data = [(kinematics_frame, x_size, y_size) for kinematics_frame in kinematics]
    with Pool(max(os.cpu_count() - 1, 1)) as pool:
        oc_matrices = pool.map(_orientation_correlation_frame, data)

    return oc_matrices


def _velocity_correlation_frame(data_frame: tuple): # pragma: no cover
    kinematics_frame, velocities_frame, x_size, y_size = data_frame

    matrix = [[0 for x in range(x_size)] for y in range(y_size)]

    N = len(kinematics_frame)
    distance_matrix = [[(0, 0) for i in range(N)] for j in range(N)]
    for i_ref_bot in range(N):
        sina = np.sin(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        cosa = np.cos(kinematics_frame[i_ref_bot][1] * DEG2RAD)
        for i_bot in range(N):
            if i_bot == i_ref_bot:
                continue
            dx = kinematics_frame[i_bot][2][0] - kinematics_frame[i_ref_bot][2][0]
            dy = kinematics_frame[i_bot][2][1] - kinematics_frame[i_ref_bot][2][1]
            X = round(dy * cosa - dx * sina)
            Y = round(+ dy * sina + dx * cosa)
            distance_matrix[i_ref_bot][i_bot] = (X, Y)

    factor = sum(v[0]**2 + v[1]**2 for v in velocities_frame) / N
    if factor == 0:
        factor = 1
    for i_ref_bot in range(N):
        v = velocities_frame[i_ref_bot]
        for i_bot in range(N):
            u = velocities_frame[i_bot]
            x, y = distance_matrix[i_ref_bot][i_bot]
            if (0 < x < x_size) and (0 < y < y_size):
                matrix[y][x] += 1 * (v[0]*u[0] + v[1]*u[1]) / factor / N**2

    return matrix


def velocity_correlation(kinematics: list,
                         x_size: int,
                         y_size: int,
                         ) -> list:
    """
    Returns velocity correlation matrix

    :param kinematics: system's kinematics
    :param x_size: window size for X-axis
    :param y_size: window size for Y-axis
    :return: matrix of scalar values per frame
    """

    N = len(kinematics[0])
    velocities = [[(0, 0) for i in range(N)]]
    for i_frame in range(1, len(kinematics)):
        velocities_frame = []
        for i_bot in range(N):
            velocities_frame.append((kinematics[i_frame][i_bot][2][0] -
                                     kinematics[i_frame - 1][i_bot][2][0],
                                     kinematics[i_frame][i_bot][2][1] -
                                     kinematics[i_frame - 1][i_bot][2][1]))
        velocities.append(velocities_frame)
    data = [(kinematics[i_frame], velocities[i_frame], x_size, y_size)
            for i_frame in range(1, len(kinematics))]
    with Pool(max(os.cpu_count() - 1, 1)) as pool:
        vc_matrices = pool.map(_velocity_correlation_frame, data)

    return vc_matrices
