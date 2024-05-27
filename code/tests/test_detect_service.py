import unittest
import cv2
import os
import sys
import time
import requests
from io import BytesIO
from PIL import Image
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
        
    def get_image_from_github_url(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print("Failed to retrieve the image")
            return None

    # def test_object_detection(self):   
    #     self.image = self.stream_service.get_image_from_url()
    #     result, analysed_image = self.detection_service.analyse_image(self.image)              
    #     self.assertIsNotNone(result)
    #     self.assertIsNotNone(analysed_image)
    #     self.logger.log(result, analysed_image)
        
    def test_get_car_count_from_result_is_0(self):
        self.image = self.get_image_from_github_url("https://raw.githubusercontent.com/Erpix3lt/KISD-I-Robot/main/assets/images/test_withCar.jpeg")
        result, analysed_image = self.detection_service.analyse_image(self.image) 
        self.logger.log(result, analysed_image)    
        ## DOUBLE THE ANALYSIS TO SIMULATE A PARKED, "STILL STANDING", CAR        
        previous_result, previous_analysed_image = self.detection_service.analyse_image(self.image)  
        self.logger.log(previous_result, previous_analysed_image)    
        total_car_count = self.detection_service.get_car_count_from_result(result, previous_result)
        print("TOTAL CAR COUNT: ",total_car_count)
        self.assertEqual(total_car_count, 0)
        
    def test_get_car_count_from_result_is_greater_0(self):
        self.image = self.get_image_from_github_url("https://raw.githubusercontent.com/Erpix3lt/KISD-I-Robot/main/assets/images/test_withCar.jpeg")
        result, analysed_image = self.detection_service.analyse_image(self.image) 
        self.logger.log(result, analysed_image)    
        ## DOUBLE THE ANALYSIS TO SIMULATE A PARKED, "STILL STANDING", CAR 
        self.image_two = self.stream_service.get_image_from_url()
        previous_result, previous_analysed_image = self.detection_service.analyse_image(self.image_two)  
        self.logger.log(previous_result, previous_analysed_image)    
        total_car_count = self.detection_service.get_car_count_from_result(result, previous_result)
        print("TOTAL CAR COUNT: ",total_car_count)
        self.assertGreater(total_car_count, 0)
    
if __name__ == '__main__':
    unittest.main()
