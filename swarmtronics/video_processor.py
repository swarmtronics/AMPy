import cv2
import numpy as np


RAD2DEG = 180 / np.pi
DEG2RAD = np.pi / 180


class VideoProcessor():
    def __init__(self):
        self._filename = None
        self._cartesian_kinematics = None
        self._extended_kinematics = None
        self._aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_1000)
        self._aruco_parameters = cv2.aruco.DetectorParameters_create()


    def set_filename(self, filename: str) -> None:
        self._filename = filename

    def extract_cartesian_kinematics(self,
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
        cartesian coordinates and rotation angles
        """

        alpha, beta = scale_parameters
        video_capture = cv2.VideoCapture(self._filename)

        if begin_frame < 1:
            start_frame = 1
        else:
            start_frame = begin_frame

        frames_number = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

        if end_frame > frames_number:
            finish_frame = frames_number
        else:
            finish_frame = end_frame

        raw_cartesian_kinematics = []
        for current_frame in range(start_frame, finish_frame + 1, get_each):
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
            success, frame = video_capture.read()
            if not success:
                continue
            frame_converted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            raw_cartesian_kinematics_for_frame = self._get_raw_cartesian_kinematics_from_frame(frame_converted,
                                                                                               ignore_codes)
            raw_cartesian_kinematics.append((current_frame, raw_cartesian_kinematics_for_frame))

        pass

    def _get_raw_cartesian_kinematics_from_frame(self,
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

            angle = self._get_angle((center_x, center_y),
                                    (top_mid_x, top_mid_y))
            if angle < 0:
                angle = 360 + angle
            # angle increasing corresponds clockwise rotation
            raw_kinematics_for_frame.append([marker_id, angle, (center_x, center_y)])
        return sorted(raw_kinematics_for_frame)

    def _get_angle(self, point_a: tuple, point_b: tuple) -> float:
        """
        Returns angle in degrees between OX-axis and (b-a) vector direction
        :param point_a: vector begin point
        :param point_b: vector end point
        :return: angle in degrees
        """
        return RAD2DEG * np.arctan2(point_b[1] - point_a[1], point_b[0] - point_a[0])







if __name__ == '__main__':
    print(__name__)

