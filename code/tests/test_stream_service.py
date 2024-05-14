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
        # Initialize the Stream_Service instance
        self.stream_service = Stream_Service()

    # def test_get_image_from_url(self):
    #     # Test with a valid URL
    #     image = self.stream_service.get_image_from_url()
        
    #     # Check if something was returned
    #     self.assertIsNotNone(image)

    #     # Display the image (optional)
    #     image.show()
        
    def test_image_is_not_different(self):
        previous_image = self.stream_service.get_image_from_url()
        image = self.stream_service.get_image_from_url()
        
        is_different = self.stream_service.is_image_different(image, previous_image)
        
        self.assertIs(is_different, False)
        
        image.show()
        
        previous_image.show()
        
        image.save("current_image.png")
        previous_image.save("previous_image.png")
        
    def test_image_is_different(self):
        previous_image = self.stream_service.get_image_from_url()
        time.sleep(30)
        image = self.stream_service.get_image_from_url()
        
        is_different = self.stream_service.is_image_different(image, previous_image)
        
        self.assertIs(is_different, True)
        
        image.show()
        
        previous_image.show()
        
        image.save("current_image.png")
        previous_image.save("previous_image.png")



if __name__ == '__main__':
    unittest.main()

