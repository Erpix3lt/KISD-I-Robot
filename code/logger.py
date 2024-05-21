from PIL import Image
import cv2
import numpy as np
import time

class Logger():
  """
  A class for logging results along with associated images.
  """

  def __init__(self) -> None:
    pass
  
  def log(self, result, image: Image.Image):
    """
    Logs the result along with an associated image.

    Args:
        result: The result to be logged.
        image (Image.Image): The image associated with the result.
    """
    #print("[{}] RESULT: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), result))
    print("RESULT: ", result)
    cv2.imshow('IMAGE', np.array(image))
    cv2.waitKey(0)