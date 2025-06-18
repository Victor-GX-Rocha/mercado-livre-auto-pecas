""" Cloudinary Library Manager. """

import cloudinary
import cloudinary.uploader
import cloudinary.api

from typing import Any

from .converters import CloudinaryResponseConveretrs
from .models import CloudinaryResponse
# from ....core.log import logging
# from ....infrastructure.database.repositories import CloudinaryReposity


class CloudinaryManager:
    """ Cloudinary Operations Manager. """
    def __init__(self, cloud_name: str, api_key: str, api_secret: str) -> None:
        """
        Data to activate the library with an user account.
        Args:
            cloud_name (str): Cloud name.
            api_key (str): Credentail API key.
            api_secret (str): Credentail API secret.
        """
        self._configure(cloud_name, api_key, api_secret)
    
    def upload_image(self, image_path: str) -> CloudinaryResponse:
        """
        Upload a image to a Cloudinary account.
        Args:
            image_path: The path of the image that must be uploaded.
        Returns:
            CloudinaryResponse: 
        """
        try:
            response: dict[str, str | int] = cloudinary.uploader.upload(image_path)
            return CloudinaryResponse(
                success=True,
                data=CloudinaryResponseConveretrs.upload_image(response)
            )
        except Exception as e:
            return CloudinaryResponse(
                success=True,
                data=None,
                error=f"Erro inesperado durante o processo de upload de uma imagem no cloudinary: {image_path}. Exceção: {e}"
            )
    
    def delete_image(self, image_id: str) -> CloudinaryResponse: 
        """
        Delete a Cloudinary image.
        Args:
            image_id (str): Cloudinary image id.
        Returns:
            CloudinaryResponse: Response what contains if the requests works.
        """
        response: dict[str, str | Any] = cloudinary.uploader.destroy(image_id)
        if response.get("result", "").lower() != "ok":
            return CloudinaryResponse(
                success=False,
                data=None,
                error=response.get("result", "Mensagem de erro não retornada.")
            )
        return CloudinaryResponse(
            success=True,
            data=response.get("result")
        )
    
    def _configure(self, cloud_name: str, api_key: str, api_secret: str) -> None:
        """
        Configures the Cloudinary credentials and activate the library.
        Args:
            cloud_name (str): Cloud name.
            api_key (str): Credentail API key.
            api_secret (str): Credentail API secret.
        Raises:
            RuntimeError: If invalid credentails.
        """
        try:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao configurar Cloudinary: {e}")

# def validate_login_details(self) -> None:
#     """
#     Valida se os detalhes de login do Cloudinary estão completos.
    
#     Levanta uma exceção se alguma chave necessária estiver ausente.
#     """
#     try:
#         required_keys = ['cloud_name', 'api_key', 'api_secret']
#         for key in required_keys:
#             if key not in self.cloud_user:
#                 raise ValueError(f"Detalhes de login do Cloudinary incompletos. Chave '{key}' ausente.")
#     except ValueError as v:
#         logging.warning(f"{v}")

