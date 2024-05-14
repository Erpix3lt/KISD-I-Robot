from skimage.metrics import structural_similarity
import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

class Stream_Service:
    """
    A class for fetching and processing images from a URL.

    Attributes:
        default_url (str): The default URL used for fetching images.
    """

    def __init__(self) -> None:
        """
        Initializes a Stream_Service instance.

        The constructor loads the environment variables using dotenv and sets the default URL
        for fetching images.
        """
        load_dotenv()
        self.crop_margin_top = 30
        self.default_url = os.getenv("DEFAULT_STREAM_URL")

    def get_image_from_url(self, url=None, is_cropped=True):
        """
        Fetches an image from the specified URL.

        Args:
            url (str, optional): The URL from which to fetch the image. If not provided,
                the default URL set in the environment variables will be used.

        Returns:
            PIL.Image.Image or None: The fetched image as a PIL.Image.Image object if successful,
                None otherwise.
        """
        if url is None:
            url = self.default_url
        try:
            response = requests.get(url)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                if is_cropped:
                    width, height = image.size
                    left = 0
                    top = self.crop_margin_top
                    right = width
                    bottom = height

                    # Cropped image
                    image = image.crop((left, top, right, bottom))
                return image
            else:
                print("Failed to fetch image. Status code:", response.status_code)
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def is_image_different(self, image, previous_image):
        """
        Compare two PIL Image objects and return True if they are different from one another.

        Args:
            image (PIL.Image.Image): First PIL Image object.
            previous_image (PIL.Image.Image): Second PIL Image object.

        Returns:
            bool: True if the images are different, False otherwise.
        """
        # Convert PIL images to numpy arrays
        np_image = np.array(image)
        np_previous_image = np.array(previous_image)

        # Convert images to grayscale
        gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        gray_previous_image = cv2.cvtColor(np_previous_image, cv2.COLOR_RGB2GRAY)

        # Compute SSIM between the two images
        score, _ = structural_similarity(gray_image, gray_previous_image, full=True)

        # Set a threshold for significant change
        threshold = 0.9  # Adjust as needed
        
        # If SSIM score is less than threshold, consider it as a significant change
        if score < threshold:
            return True
        else:
            return False
