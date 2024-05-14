import torch
import cv2

class Detection_Service:
    """
    A service for object detection using YOLOv5 model.

    Attributes:
    - model: YOLOv5 object detection model.
    """

    def __init__(self):
        """
        Initializes the Detection_Service object.

        This method loads the YOLOv5 model using torch.hub.load() from the ultralytics/yolov5 repository.
        """
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
    
    def initialise_image(self, image, width=1000, height=650):
        """
        Resizes the input image to a specified width and height.

        Args:
        - image: Input image to be resized.
        - width: Desired width of the resized image (default is 1000).
        - height: Desired height of the resized image (default is 650).

        Returns:
        Resized image.
        """
        image = cv2.resize(image, (width, height))
        return image
        
    def analyse_image(self, image):
        """
        Performs object detection on the input image using the initialized YOLOv5 model.

        Args:
        - image: Input image for object detection.

        Returns:
        A tuple containing:
        - result: Detection result returned by the YOLOv5 model.
        - image: Input image with bounding boxes drawn around detected objects.
        """
        image = self.initialise_image(image)
        result = self.model(image)
        return result, image

    def has_moving_object(self, image, previous_image):
        # Compare two images using opencv 
        # Check wether the "newer" image is different from the "older" one
        return True
    
    def get_moving_objects(self, result, previous_result):
        # Compare the two analysed results of the image 
        # Implement logic to check wether an image has n moving cars
        # create a new result object containing the list of moving objects and their positions
        return True