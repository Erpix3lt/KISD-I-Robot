import unittest
import cv2
from detection_service import Detection_Service

class TestRobotService(unittest.TestCase):
    """
    This is a mockup test suite for the interface package. It will not 
    publish any MQTT messages.
    """
    def setUp(self):
      self.detection_service = Detection_Service()

    def test_object_detection(self):          
      result, image = self.detection_service.analyse_image()
      print('result: ', result)
    
      data_frame = result.pandas().xyxy[0]
      indexes = data_frame.index
      for index in indexes:
          # Find the coordinate of top left corner of bounding box
          x1 = int(data_frame['xmin'][index])
          y1 = int(data_frame['ymin'][index])
          # Find the coordinate of right bottom corner of bounding box
          x2 = int(data_frame['xmax'][index])
          y2 = int(data_frame['ymax'][index ])

          # Find label name
          label = data_frame['name'][index ]
          
          # Find confidence score of the model
          conf = data_frame['confidence'][index]
          text = label + ' ' + str(conf.round(decimals= 2))

          cv2.rectangle(image, (x1,y1), (x2,y2), (255,255,0), 2)
          cv2.putText(image, text, (x1,y1-5), cv2.FONT_HERSHEY_PLAIN, 2,
                      (255,255,0), 2)

      cv2.imshow('IMAGE', image)
      #PRESS ANY KEY IN THE IMAGE DISPLAY TO TERMINATE!
      cv2.waitKey(0)
      
if __name__ == '__main__':
    unittest.main()
