""" Manage the creation of a mercado libre images IDs """

import os

from src.core import log
from src.infra.db.models.produtos import Product
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.images import MeliImageManager
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.api.cloudinary.manager import CloudinaryManager
from src.app.shared.image_normalizer import ImageNormalizer
from .url_generators import UrlGeneratorFactory 
from .models import PicturesGeneratorResponse
from .corrector import CorretImageProperties
from .url_generators.interface import (
    IImageUploader,
    UrlGeneratorResponse
)


class PicturesGenerator:
    """ Manages the generation of the product meli picutures IDs. """
    def __init__(self):
        self.url_generator: IImageUploader = UrlGeneratorFactory.chose("cloudinary")
        self.image_normalizer = ImageNormalizer
        self.correct_image = CorretImageProperties()
        self.meli_image_manager = MeliImageManager()
    
    def generate(self, product: Product, token: AuthResponse) -> PicturesGeneratorResponse:
        """
        Generate a list of meli picutures IDs.
        Args:
            product (Product): 
            token (AuthResponse): Meli token for upload url request.
        Returns:
            PicturesGeneratorResponse: List with the meli pictures IDs.
        """
        try:
            
            image_paths: list[str] = self.image_normalizer.correct_format(product.sale.imagens)
            if not image_paths:
                return PicturesGeneratorResponse(
                    success=False,
                    result=None,
                    error=f'Coluna "imagens" possui conteúdo em formato inadequado: {image_paths}'
                )
            
            url_response = self.__create_urls(image_paths)
            if not url_response.success:
                return url_response
            
            return self.__create_meli_ids(url_response.result, token)
            
        except Exception as e:
            log.dev.exception(e)
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f"Erro inesperado durante o processo de criação dos IDs de imagem do mercado livre: {e}"
            )
    
    def __create_urls(self, images_paths: list[str]) -> PicturesGeneratorResponse:
        """
        Upload a list of images on a online repositorie.
        Args:
            images_paths (list[str]): Images paths to upload.
        Returns:
            PicturesGeneratorResponse A list with the images URLs.
        """
        urls: list[UrlGeneratorResponse] = []
        failed_urls: list[str] = []
        
        for img in images_paths:
            temp_image = self.correct_image.corret(img)
            url_response = self.__upload_image(temp_image)
            if not url_response.success:
                failed_urls.append(f"Imagem: {img}, causa: {url_response.error}")
            urls.append(url_response)
            os.remove(temp_image) # Removes the temp image.
        
        if failed_urls:
            log.user.warning(f"Falha ao gerar uma url para a imagem: {failed_urls}")
        
        if not urls:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f'Nenhuma das imagens da coluna "imagens" gerou uma URL válida: {images_paths}'
            )
        
        return PicturesGeneratorResponse(
            success=True,
            result=urls,
            error=None
        )
    
    def __upload_image(self, image_path: str) -> UrlGeneratorResponse:
        """
        Upload an image to a online repositorie and returns the image link.
        Args:
            image_path (str): Image path.
        Returns:
            (UrlGeneratorResponse): Response what contains the content of the upload (image url).
        """
        return self.url_generator.upload_image(image_path)

    
    def __create_meli_ids(self, urls: list[UrlGeneratorResponse], token: AuthResponse) -> PicturesGeneratorResponse:
        """
        Upload a list of URLs to mercado libre and create the meli image IDs.
        Args:
            urls (list[UrlGeneratorResponse]): List with the UrlGeneratorResponse what contains the images urls.
        Returns:
            PicturesGeneratorResponse: Mercado libre response with IDs.
        """
        failed_pictures_ids: list[str] = []
        meli_pictures_ids: list[str] = []
        
        for url in urls:
            meli_picture_id = self.__upload_url(url.data.url, token)
            if not meli_picture_id.success:
                failed_pictures_ids.append(f"url: {url.data.url}, causa: {meli_picture_id.error.message}")
            meli_pictures_ids.append({"id": meli_picture_id.result.get("id")}) # Gets the meli image id
            self.url_generator.delete_image(url.data.id) # Removes the online image from account
            
        if failed_pictures_ids:
            log.user.warning(f"Falha ao gerar um ID para a url: {failed_pictures_ids}")
        
        if not meli_pictures_ids:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f'Nenhuma das imagens da coluna "imagens" gerou um ID de imagem do mercado livre válida. Causas: {failed_pictures_ids}'
            )
        
        return PicturesGeneratorResponse(
            success=True,
            result=meli_pictures_ids
        )
    
    def __upload_url(self, url: str, token: AuthResponse) -> PicturesGeneratorResponse:
        """
        Returns a MeliResponse with the mercado libre picture data.
        Args:
            url (str): Image url.
            token (AuthResponse): Meli token for upload url request.
        Returns:
            MeliResponse: Response with the IDs content.
        """
        meli_id_response = self.meli_image_manager.get_meli_picture(image_url=url, access_token=token.access_token)
        
        if not meli_id_response.success:
            log.user.error(f"{meli_id_response.error.message}. Exception: {meli_id_response.error.exception}")
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=meli_id_response.error
            )
        
        return PicturesGeneratorResponse(
            success=True,
            result=meli_id_response.data
        )
