from skimage.metrics import structural_similarity
import cv2
import numpy as np
from PIL import Image
import os
from dotenv import load_dotenv

class Image_Service:
  
  def __init__(self) -> None:
    load_dotenv() 
    self.similarity: float = float(os.getenv("IMAGE_COMPARE_SIMILARITY"))
  
  def apply_mask_to_image(self, image: Image.Image, mask_image_path:str = 'code/detection/assets/street-mask.png') -> Image.Image:
      """
      Apply a mask via path to an image.

      Args:
          image (PIL.Image.Image): PIL Image object.
          mask_image_path (str): Path to the mask.

      Returns:
          PIL.Image.Image or None: The masked PIL.Image.Image object if successful,
          None otherwise.
      """
      try:
          mask_image = Image.open(mask_image_path).convert("L")  # Convert to grayscale
          return Image.composite(image, Image.new('RGB', image.size, 'white'), mask_image)
      except Exception as e:
          print("An error occurred while applying mask:", e)
          return None

  def is_image_different(self, image: Image.Image, previous_image: Image.Image, compare_with_mask:bool = True) -> bool:
    """
    Compare two PIL Image objects and return True if they are different from one another.

    Args:
        image (PIL.Image.Image): First PIL Image object.
        previous_image (PIL.Image.Image): Second PIL Image object.

    Returns:
        bool: True if the images are different, False otherwise.
    """
    if previous_image is not None:
        if compare_with_mask:
            image = self.apply_mask_to_image(image)
            previous_image = self.apply_mask_to_image(previous_image)
        
        np_image = np.array(image)
        np_previous_image = np.array(previous_image)

        gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        gray_previous_image = cv2.cvtColor(np_previous_image, cv2.COLOR_RGB2GRAY)

        score, _ = structural_similarity(gray_image, gray_previous_image, full=True)
        if score < self.similarity:
            return True
        else:
            return False
    else: 
        print("*WARN* Previous image was none.")
        return False
    