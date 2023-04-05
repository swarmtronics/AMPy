import cv2
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


def calc_angle(point_a: tuple, point_b: tuple) -> float:
    """
    Returns angle in degrees between OX-axis and (b-a) vector direction

    :param point_a: vector's begin point
    :param point_b: vector's end point
    :return: angle in degrees
    """
    return RAD2DEG * np.arctan2(point_b[1] - point_a[1], point_b[0] - point_a[0])


def calc_distance(point_a: tuple, point_b: tuple) -> float:
    """
    Returns euclidean distance between two points

    :param point_a: first point
    :param point_b: vector end point
    :return: distance between points
    """

    return ((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)**0.5


class Processor:
    def __init__(self):
        self._filename = None
        self._cartesian_kinematics = None
        self._polar_kinematics = None
        self._aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_1000)
        self._aruco_parameters = cv2.aruco.DetectorParameters_create()

    def set_filename(self, filename: str) -> None:
        self._filename = filename

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
        :return: list of frame-by-frame particles cartesian kinematics including particles ids,
        cartesian coordinates and rotation angles (from 0 to 360 degrees clockwise in relation to X-axis)
        """

        alpha, beta = scale_parameters
        video_capture = cv2.VideoCapture(self._filename)

        if begin_frame < 1:
            start_frame = 1
        else:
            start_frame = begin_frame

        frames_number = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        if end_frame > frames_number:
            finish_frame = frames_number
        else:
            finish_frame = end_frame

        raw_cartesian_kinematics = []
        for current_frame in range(start_frame, finish_frame + 1, get_each):
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
            success, frame = video_capture.read()
            if not success:
                raw_cartesian_kinematics.append([])
                continue
            frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            raw_cart_kin_for_frame = self._raw_cartesian_kinematics_from_frame(frame_converted,
                                                                               ignore_codes)
            raw_cartesian_kinematics.append(raw_cart_kin_for_frame)

        completed_cartesian_kinematics = self._fill_gaps_in_raw_kinematics(bots_number, raw_cartesian_kinematics)
        self._cartesian_kinematics = completed_cartesian_kinematics
        return completed_cartesian_kinematics

    @staticmethod
    def polar_kinematics(cartesian_kinematics: list, field_center: tuple) -> list:
        """
        Returns kinematics extended by a polar angle (from 0 to 360 degrees clockwise in relation to X-axis) and a distance from field center for each particle

        :param cartesian_kinematics: cartesian kinematics of a system
        :param field_center: a center of a polar coordinates
        :return: polar system's kinematics
        """

        polar_kinematics = deepcopy(cartesian_kinematics)
        for i_frame in range(len(polar_kinematics)):
            for i_bot in range(len(polar_kinematics[i_frame])):
                polar_kinematics[i_frame][i_bot] = [
                    polar_kinematics[i_frame][i_bot][0],
                    polar_kinematics[i_frame][i_bot][1],
                    polar_kinematics[i_frame][i_bot][2],
                    calc_angle(field_center, polar_kinematics[i_frame][i_bot][2]),
                    calc_distance(field_center, polar_kinematics[i_frame][i_bot][2])
                ]
        return polar_kinematics

    def field_center_manual(self) -> tuple:
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

    # TODO implement the function
    def field_center_auto(self, first_line_markers: tuple, second_line_markers: tuple) -> tuple:
        """
        Return center of the field calculated as the intersection of two lines which were defined by two pairs of
        markers

        :param first_line_markers: markers IDs to define the first line
        :param second_line_markers: markers IDs to define the second line
        :return: field's center
        """
        ...

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
        while not success:
            success, frame = video_capture.read()
        frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame_converted, self._aruco_dictionary, parameters=self._aruco_parameters
        )
        if len(corners) == 0:
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
                                             ) -> list:
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
            if marker_id in ignore_codes:
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
    def _center_of_image(image: np.ndarray) -> tuple:
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
    def _fill_gaps_in_raw_kinematics(bots_number: int, raw_cartesian_kinematics: list) -> list:
        """
        Returns cartesian kinematics with filling gaps from unrecognized bots by they future positions

        :param bots_number: total number of particles in video
        :param raw_cartesian_kinematics: raw cartesian kinematics
        :return: cartesian kinematics with filled gaps
        """
        raw_kinematics = deepcopy(raw_cartesian_kinematics)

        frames_number = len(raw_kinematics)
        best_recognized_frame_number = 0

        for i in range(1, frames_number):
            if len(raw_kinematics[i]) > len(raw_kinematics[best_recognized_frame_number]):
                best_recognized_frame_number = i

        top_recognized_bots_number = len(raw_kinematics[best_recognized_frame_number])
        if top_recognized_bots_number != bots_number:
            return raw_kinematics

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
                        else:
                            for i_new_bot in range(len(raw_kinematics[i_next_frame])):
                                if raw_kinematics[i_next_frame][i_new_bot][0] == difference[i_absent_bot]:
                                    raw_kinematics[i_frame].append(raw_kinematics[i_next_frame][i_new_bot])
                                    bot_searched_out = True
                                    break
                        if bot_searched_out:
                            break
        complete_kinematics = [sorted(raw_kinematics[i_frame].copy()) for i_frame in range(frames_number) if (len(raw_kinematics[i_frame])) == bots_number]
        return complete_kinematics


if __name__ == '__main__':
    print(__name__)
