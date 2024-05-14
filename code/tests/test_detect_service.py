import unittest
import cv2
import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from detection.detection_service import Detection_Service
from detection.image_service import Image_Service
from stream.stream_service import Stream_Service

from logger import Logger

class TestRobotService(unittest.TestCase):
    """
    This is a mockup test suite for the interface package. It will not 
    publish any MQTT messages.
    """
    def setUp(self):
        self.image_service = Image_Service()
        self.stream_service = Stream_Service()
        self.detection_service = Detection_Service(self.image_service)
        self.logger = Logger()

    def test_object_detection(self):   
        self.image = self.stream_service.get_image_from_url()
        result, analysed_image = self.detection_service.analyse_image(self.image)              
        # Assert that result and image are not None
        self.assertIsNotNone(result)
        self.assertIsNotNone(analysed_image)
        
        self.logger.log(result, analysed_image)
    
if __name__ == '__main__':
    unittest.main()
