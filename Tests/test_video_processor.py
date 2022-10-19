import unittest
from swarmtronics.video_processor import VideoProcessor
import cv2


class TestVideoProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.vp = VideoProcessor()

    def test_get_angle(self):
        # assign
        first_points = ((0, 0),
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        )
        second_points = ((1, 0),
                         (0, 1),
                         (-1, 0),
                         (0, -1),
                         (1, 1),
                         )
        results = (0,
                   90,
                   180,
                   -90,
                   45)

        # assert
        angle = self.vp._get_angle(first_points[0], second_points[0])
        self.assertAlmostEqual(angle, results[0], 2)
        angle = self.vp._get_angle(first_points[1], second_points[1])
        self.assertAlmostEqual(angle, results[1], 2)
        angle = self.vp._get_angle(first_points[2], second_points[2])
        self.assertAlmostEqual(angle, results[2], 2)
        angle = self.vp._get_angle(first_points[3], second_points[3])
        self.assertAlmostEqual(angle, results[3], 2)
        angle = self.vp._get_angle(first_points[4], second_points[4])
        self.assertAlmostEqual(angle, results[4], 2)

    def test_get_raw_cartesian_kinematics_from_frame(self):
        # assign
        # assert
        pass

if __name__ == '__main__':
    unittest.main()
