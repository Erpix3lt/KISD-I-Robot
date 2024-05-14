from detection.detection_service import Detection_Service
from stream.stream_service import Stream_Service
from interface.robot_service import Robot_Service
from helpers import Helpers
import time

class Count_Cars():
  
  def __init__(self) -> None:
    self.detection_service = Detection_Service()
    self.stream_service = Stream_Service()
    self.robot_service = Robot_Service()
    self.helpers = Helpers()
    self.previous_image = None
    self.previous_result = None

  def count(self):
    try:
      while True:
        pil_image = self.stream_service.get_image_from_url()
        if self.previous_image is not None:
          if self.stream_service.is_image_different(pil_image, self.previous_image):
            masked_pil_image = self.stream_service.apply_mask_to_image(pil_image)
            result, analysed_image = self.detection_service.analyse_image(self.helpers.convert_pil_image_to_opencv_image(masked_pil_image))
            print("[{}] RESULT: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), result))
            self.helpers.draw_box_around_recognised_objects(analysed_image, result)
        elif self.previous_image is None:
          masked_pil_image = self.stream_service.apply_mask_to_image(pil_image)
          result, analysed_image = self.detection_service.analyse_image(self.helpers.convert_pil_image_to_opencv_image(masked_pil_image))
          print("[{}] RESULT: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), result))
          self.helpers.draw_box_around_recognised_objects(analysed_image, result)
        self.previous_image = pil_image
        self.previous_result = result
        time.sleep(5)
    except KeyboardInterrupt:
      print("Keyboard interrupt received. Exiting...")
      
count_Cars = Count_Cars()
count_Cars.count()
