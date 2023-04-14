"""
Module provides tests for the *ampy.processing*
"""

import os 

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

    def test_raw_cartesian_kinematics_from_frame(self):
        """
        Test working of video recognition
        """

        # assign
        data0 = (cv2.VideoCapture(os.path.dirname(__file__) + "/" + 'test_processing_files/image0.jpg')).read()[1]
        truth_result0 = [[18, 343.73979529168804, (802, 360)]]
        data1 = None
        truth_result1 = []
        data2 = (cv2.VideoCapture(os.path.dirname(__file__) + "/" + 'test_processing_files/image1.jpg')).read()[1]
        truth_result2 = [[2, 256.7594800848128, (1101, 172)], [4, 147.2647737278924, (761, 713)],
                   [5, 312.5104470780008, (1043, 240)], [7, 16.389540334034784, (1373, 755)],
                   [9, 280.00797980144137, (1282, 326)], [12, 180.0, (714, 544)],
                   [13, 162.6459753637387, (738, 403)], [20, 76.7594800848128, (1041, 869)],
                   [22, 26.56505117707799, (1206, 744)], [25, 75.96375653207353, (1103, 708)],
                   [26, 289.4400348281762, (936, 116)], [27, 173.29016319224309, (818, 581)],
                   [28, 289.4400348281762, (1180, 139)], [30, 194.93141717813754, (1034, 398)],
                   [31, 270.0, (1038, 137)], [32, 217.56859202882748, (889, 473)],
                   [39, 263.6598082540901, (918, 220)], [41, 149.03624346792648, (765, 782)],
                   [46, 255.96375653207352, (1044, 479)], [47, 13.240519915187205, (1368, 536)],
                   [50, 197.3540246362613, (789, 468)], [51, 310.23635830927384, (1208, 344)],
                   [52, 266.8201698801358, (979, 191)], [54, 222.51044707800082, (691, 459)],
                   [55, 249.44395478041653, (1171, 249)], [56, 120.96375653207352, (908, 696)],
                   [57, 262.8749836510982, (980, 458)], [58, 290.55604521958344, (851, 252)],
                   [59, 69.44395478041653, (1056, 766)], [60, 120.96375653207352, (852, 820)],
                   [62, 51.84277341263094, (1280, 706)], [65, 237.26477372789242, (979, 299)],
                   [66, 346.7594800848128, (1455, 467)], [68, 240.25511870305778, (948, 359)],
                   [69, 253.6104596659652, (1117, 277)], [70, 339.44395478041656, (1428, 406)],
                   [72, 283.2405199151872, (1059, 319)], [74, 236.30993247402023, (653, 351)],
                   [76, 324.4623222080256, (1229, 425)], [77, 73.61045966596522, (1153, 806)],
                   [78, 305.5376777919744, (884, 317)], [79, 266.6335393365702, (1231, 217)],
                   [80, 73.61045966596522, (987, 899)], [82, 59.03624346792648, (1111, 860)],
                   [83, 231.84277341263095, (903, 405)]]
        # assert

        def _is_equal(result, truth_result):
            """
            Check equality of two lists
            """

            if len(result) != len(truth_result):
                return False
            for i in range(len(result)):
                if result[i][0] != truth_result[i][0]:
                    return False
                if abs(result[i][1] - truth_result[i][1]) > 0.1:
                    return False
                if not (result[i][2][0] == truth_result[i][2][0]
                        and result[i][2][1] == truth_result[i][2][1]):
                    return False
            return True

        result0 = self.vp._raw_cartesian_kinematics_from_frame(data0, ignore_codes=())
        self.assertTrue(_is_equal(result0, truth_result0))
        result1 = self.vp._raw_cartesian_kinematics_from_frame(data1, ignore_codes=())
        self.assertTrue(_is_equal(result1, truth_result1))
        result2 = self.vp._raw_cartesian_kinematics_from_frame(data2, ignore_codes=())
        self.assertTrue(_is_equal(result2, truth_result2))


if __name__ == '__main__':
    unittest.main()
