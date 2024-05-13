import torch
import cv2

class Detection_Service():
    
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
    
    def initialise_image(self, width=1000, height=650):
        img = cv2.imread('assets/2car.png')
        image = cv2.resize(img,(width, height))
        return image
        
    def analyse_image(self):
        image = self.initialise_image()
        result = self.model(image)
        print("RESULT: !!!!!!!!!", result)
        return result, image