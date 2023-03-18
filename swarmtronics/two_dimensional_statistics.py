import numpy as np
from tqdm import tqdm
import multiprocessing as mp
import os
from math import sin, cos


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


stadium_bot_approx_points = [(0, 4.25),
                             (1.09, 4),
                             (1.79, 3.5),
                             (2.17, 3),
                             (2.38, 2.5),
                             (2.5, 1.75),
                             (2.5, -1.75),
                             (2.38, -2.5),
                             (2.17, -3),
                             (1.79, -3.5),
                             (1.09, -4),
                             (0, -4.25),
                             (-1.09, -4),
                             (-1.79, -3.5),
                             (-2.17, -3),
                             (-2.38, -2.5),
                             (-2.5, -1.75),
                             (-2.5, 1.75),
                             (-2.38, 2.5),
                             (-2.17, 3),
                             (-1.79, 3.5),
                             (-1.09, 4),
                             ]


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


# TODO add docstrings
def calculate_chi_4(tau: int,
                    a: float,
                    kinematics: list) -> float:
    q_sequence = []
    N = len(kinematics[0])
    for i_frame in range(len(kinematics) - tau):
        q = 0
        for i_bot in range(N):
            q += int(a - calculate_distance(kinematics[i_frame + tau][i_bot][2], kinematics[i_frame][i_bot][2]) >= 0)
        q /= N
        q_sequence.append(q)
    chi_4 = N * np.std(q_sequence)
    return chi_4

def _calculate_chi_4_for_stcp(data: tuple) -> float:
    tau, a, kinematics = data
    q_sequence = []
    N = len(kinematics[0])
    for i_frame in range(len(kinematics) - tau):
        q = 0
        for i_bot in range(N):
            q += int(a - calculate_distance(kinematics[i_frame + tau][i_bot][2], kinematics[i_frame][i_bot][2]) >= 0)
        q /= N
        q_sequence.append(q)
    chi_4 = N * np.std(q_sequence)
    return chi_4

# TODO add docstrings
def calculate_stcp(kinematics: list,
                   a: float,
                   upper_bound: int = None,) -> tuple:
    if upper_bound is None:
        upper_bound = len(kinematics) - 1
    chi_4_sequence = []
    data = [(tau, a, kinematics) for tau in range(1, upper_bound + 1)]
    with mp.Pool(max(os.cpu_count()- 1, 1)) as pool:
        chi_4_sequence = pool.map(_calculate_chi_4_for_stcp, data)
    stcp = max(chi_4_sequence)
    return stcp, chi_4_sequence


def _sum_points(p1: tuple, p2: tuple, scale: float = 1) -> tuple:
    return (p1[0] + p2[0] * scale,
            p1[1] + p2[1] * scale)


def _cross_product(v: tuple, u: tuple) -> float:
    return v[0]*u[1] - v[1]*u[0]


def _get_triangle_orientation(p1: tuple, p2: tuple, p3: tuple, eps: float = 1e-9) -> int:
    val = _cross_product(_sum_points(p2, p1, scale=-1),
                        _sum_points(p3, p1, scale=-1))

    if abs(val) <= eps:
        return 0

    if val > 0:
        return 1
    else:
        return -1


def _check_point_on_segment(p1: tuple, p2: tuple, q: tuple) -> bool:
    return p1[0] <= q[0] <= p2[0] and p1[1] <= q[1] <= p2[1]


def _check_two_segments_intersection(p1: tuple, p2: tuple, q1: tuple, q2: tuple) -> bool:
    o1 = _get_triangle_orientation(p1, p2, q1)
    o2 = _get_triangle_orientation(p1, p2, q2)
    o3 = _get_triangle_orientation(q1, q2, p1)
    o4 = _get_triangle_orientation(q1, q2, p2)

    return (((o1 != o2) and (o3 != o4)) or
            ((o1 == 0) and _check_point_on_segment(p1, p2, q1)) or
            ((o2 == 0) and _check_point_on_segment(q1, q2, p1)) or
            ((o3 == 0) and _check_point_on_segment(p1, p2, q2)) or
            ((o4 == 0) and _check_point_on_segment(q1, q2, p2)))


def _check_polygon_intersection(polygon_1: list, polygon_2: list) -> bool:
    intersection = False
    for i in range(len(polygon_1)):
        p1 = polygon_1[i]
        p2 = polygon_1[(i + 1) % len(polygon_1)]
        for j in range(len(polygon_2)):
            q1 = polygon_2[j]
            q2 = polygon_2[(j + 1) % len(polygon_2)]
            intersection = intersection or _check_two_segments_intersection(p1, p2, q1, q2)
            if intersection:
                return intersection
    return intersection


def _is_collide(bot_1: list, bot_2: list, metric_const: float) -> bool:
    angle_1 = bot_1[1]
    x_1, y_1 = bot_1[2]
    angle_2 = bot_2[1]
    x_2, y_2 = bot_2[2]
    scaling_coeff = 1.2
    sin1 = sin(angle_1*DEG2RAD)
    cos1 = cos(angle_1*DEG2RAD)
    sin2 = sin(angle_2*DEG2RAD)
    cos2 = cos(angle_2*DEG2RAD)
    x_1, y_1, x_2, y_2 = (item / scaling_coeff * metric_const for item in (x_1, y_1, x_2, y_2))
    dx = x_2 - x_1
    dy = y_2 - y_1
    polygon_1 = [(p[1] * cos1 - p[0] * sin1, p[1] * sin1 + p[0] * cos1) for p in stadium_bot_approx_points]
    polygon_2 = [(dy + p[1] * cos2 - p[0] * sin2, dx + p[1] * sin2 + p[0] * cos2) for p in stadium_bot_approx_points]
    return _check_polygon_intersection(polygon_1, polygon_2)


def _calculate_adj_matrix(kinematics_frame: list, metric_constant: float) -> list:
    N = len(kinematics_frame)
    adj_matrix = [[0 for i in range(N)] for j in range(N)]
    for i_bot in range(N):
        for j_bot in range(N):
            if i_bot == j_bot:
                continue
            adj_matrix[i_bot][j_bot] = int(_is_collide(kinematics_frame[i_bot], kinematics_frame[j_bot], metric_constant))
    return adj_matrix


def _calculate_clustering_coefficient_frame(data_frame: tuple) -> float:
    kinematics_frame, metric_constant = data_frame
    N = len(kinematics_frame)
    adj_matrix = _calculate_adj_matrix(kinematics_frame, metric_constant)
    # print(adj_matrix)
    cl_coeff = 0
    for i in range(N):
        k_i = sum(adj_matrix[i][j] for j in range(N))
        if (k_i == 0) or (k_i == 1):
            continue
        c_i = 0
        for j in range(N):
            for k in range(N):
                c_i += adj_matrix[i][j] * adj_matrix[j][k] * adj_matrix[k][i]
        c_i /= k_i * (k_i - 1)
        cl_coeff += c_i
    cl_coeff /= N
    return cl_coeff


# TODO add docstrings
def calculate_clustering_coefficient(kinematics: list, metric_constant: float) -> list:
    cl_coeff_seq = []
    data = [(kinematics[i_frame], metric_constant) for i_frame in range(len(kinematics))]
    with mp.Pool(max(os.cpu_count() - 1, 1)) as pool:
        cl_coeff_seq = pool.map(_calculate_clustering_coefficient_frame, data)
    # for i_frame in range(len(kinematics)):
    #     cl_coeff_seq.append(_calculate_clustering_coefficient_frame(kinematics[i_frame], metric_constant))
    return cl_coeff_seq





