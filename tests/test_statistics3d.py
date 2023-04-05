import unittest
from amtoolkit.processing import Processor
import amtoolkit.statistics3d as tds
import numpy as np


class TestStatistics3D(unittest.TestCase):
    def setUp(self) -> None:
        self.vp = Processor()
        self.kinematics = np.load("test_statistics2d_files/test_kinematics.npy", allow_pickle=True).tolist()

    def test_position_correlation(self):
        # assign
        truth = np.load("test_statistics3d_files/position_correlation_truth.npy",
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

        self.assertTrue(is_equal(tds.position_correlation(self.kinematics, 200, 200), truth))

    def test_orientation_correlation(self):
        # assign
        truth = np.load("test_statistics3d_files/orientation_correlation_truth.npy",
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

        self.assertTrue(is_equal(tds.orientation_correlation(self.kinematics, 200, 200), truth))

    def test_velocity_correlation(self):
        # assign
        truth = np.load("test_statistics3d_files/velocity_correlation_truth.npy",
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

        self.assertTrue(is_equal(tds.velocity_correlation(self.kinematics, 200, 200), truth))


if __name__ == '__main__':
    unittest.main()
