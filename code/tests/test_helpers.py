import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import Helpers
from stream.stream_service import Stream_Service
from detection.detection_service import Detection_Service

class TestStreamService(unittest.TestCase):
    """
    This tests the helper.
    """
    def setUp(self):
        # Initialize the Stream_Service instance
        self.helpers = Helpers()
        self.stream_service = Stream_Service()
        self.detection_service = Detection_Service()

    def test_convert_pil_image_to_opencv_image(self):
        pil_image = self.stream_service.get_image_from_url()
        image = self.helpers.convert_pil_image_to_opencv_image(pil_image)
        result = self.detection_service.analyse_image(image)

        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
