from PIL import Image
import cv2
import numpy as np

class Helpers:
  
    def __init__(self) -> None:
        pass
  
    def convert_pil_image_to_opencv_image(self, pil_image: Image.Image) -> np.ndarray:
        numpy_image = np.array(pil_image)
        return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    def draw_box_around_recognised_objects(self, image, result):
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

            cv2.rectangle(image, (x1,y1), (x2,y2), (255,255,0), 2)
            cv2.putText(image, text, (x1,y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)

        cv2.imshow('IMAGE', image)
        cv2.waitKey(0)