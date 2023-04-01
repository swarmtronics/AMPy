import unittest
from swarmtronics.video_processor import VideoProcessor
import swarmtronics.two_dimensional_statistics as tds
import numpy as np



class TestTwoDimensionalStatistics(unittest.TestCase):
    def setUp(self) -> None:
        self.vp = VideoProcessor()
        self.kinematics = np.load("test_two_dimensional_statistics_files/test_kinematics.npy", allow_pickle=True).tolist()
        self.extended_kinematics = self.vp.extend_kinematics(self.kinematics, (0, 0))

    def test_calculate_angle(self):
        self.assertEqual(tds.calculate_angle((0,1), (1,0)), -45.0)

    def test_get_distance(self):
        self.assertEqual(tds.get_distance((0, 0), (1, 0)), 1.0)

    def test_get_mean_distance_from_center(self):
        #assign
        truth = np.load("test_two_dimensional_statistics_files/get_mean_distance_from_center_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if abs(l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_mean_distance_from_center(self.extended_kinematics), truth))

    def test_get_mean_polar_angle(self):
        #assing
        truth = np.load("test_two_dimensional_statistics_files/get_mean_polar_angle_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_mean_polar_angle(self.extended_kinematics), truth))

    def test_get_mean_polar_angle_absolute(self):
        # assing
        truth = np.load("test_two_dimensional_statistics_files/get_mean_polar_angle_absolute_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_mean_polar_angle_absolute(self.extended_kinematics), truth))

    def test_get_mean_cartesian_displacements(self):
        #assign
        truth = np.load("test_two_dimensional_statistics_files/get_mean_cartesian_displacements_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_mean_cartesian_displacements(self.kinematics), truth))

    def test_get_bond_orientation(self):
        #assign
        truth = np.load("test_two_dimensional_statistics_files/get_bond_orientation_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_bond_orientation(self.kinematics, 6, 6, 1), truth))

    def test_get_chi_4(self):
        #assign
        truth = float(np.load("test_two_dimensional_statistics_files/get_chi_4_truth.npy", allow_pickle=True))

        #assert
        self.assertAlmostEqual(tds.get_chi_4(60, 100, self.kinematics), truth)

    def test_get_cluster_dynamics(self):
        #assign
        truth = np.load("test_two_dimensional_statistics_files/get_cluster_dynamics_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.get_cluster_dynamics(self.kinematics), truth))


if __name__ == '__main__':
    unittest.main()
