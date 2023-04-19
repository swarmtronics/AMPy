"""
Module provides tests for the *ampy.processing*
"""

import os
import numpy as np

import unittest

import cv2

from ampy.processing import Processor


class TestProcessing(unittest.TestCase):
    """
    *TestProcessing* class provides tests for the *processing.Processor* class
    """

    def setUp(self) -> None:
        """
        Initialize objects for testing
        """

        self.vp = Processor()
        self.vp.set_filename(os.path.dirname(__file__) + "/"
                             + 'test_processing_files/test_video.mp4')

    def test_cartesian_kinematics(self):
        """
        Test *cartesian_kinematics* method
        """

        # assign

        truth = np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/cartesian_kinematics_truth.npy",
                        allow_pickle=True).tolist()

        # assert

        def _is_equal(result, truth_result):
            """
            Check equality of two Cartesian kinematics
            """

            if len(result) != len(truth_result):
                return False
            for i_frame in range(len(result)):
                if len(result[i_frame]) != len(truth_result[i_frame]):
                    return False
                for i_bot in range(len(result[i_frame])):
                    if result[i_frame][i_bot][0] != truth_result[i_frame][i_bot][0]:
                        return False
                    if abs(result[i_frame][i_bot][1] - truth_result[i_frame][i_bot][1]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][0] - truth_result[i_frame][i_bot][2][0]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][1] - truth_result[i_frame][i_bot][2][1]) > 0.1:
                        return False
            return True

        result = self.vp.cartesian_kinematics(2, 1, 100, 1, (114, 115, 116, 117), (1, 0))
        self.assertTrue(_is_equal(result, truth))

    def test_field_center_auto(self):
        """
        Test *field_center_auto* method
        """

        # assign

        truth = np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/field_center_auto_truth.npy",
                        allow_pickle=True).tolist()

        # assert

        def _is_equal(result, truth_result):
            """
            Check equality of two tuples
            """

            if len(result) != len(truth_result):
                return False
            for i in range(len(result)):
                if abs(result[i] - truth_result[i]) > 0.1:
                    return False
            return True

        result = self.vp.field_center_auto((114, 116), (115, 117), (1, 0))
        self.assertTrue(_is_equal(result, truth))

    def test_polar_kinematics(self):
        """
        Test *polar_kinematics* method
        """

        # assign

        truth = np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/polar_kinematics_truth.npy",
                        allow_pickle=True).tolist()
        cart_kin = np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/cartesian_kinematics_truth.npy",
                        allow_pickle=True).tolist()

        center = tuple(np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/field_center_auto_truth.npy",
                        allow_pickle=True).tolist())

        # assert

        def _is_equal(result, truth_result):
            """
            Check equality of two polar kinematics
            """

            if len(result) != len(truth_result):
                return False
            for i_frame in range(len(result)):
                if len(result[i_frame]) != len(truth_result[i_frame]):
                    return False
                for i_bot in range(len(result[i_frame])):
                    if result[i_frame][i_bot][0] != truth_result[i_frame][i_bot][0]:
                        return False
                    if abs(result[i_frame][i_bot][1] - truth_result[i_frame][i_bot][1]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][0] - truth_result[i_frame][i_bot][2][0]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][1] - truth_result[i_frame][i_bot][2][1] > 0.1):
                        return False
                    if abs(result[i_frame][i_bot][3] - truth_result[i_frame][i_bot][3]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][4] - truth_result[i_frame][i_bot][4]) > 0.1:
                        return False
            return True


        result = self.vp.polar_kinematics(cart_kin, center)
        self.assertTrue(_is_equal(result, truth))

    def test_metric_constant(self):
        """
        Test *metric_constant* method
        """

        # assign

        truth = float(np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/metric_constant_truth.npy",
                        allow_pickle=True).tolist())

        # assert

        result = self.vp.metric_constant(3, (1, 0))
        self.assertAlmostEqual(result, truth)

    def test_load_p(self):
        """
        Test *load_p* method
        """

        # assign

        truth = np.load(os.path.dirname(__file__) + "/"
                        + "test_processing_files/cartesian_kinematics_truth.npy",
                        allow_pickle=True).tolist()

        #assert

        def _is_equal(result, truth_result):
            """
            Check equality of two Cartesian kinematics
            """

            if len(result) != len(truth_result):
                return False
            for i_frame in range(len(result)):
                if len(result[i_frame]) != len(truth_result[i_frame]):
                    return False
                for i_bot in range(len(result[i_frame])):
                    if result[i_frame][i_bot][0] != truth_result[i_frame][i_bot][0]:
                        return False
                    if abs(result[i_frame][i_bot][1] - truth_result[i_frame][i_bot][1]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][0] - truth_result[i_frame][i_bot][2][0]) > 0.1:
                        return False
                    if abs(result[i_frame][i_bot][2][1] - truth_result[i_frame][i_bot][2][1]) > 0.1:
                        return False
            return True

        result = self.vp.load_p(os.path.dirname(__file__) + "/"
                                + "test_processing_files/load_p.pickle")

        self.assertTrue(_is_equal(result, truth))

if __name__ == '__main__':
    unittest.main()
