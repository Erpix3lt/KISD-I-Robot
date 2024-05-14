import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from typing import Optional

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

    def get_image_from_url(self, url: Optional[str] = None, is_cropped: bool = True) -> Optional[Image.Image]:
        """
        Fetches an image from the specified URL.

        Args:
            url (str, optional): The URL from which to fetch the image. If not provided,
                the default URL set in the environment variables will be used.
            is_cropped (bool): Flag indicating whether to crop the fetched image.

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