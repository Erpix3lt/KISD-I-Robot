import torch
import cv2
from PIL import Image
import numpy as np
import time

class Detection_Service:
    """
    A service for object detection using YOLOv5 model.

    Attributes:
    - model: YOLOv5 object detection model.
    """

    def __init__(self, _image_service):
        """
        Initializes the Detection_Service object.

        This method loads the YOLOv5 model using torch.hub.load() from the ultralytics/yolov5 repository.
        """
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
        self.image_service = _image_service
    
    def initialise_image(self, image: Image.Image, analyse_with_mask:bool)-> np.ndarray:
        """
        Resizes the input image to a specified width and height.

        Args:
        - image: Input image to be resized.
        - width: Desired width of the resized image (default is 1000).
        - height: Desired height of the resized image (default is 650).

        Returns:
        Resized image.
        """
        if analyse_with_mask:
            return np.array(self.image_service.apply_mask_to_image(image))
        else:
            return np.array(image)
    
    def finalize_image(self, image: Image.Image, result, add_timestamp: bool = False) -> Image.Image:
        """
       Finalize the image. If true draw a timestamp. Draws boxes and percentage around objects found.

        Args:
        - image: Input image to be resized.
        - result: Result
        - add_timestamp: Check wether to draw timestamp

        Returns:
        Finalized Image
        """
        np_image = np.array(image)
        
        if add_timestamp:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(np_image, timestamp, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        data_frame = result.pandas().xyxy[0]
        indexes = data_frame.index
        for index in indexes:
            # Find the coordinate of top left corner of bounding box
            x1 = int(data_frame['xmin'][index])
            y1 = int(data_frame['ymin'][index])
            # Find the coordinate of right bottom corner of bounding box
            x2 = int(data_frame['xmax'][index])
            y2 = int(data_frame['ymax'][index])

            # Find label name
            label = data_frame['name'][index]
            
            # Find confidence score of the model
            conf = data_frame['confidence'][index]
            text = label + ' ' + str(conf.round(decimals=2))

            cv2.rectangle(np_image, (x1,y1), (x2,y2), (255,255,0), 2)
            cv2.putText(np_image, text, (x1,y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)
        return Image.fromarray(np_image)
        
    def analyse_image(self, image: Image.Image, analyse_with_mask:bool = True):
        """
        Performs object detection on the input image using the initialized YOLOv5 model.

        Args:
        - image: Input image for object detection.

        Returns:
        A tuple containing:
        - result: Detection result returned by the YOLOv5 model.
        - image: Input image with bounding boxes drawn around detected objects.
        """
        result = self.model(self.initialise_image(image, analyse_with_mask))
        return result, self.finalize_image(image, result)
    
    def get_car_count_from_result(self, result, previous_result, threshold=5):
        """
        Counts the total number of cars found in the detection result, excluding those
        already detected in the previous result within a given threshold.

        Args:
        - result: Detection result returned by the YOLOv5 model.
        - previous_result: Detection result from the previous frame.
        - threshold: Pixel threshold to determine if a car has already been detected.

        Returns:
        Total number of newly detected cars.
        """
        car_count = 0
        current_cars = result.pandas().xyxy[0]
        previous_cars = previous_result.pandas().xyxy[0] if previous_result is not None else None

        def is_similar(car1, car2, threshold):
            """Check if two cars are within a certain threshold of each other."""
            return (abs(car1['xmin'] - car2['xmin']) < threshold and
                    abs(car1['ymin'] - car2['ymin']) < threshold and
                    abs(car1['xmax'] - car2['xmax']) < threshold and
                    abs(car1['ymax'] - car2['ymax']) < threshold)

        for _, current_car in current_cars.iterrows():
            if current_car['name'] == 'car':
                already_counted = False
                if previous_cars is not None:
                    for _, previous_car in previous_cars.iterrows():
                        if previous_car['name'] == 'car' and is_similar(current_car, previous_car, threshold):
                            already_counted = True
                            break
                if not already_counted:
                    car_count += 1
        
        return car_count