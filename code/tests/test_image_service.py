import unittest
import cv2
import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from detection.image_service import Image_Service
from stream.stream_service import Stream_Service

class TestRobotService(unittest.TestCase):
    """
    This is a mockup test suite for the interface package. It will not 
    publish any MQTT messages.
    """
    def setUp(self):
        self.image_service = Image_Service()
        self.stream_service = Stream_Service()
        
    def test_apply_mask_to_image(self):
        image = self.stream_service.get_image_from_url()
        masked_image = self.image_service.apply_mask_to_image(image)
        masked_image.show()
        self.assertIsNotNone(masked_image)
        
    def test_image_is_not_different(self):
        previous_image = self.stream_service.get_image_from_url()
        time.sleep(10)
        image = self.stream_service.get_image_from_url()
        is_different = self.image_service.is_image_different(image, previous_image)
        print("IS DIFFERENT?", is_different)        
        image.show()
        previous_image.show()

if __name__ == '__main__':
    unittest.main()
