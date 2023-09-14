"""
Module provides tests for the *ampy.animation*
"""

import os
import numpy as np

import unittest

import cv2

from ampy.animation import *
from ampy.utils import get_video

class TestAnimation(unittest.TestCase):
    """
    *TestAnimation* class provides tests for the *animation* mehods
    """

    def setUp(self) -> None:
        """
        Initialize objects for testing
        """

        self.filename = 'test_processing_files/test_video.mp4'

    def test_draw_markers(self):
        """
        Test *draw_markers* method
        """

        # assert
        
        try:
            video = get_video(self.filename, 0, 100, 5)
            markers = draw_markers(video)
        except:
            self.fail()

if __name__ == '__main__':
    unittest.main()
