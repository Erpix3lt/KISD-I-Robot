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

    # def test_get_image_from_url(self):
    #     image = self.stream_service.get_image_from_url()
    #     self.assertIsNotNone(image)
    #     image.show()
    
    # def test_apply_mask_to_image(self):
    #     image = self.stream_service.get_image_from_url()
    #     masked_image = self.stream_service.apply_mask_to_image(image)
    #     masked_image.show()
    #     self.assertIsNotNone(masked_image)
        
    def test_image_is_not_different(self):
        previous_image = self.stream_service.get_image_from_url()
        time.sleep(10)
        image = self.stream_service.get_image_from_url()
        previous_image = self.stream_service.apply_mask_to_image(previous_image)
        image = self.stream_service.apply_mask_to_image(image)

        is_different = self.stream_service.is_image_different(image, previous_image)
        print("IS DIFFERENT?", is_different)        
        image.show()
        previous_image.show()

if __name__ == '__main__':
    unittest.main()

