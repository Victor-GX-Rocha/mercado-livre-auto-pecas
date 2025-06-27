""" Cloudinary interface adapter. """

from src.config import AppConfigManager
from src.infra.db.repo import CloudinaryRepository
from src.infra.api.cloudinary import CloudinaryManager
from .interface import (
    IImageUploader, 
    UrlGeneratorResponse, 
    UrlGeneratorContent, 
    UrlGeneratorError
)


class CloudinaryImageUploader(CloudinaryManager, IImageUploader):
    """ Interface to clouadinary responses. """
    def __init__(self):
        app_config = AppConfigManager()
        cloud_user = app_config.get_cloud_user_name()
        cloud_repo = CloudinaryRepository()
        
        user = cloud_repo.get.user(cloud_user)[0]
        
        if not all([user.cloud_name, user.api_key, user.api_secret]):
            raise ValueError(f"Dados de credencial do cloudinary ausentes! {user}")
        
        super().__init__(
            cloud_name=user.cloud_name,
            api_key=user.api_key,
            api_secret=user.api_secret
        )
    
    def upload_image(self, image_path: str) -> UrlGeneratorResponse:
        """
        Upload a image to a Cloudinary account.
        Args:
            image_path: The path of the image that must be uploaded.
        Returns:
            UrlGeneratorResponse:
        """
        response = super().upload_image(image_path)
        if not response.success:
            return UrlGeneratorResponse(
                success=False,
                data=None,
                error=UrlGeneratorError(
                    cause=response.error,
                    provider="cloudinary",
                    operation="delete"
                )
            )
        
        if not hasattr(response.data, 'public_id') or not hasattr(response.data, 'secure_url'):
            return UrlGeneratorResponse(
                success=False,
                data=None,
                error=UrlGeneratorError(cause="Resposta inválida do Cloudinary")
            )
        
        return UrlGeneratorResponse(
                success=True,
                data=UrlGeneratorContent(
                    id=response.data.public_id,
                    url=response.data.secure_url
                ),
                error=None
            )
    
    def delete_image(self, image_id: str) -> UrlGeneratorResponse:
        """
        Delete a Cloudinary image.
        Args:
            image_id (str): Cloudinary image id.
        Returns:
            UrlGeneratorResponse: Success true if it works.
        """
        response = super().delete_image(image_id)
        if not response.success:
            return UrlGeneratorResponse(
                success=False,
                data=None,
                error=UrlGeneratorError(
                    cause=response.error
                )
            )
        return UrlGeneratorResponse(
            success=True,
            data=None,
            error=None
        )
