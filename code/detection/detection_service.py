import torch
import cv2

class Detection_Service():
    
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
    
    def initialise_image(self, image, width=1000, height=650):
        image = cv2.resize(image,(width, height))
        return image
        
    def analyse_image(self, image):
        image = self.initialise_image(image)
        result = self.model(image)
        print("RESULT: !!!!!!!!!", result)
        return result, image