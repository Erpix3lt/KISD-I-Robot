import unittest
import os
import time
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stream.stream_service import Stream_Service

class TestStreamService(unittest.TestCase):
    """
    This tests the stream service with the default url and displays an image.
    """
    def setUp(self):
        self.stream_service = Stream_Service()

    def test_get_image_from_url(self):
        image = self.stream_service.get_image_from_url()
        self.assertIsNotNone(image)
        image.show()
    
   
if __name__ == '__main__':
    unittest.main()

