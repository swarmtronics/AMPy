import unittest
from amtoolkit.processing import Processor
import amtoolkit.statistics2d as tds
import numpy as np



class TestStatistics2D(unittest.TestCase):
    def setUp(self) -> None:
        self.vp = Processor()
        self.kinematics = np.load("test_statistics2d_files/test_kinematics.npy", allow_pickle=True).tolist()
        self.extended_kinematics = self.vp.polar_kinematics(self.kinematics, (0, 0))

    def test_calc_angle(self):
        self.assertEqual(tds.calc_angle((0, 1), (1, 0)), -45.0)

    def test_calc_distance(self):
        self.assertEqual(tds.calc_distance((0, 0), (1, 0)), 1.0)

    def test_mean_distance_from_center(self):
        #assign
        truth = np.load("test_statistics2d_files/mean_distance_from_center_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if abs(l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.mean_distance_from_center(self.extended_kinematics), truth))

    def test_mean_polar_angle(self):
        #assing
        truth = np.load("test_statistics2d_files/mean_polar_angle_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.mean_polar_angle(self.extended_kinematics), truth))

    def test_mean_polar_angle_absolute(self):
        # assing
        truth = np.load("test_statistics2d_files/mean_polar_angle_absolute_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.mean_polar_angle_absolute(self.extended_kinematics), truth))

    def test_mean_cartesian_displacements(self):
        #assign
        truth = np.load("test_statistics2d_files/mean_cartesian_displacements_truth.npy", allow_pickle=True).tolist()

        # assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.mean_cartesian_displacements(self.kinematics), truth))

    def test_bond_orientation(self):
        #assign
        truth = np.load("test_statistics2d_files/bond_orientation_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.bond_orientation(self.kinematics, 6, 6, 1), truth))

    def test_chi_4(self):
        #assign
        truth = float(np.load("test_statistics2d_files/chi_4_truth.npy", allow_pickle=True))

        #assert
        self.assertAlmostEqual(tds.chi_4(self.kinematics, 60, 100), truth)

    def test_cluster_dynamics(self):
        #assign
        truth = np.load("test_statistics2d_files/cluster_dynamics_truth.npy", allow_pickle=True).tolist()

        #assert
        def is_equal(l1, l2):
            if len(l1) != len(l2):
                return False
            for i in range(len(l1)):
                if (l1[i] - l2[i]) >= 0.001:
                    return False
            return True

        self.assertTrue(is_equal(tds.cluster_dynamics(self.kinematics), truth))


if __name__ == '__main__':
    unittest.main()
