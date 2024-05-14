from PIL import Image
import cv2
import numpy as np

class Helpers:
  
    def __init__(self) -> None:
        pass
  
    def convert_pil_image_to_opencv_image(self, pil_image: Image.Image) -> np.ndarray:
        numpy_image = np.array(pil_image)
        return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
