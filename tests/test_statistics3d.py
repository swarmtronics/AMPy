"""
Module provides tests for the *amtoolkit.statistics3d*
"""
import os 

import unittest

import numpy as np

from amtoolkit.processing import Processor
import amtoolkit.statistics3d as tds


class TestStatistics3D(unittest.TestCase):
    """
    *TestStatistics3D* class provides tests for the *amtoolkit.statistics2d* module
    """

    def setUp(self) -> None:
        """
        Initialize objects for testing
        """

        self.vp = Processor()
        self.kinematics = \
            np.load(os.path.dirname(__file__) + "/test_statistics2d_files/test_kinematics.npy", allow_pickle=True).tolist()

    def test_position_correlation(self):
        """
        Test *amtoolkit.statistics3d.position_correlation* function
        """

        # assign
        truth = np.load("test_statistics3d_files/position_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m_1, m_2):
            """
            Check equality of two matrices
            """

            if len(m_1) != len(m_2):
                return False
            if len(m_1[0]) != len(m_2[0]):
                return False
            if len(m_1[0][0]) != len(m_2[0][0]):
                return False
            for k in range(len(m_1)):
                for i in range(len(m_1[0])):
                    for j in range(len(m_1[0][0])):
                        if abs(m_1[k][i][j] - m_2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.position_correlation(self.kinematics, 200, 200), truth))

    def test_orientation_correlation(self):
        """
        Test *amtoolkit.statistics3d.orientation_correlation* function
        """

        # assign
        truth = np.load("test_statistics3d_files/orientation_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m_1, m_2):
            """
            Check equality of two matrices
            """

            if len(m_1) != len(m_2):
                return False
            if len(m_1[0]) != len(m_2[0]):
                return False
            if len(m_1[0][0]) != len(m_2[0][0]):
                return False
            for k in range(len(m_1)):
                for i in range(len(m_1[0])):
                    for j in range(len(m_1[0][0])):
                        if abs(m_1[k][i][j] - m_2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.orientation_correlation(self.kinematics, 200, 200), truth))

    def test_velocity_correlation(self):
        """
        Test *amtoolkit.statistics3d.velocity_correlation* function
        """

        # assign
        truth = np.load("test_statistics3d_files/velocity_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m_1, m_2):
            """
            Check equality of two matrices
            """

            if len(m_1) != len(m_2):
                return False
            if len(m_1[0]) != len(m_2[0]):
                return False
            if len(m_1[0][0]) != len(m_2[0][0]):
                return False
            for k in range(len(m_1)):
                for i in range(len(m_1[0])):
                    for j in range(len(m_1[0][0])):
                        if abs(m_1[k][i][j] - m_2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.velocity_correlation(self.kinematics, 200, 200), truth))


if __name__ == '__main__':
    unittest.main()
