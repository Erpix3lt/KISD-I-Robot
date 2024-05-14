from detection.detection_service import Detection_Service
from stream.stream_service import Stream_Service
from interface.robot_service import Robot_Service
import time
class Count_Cars():
  
  def __init__(self) -> None:
    self.detection_service = Detection_Service()
    self.stream_service = Stream_Service()
    self.robot_service = Robot_Service()
    self.previous_image = None
    self.previous_result = None
    
  def count(self):
    while True:
      image = self.stream_service.get_image_from_url()
      #TODO translate image to opencv capable image object
      result, analysed_image = self.detection_service.analyse_image(image)
      if self.detection_service.has_new_object(analysed_image, self.previous_image):
        if self.detection_service.get_moving_objects(result, self.previous_result):
          self.robot_service.move_pos('1')
        else:
          self.robot_service.move_pos('2')
      else:
        self.robot_service.move_pos('2')
      self.previous_image = analysed_image
      self.previous_result = result
      time.sleep(1)
      
  
  
  