import unittest
from swarmtronics.video_processor import VideoProcessor
import swarmtronics.three_dimensional_statistics as tds
import numpy as np


class TestThreeDimensionalStatistics(unittest.TestCase):
    def setUp(self) -> None:
        self.vp = VideoProcessor()
        self.kinematics = np.load("test_two_dimensional_statistics_files/test_kinematics.npy", allow_pickle=True).tolist()

    def test_get_position_correlation(self):
        # assign
        truth = np.load("test_three_dimensional_statistics_files/get_position_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m1, m2):
            if len(m1) != len(m2):
                return False
            if len(m1[0]) != len(m2[0]):
                return False
            if len(m1[0][0]) != len(m2[0][0]):
                return False
            for k in range(len(m1)):
                for i in range(len(m1[0])):
                    for j in range(len(m1[0][0])):
                        if abs(m1[k][i][j] - m2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.get_position_correlation(self.kinematics, 200, 200), truth))

    def test_get_orientation_correlation(self):
        # assign
        truth = np.load("test_three_dimensional_statistics_files/get_orientation_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m1, m2):
            if len(m1) != len(m2):
                return False
            if len(m1[0]) != len(m2[0]):
                return False
            if len(m1[0][0]) != len(m2[0][0]):
                return False
            for k in range(len(m1)):
                for i in range(len(m1[0])):
                    for j in range(len(m1[0][0])):
                        if abs(m1[k][i][j] - m2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.get_orientation_correlation(self.kinematics, 200, 200), truth))

    def test_get_velocity_correlation(self):
        # assign
        truth = np.load("test_three_dimensional_statistics_files/get_velocity_correlation_truth.npy",
                        allow_pickle=True).tolist()

        # assert
        def is_equal(m1, m2):
            if len(m1) != len(m2):
                return False
            if len(m1[0]) != len(m2[0]):
                return False
            if len(m1[0][0]) != len(m2[0][0]):
                return False
            for k in range(len(m1)):
                for i in range(len(m1[0])):
                    for j in range(len(m1[0][0])):
                        if abs(m1[k][i][j] - m2[k][i][j]) >= 0.001:
                            return False
            return True

        self.assertTrue(is_equal(tds.get_velocity_correlation(self.kinematics, 200, 200), truth))


if __name__ == '__main__':
    unittest.main()
