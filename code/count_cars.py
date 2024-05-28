from detection.detection_service import Detection_Service
from detection.image_service import Image_Service
from stream.stream_service import Stream_Service
from interface.robot_service import Robot_Service
from logger import Logger
from PIL import Image
import time

class Count_Cars():
    """
    A class for counting cars using opencv and machine learning.
    """

    def __init__(self) -> None:
        """
        Initializes the Count_Cars object.
        """
        self.mqtt = Robot_Service()
        self.mqtt.looking_idle(2)
        self.image_service = Image_Service()
        self.detection_service = Detection_Service(self.image_service)
        self.stream_service = Stream_Service()
        self.logger = Logger()
        self.image: Image.Image = None
        self.previous_image: Image.Image = None
        self.previous_result = None
      
    def count(self):
        """
        Check wether there is a change in the image retrieved, analyse the image
        and log the result.
        Terminate via ctrl + c.
        """
        try:
            while(True):
                self.image = self.stream_service.get_image_from_url()
                if self.image_service.is_image_different(self.image, self.previous_image):
                    result, analysed_image = self.detection_service.analyse_image(self.image)
                    car_count = self.detection_service.get_car_count_from_result(result, self.previous_result)
                    print("car count:", car_count)
                    self.mqtt.move_towards_count()
                    self.mqtt.count(car_count)
                self.mqtt.looking_idle(4)
                if result and self.image is not None:
                    self.previous_image = self.image
                    self.previous_result = result
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Exiting...")

count_Cars = Count_Cars()
count_Cars.count()
