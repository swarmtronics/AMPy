"""
Module provides the processing of experimental video recordings and identifies ArUco markers
placed on the robots' upper surfaces
"""
from copy import deepcopy
from tqdm import tqdm
import pickle

import numpy as np

import cv2
from matplotlib import pyplot as plt


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11,
}


def calc_angle(point_a: tuple, point_b: tuple) -> float: # pragma: no cover
    """
    Returns angle in degrees between OX-axis and (b-a) vector direction

    :param point_a: vector's begin point
    :param point_b: vector's end point
    :return: angle in degrees
    """
    return RAD2DEG * np.arctan2(point_b[1] - point_a[1], point_b[0] - point_a[0])


def calc_distance(point_a: tuple, point_b: tuple) -> float: # pragma: no cover
    """
    Returns Euclidean distance between two points

    :param point_a: first point
    :param point_b: vector end point
    :return: distance between points
    """

    return ((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)**0.5


class Processor:
    """
    *processing.Processor* class provides interface for processing of experiment videos
    """
    def __init__(self):
        self._filename = None
        self._cartesian_kinematics = None
        self._polar_kinematics = None
        self._time = None
        self._aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_1000)
        self._aruco_parameters = cv2.aruco.DetectorParameters_create()

    def set_filename(self, filename: str) -> None: # pragma: no cover
        """
        Set path to the file you want to process
        :param filename: the path
        """
        self._filename = filename

    def set_aruco_dict(self, dict_name: str): # pragma: no cover
        """
        Set ArUco dictionary you want to use to
        :param dict_name: the name of the dict
        """
        if dict_name in ARUCO_DICT.keys():
            self._aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])

    def get_time(self) -> int: # pragma: no cover
        """
        Returns the time parameter

        :return: the time parameter of extracted kinematics
        """
        return self._time

    def cartesian_kinematics(self,
                             bots_number: int,
                             begin_frame: int,
                             end_frame: int,
                             get_each: int,
                             ignore_codes: tuple,
                             scale_parameters: tuple,
                             ) -> list:
        """
        Returns cartesian kinematics for particles in video with given processing parameters

        :param bots_number: number of bots in video
        :param begin_frame: frame to begin the processing
        :param end_frame: frame to end the processing
        :param get_each: frames decimation frequency
        :param ignore_codes: markers to ignore while recognition
        :param scale_parameters: pixels absolute scaling parameters
        :return: list of frame-by-frame particles cartesian kinematic
        """

        alpha, beta = scale_parameters
        video_capture = cv2.VideoCapture(self._filename)

        if begin_frame < 1: # pragma: no cover
            start_frame = 1
        else:
            start_frame = begin_frame

        frames_number = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        if end_frame > frames_number: # pragma: no cover
            finish_frame = frames_number
        else:
            finish_frame = end_frame

        raw_cart_kin = []
        for current_frame in tqdm(range(start_frame, finish_frame + 1, get_each)):
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
            success, frame = video_capture.read()
            if not success: # pragma: no cover
                raw_cart_kin.append([])
                continue
            frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            raw_cart_kin_for_frame = self._raw_cartesian_kinematics_from_frame(frame_converted,
                                                                               ignore_codes)
            raw_cart_kin.append(raw_cart_kin_for_frame)

        completed_cart_kin = self._fill_gaps_in_raw_kinematics(bots_number, raw_cart_kin)
        self._cartesian_kinematics = completed_cart_kin
        self._time = len(completed_cart_kin)
        return completed_cart_kin

    @staticmethod
    def polar_kinematics(cartesian_kinematics: list, field_center: tuple) -> list:
        """
        Returns kinematics extended by a polar angle
        (from 0 to 360 degrees clockwise in relation to X-axis)
        and a distance from field center for each particle

        :param cartesian_kinematics: cartesian kinematics of a system
        :param field_center: a center of a polar coordinates
        :return: polar system's kinematics
        """

        polar_kinematics = deepcopy(cartesian_kinematics)
        for i_frame in tqdm(range(len(polar_kinematics))):
            for i_bot in range(len(polar_kinematics[i_frame])):
                polar_kinematics[i_frame][i_bot] = [
                    polar_kinematics[i_frame][i_bot][0],
                    polar_kinematics[i_frame][i_bot][1],
                    polar_kinematics[i_frame][i_bot][2],
                    calc_angle(field_center, polar_kinematics[i_frame][i_bot][2]),
                    calc_distance(field_center, polar_kinematics[i_frame][i_bot][2])
                ]
        return polar_kinematics

    def field_center_manual(self) -> tuple: # pragma: no cover
        """
        Shows the video's first frame and returns clicked point coordinates

        :return: clicked point coordinates
        """
        video_capture = cv2.VideoCapture(self._filename)
        success, frame = video_capture.read()
        while not success:
            success, frame = video_capture.read()
        center = self._center_of_image(frame)
        return center

    @staticmethod
    def _lines_intersection(first_line_points: tuple, second_line_points: tuple)\
            -> tuple: # pragma: no cover
        """
        Return intersection point of two lines defined by two segments
        """
        p_1, q_1 = first_line_points
        p_2, q_2 = second_line_points
        s_1 = (q_1[0] - p_1[0], q_1[1] - p_1[1])
        s_2 = (q_2[0] - p_2[0], q_2[1] - p_2[1])
        delta = s_2[0] * (-s_1[1]) - (-s_1[0]) * s_2[1]
        delta_2 = (p_1[0] - p_2[0]) * (-s_1[1]) - (-s_1[0]) * (p_1[1] - p_2[1])
        t_2 = delta_2 / delta
        return p_2[0] + t_2 * s_2[0], p_2[1] + t_2 * s_2[1]

    def field_center_auto(self,
                          first_line_markers: tuple,
                          second_line_markers: tuple,
                          scale_parameters: tuple) -> tuple:
        """
        Return center of the field calculated as the intersection of two lines which were defined by
        two pairs of markers

        :param first_line_markers: markers IDs to define the first line
        :param second_line_markers: markers IDs to define the second line
        :param scale_parameters: pixels absolute scaling parameters
        :return: field's center
        """
        alpha, beta = scale_parameters
        video_capture = cv2.VideoCapture(self._filename)
        poses = []
        n_frames_to_try = min(100, int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        for i_frame in range(n_frames_to_try):
            success, frame = video_capture.read()
            while not success: # pragma: no cover
                success, frame = video_capture.read()
            frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            (corners, ids, rejected) = cv2.aruco.detectMarkers(
                frame_converted, self._aruco_dictionary, parameters=self._aruco_parameters
            )
            ids = ids.flatten()
            if set(first_line_markers + second_line_markers).issubset(set(ids.tolist())):
                idx_1 = np.where(ids == first_line_markers[0])
                (top_left, top_right, bottom_right, bottom_left)\
                    = corners[idx_1[0][0]].reshape((4, 2))
                center_1 = ((top_left[0] + bottom_right[0]) // 2,
                            (top_left[1] + bottom_right[1]) // 2)
                idx_2 = np.where(ids == first_line_markers[1])
                (top_left, top_right, bottom_right, bottom_left)\
                    = corners[idx_2[0][0]].reshape((4, 2))
                center_2 = ((top_left[0] + bottom_right[0]) // 2,
                            (top_left[1] + bottom_right[1]) // 2)
                idx_3 = np.where(ids == second_line_markers[0])
                (top_left, top_right, bottom_right, bottom_left)\
                    = corners[idx_3[0][0]].reshape((4, 2))
                center_3 = ((top_left[0] + bottom_right[0]) // 2,
                            (top_left[1] + bottom_right[1]) // 2)
                idx_4 = np.where(ids == second_line_markers[1])
                (top_left, top_right, bottom_right, bottom_left)\
                    = corners[idx_4[0][0]].reshape((4, 2))
                center_4 = ((top_left[0] + bottom_right[0]) // 2,
                            (top_left[1] + bottom_right[1]) // 2)
                poses.append((center_1, center_2))
                poses.append((center_3, center_4))
                break
        if not poses: # pragma: no cover
            return None
        center = self._lines_intersection(poses[0], poses[1])
        return center



    def metric_constant(self, marker_size: float, scale_parameters: tuple) -> float:
        """
        Returns factor that scale distances in pixel on video to distances in centimeters

        :param marker_size: used ArUco marker size in centimeters
        :param scale_parameters: pixels absolute scaling parameters
        :return: scaling factor
        """

        alpha, beta = scale_parameters
        video_capture = cv2.VideoCapture(self._filename)
        success, frame = video_capture.read()
        while not success: # pragma: no cover
            success, frame = video_capture.read()
        frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame_converted, self._aruco_dictionary, parameters=self._aruco_parameters
        )
        if len(corners) == 0: # pragma: no cover
            return None
        marker_corners = corners[0]
        (top_left, top_right, bottom_right, bottom_left) = marker_corners.reshape((4, 2))
        top_right = (int(top_right[0]), int(top_right[1]))
        top_left = (int(top_left[0]), int(top_left[1]))
        metric_constant = marker_size / calc_distance(top_left, top_right)
        return metric_constant

    def _raw_cartesian_kinematics_from_frame(self,
                                             frame: np.ndarray,
                                             ignore_codes: tuple,
                                             ) -> list: # pragma: no cover
        """
        Returns raw cartesian kinematics for particles in frame

        :param frame: frame to process
        :return: raw cartesian kinematics for the given frame
        """
        if frame is None:
            return []
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                                           self._aruco_dictionary,
                                                           parameters=self._aruco_parameters
                                                           )
        raw_kinematics_for_frame = []
        recognized_markers_number = len(corners)
        for i in range(recognized_markers_number):
            marker_corners = corners[i]
            marker_id = ids[i][0]
            if marker_id in ignore_codes: # pragma: no cover
                continue
            (top_left, top_right, bottom_right, bottom_left) = marker_corners.reshape((4, 2))
            (top_left, top_right, bottom_right, bottom_left) = (tuple(map(int, top_left)),
                                                                tuple(map(int, top_right)),
                                                                tuple(map(int, bottom_right)),
                                                                tuple(map(int, bottom_left)),
                                                                )
            center_x = (top_left[0] + bottom_right[0]) // 2
            center_y = (top_left[1] + bottom_right[1]) // 2
            top_mid_x = (top_left[0] + top_right[0]) // 2
            top_mid_y = (top_left[1] + top_right[1]) // 2

            angle = calc_angle((center_x, center_y),
                               (top_mid_x, top_mid_y))
            if angle < 0:
                angle = 360 + angle
            # angle increasing corresponds clockwise rotation
            raw_kinematics_for_frame.append([marker_id, angle, (center_x, center_y)])
        return sorted(raw_kinematics_for_frame)

    @staticmethod
    def _center_of_image(image: np.ndarray) -> tuple: # pragma: no cover
        """
        Shows matplotlib window with a given images. Returns last clicked point

        :param image: image to show
        :return: last clicked point
        """
        center = []

        def onclick(event):
            value = (event.xdata, event.ydata)
            center.append(value)
            return center

        fig, ax = plt.subplots()
        plt.imshow(image)
        fig.canvas.mpl_connect("button_press_event", onclick)
        plt.show()
        return center[-1]

    @staticmethod
    def _fill_gaps_in_raw_kinematics(bots_number: int, raw_cartesian_kinematics: list)\
            -> list: # pragma: no cover
        """
        Returns cartesian kinematics with filling gaps from unrecognized bots
        by they future positions

        :param bots_number: total number of particles in video
        :param raw_cartesian_kinematics: raw Cartesian kinematics
        :return: Cartesian kinematics with filled gaps
        """
        raw_kinematics = deepcopy(raw_cartesian_kinematics)

        frames_number = len(raw_kinematics)
        best_recognized_frame_number = 0

        for i in range(1, frames_number):
            if len(raw_kinematics[i]) > len(raw_kinematics[best_recognized_frame_number]):
                best_recognized_frame_number = i

        top_recognized_bots_number = len(raw_kinematics[best_recognized_frame_number])

        assert  top_recognized_bots_number <= bots_number, 'Number of recognized markers exceeded the expected value. Kinematics processing was aborted!'
        assert  top_recognized_bots_number >= bots_number, 'Number of recognized markers did not reach the expected value. Kinematics processing was aborted!'

        total_ids = np.array(raw_kinematics[best_recognized_frame_number])[:, 0]
        for i_frame in range(frames_number):
            if len(raw_kinematics[i_frame]) != bots_number:
                if len(raw_kinematics[i_frame]) == 0:
                    current_ids = np.array([])
                else:
                    current_ids = np.array(raw_kinematics[i_frame])[:, 0]
                difference = list(set(total_ids) - set(current_ids))
                for i_absent_bot in range(len(difference)):
                    for i_next_frame in range(i_frame + 1, frames_number):
                        bot_searched_out = False
                        if len(raw_kinematics[i_next_frame]) == 0:
                            new_bots_ids = np.array([])
                        else:
                            new_bots_ids = np.array(raw_kinematics[i_next_frame])[:, 0]
                        if difference[i_absent_bot] not in set(new_bots_ids):
                            continue
                        for i_new_bot in range(len(raw_kinematics[i_next_frame])):
                            if raw_kinematics[i_next_frame][i_new_bot][0] ==\
                                    difference[i_absent_bot]:
                                raw_kinematics[i_frame].append(
                                    raw_kinematics[i_next_frame][i_new_bot])
                                bot_searched_out = True
                                break
                        if bot_searched_out:
                            break
        complete_kinematics = [sorted(raw_kinematics[i_frame].copy())
                               for i_frame in range(frames_number)
                               if (len(raw_kinematics[i_frame])) == bots_number]
        return complete_kinematics

    @staticmethod
    def load_p(filename) -> list:
        """
        Load system's kinematics serialized by *pickle*
        :param filename: path to *.pickle* file
        :return: system's kinematics
        """
        with open(filename, 'rb') as file:
            kin = list(pickle.load(file))
            if not kin: # pragma: no cover
                return None
            for i, bot in enumerate(kin):
                if len(bot) != len(kin[0]): # pragma: no cover
                    return None
            return kin
