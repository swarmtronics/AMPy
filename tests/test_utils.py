"""
Module provides tests for the *ampy.utils*
"""

import os
import numpy as np

import unittest

import cv2

from ampy.utils import *


class TestUtils(unittest.TestCase):
    """
    *TestUtils* class provides tests for the *utils* methods
    """

    def setUp(self) -> None:
        """
        Initialize objects for testing
        """
        
        self.filename = 'test_processing_files/test_video.mp4'
                
    def test_get_video(self):
        """
        Test *get_video* method
        """

        # assert
        
        try:
            video_original = get_video(self.filename, 0, 125, 10)
        except:
            self.fail()
            
    def test_save_video(self):
        """
        Test *save_video* method
        """
                   
        # assert
        
        try:
            save_video('test_video_saved.mp4',  np.uint8(np.random.rand(100, 1080, 1920, 3)*255))
        except:
            self.fail()
            
if __name__ == '__main__':
    unittest.main()
