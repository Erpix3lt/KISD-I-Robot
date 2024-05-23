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
        crop_margin_top (int): The top margin to use when cropping images.
    """

    def __init__(self) -> None:
        """
        Initializes a Stream_Service instance.

        The constructor loads the environment variables using dotenv and sets the default URL
        for fetching images.
        """
        load_dotenv()
        self.crop_margin_top: int = int(os.getenv("IMAGE_CROP_MARGIN_TOP", 0))
        self.default_url: str = os.getenv("DEFAULT_STREAM_URL", "http://192.168.0.52/")

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
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                byte_array = bytes()

                for chunk in response.iter_content(chunk_size=1024):
                    byte_array += chunk
                    start = byte_array.find(b'\xff\xd8')
                    end = byte_array.find(b'\xff\xd9')

                    if start != -1 and end != -1:
                        jpg = byte_array[start:end+2]
                        byte_array = byte_array[end+2:]

                        image = Image.open(BytesIO(jpg))
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

# Example usage
if __name__ == "__main__":
    stream_service = Stream_Service()
    image = stream_service.get_image_from_url()
    if image:
        image.show()  # Display the image
        # image.save("fetched_image.jpg")  # Save the image if needed
