""" Response interface for image uploaders. """

from abc import ABC, abstractmethod
from dataclasses import dataclass


# Data models
@dataclass
class UrlGeneratorError:
    cause: str
    provider: str 
    operation: str 

@dataclass
class UrlGeneratorContent:
    id: str
    url: str

@dataclass
class UrlGeneratorResponse:
    success: bool
    data: UrlGeneratorContent | None
    error: UrlGeneratorError | None


# Protocol
class IImageUploader(ABC):
    @abstractmethod
    def upload_image(self, image_path: str) -> UrlGeneratorResponse:
        """
        Upload an image to a online repositorie and returns the image url and id.
        Args:
            image_path: The path of the image that must be uploaded.
        Returns:
            UrlGeneratorResponse: The url and id generated after the upload.
        """
        pass
    
    @abstractmethod
    def delete_image(self, image_id: str) -> UrlGeneratorResponse:
        """
        Delete a uploaded image.
        Args:
            image_id (str): Uploaded image id.
        Returns:
            UrlGeneratorResponse: Success True if it works else False.
        """
        pass
