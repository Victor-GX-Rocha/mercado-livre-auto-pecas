""" Manage the creation of a mercado libre images IDs """

import os

from ......core.log import logging
from ......infrastructure.database.models.produtos import Product
from ......infrastructure.api.mercadolivre.auth import AuthResponse
from ......infrastructure.api.mercadolivre.images import MeliImageManager
from ......infrastructure.api.mercadolivre.models import MeliResponse
from ......infrastructure.api.cloudinary.cloud import CloudinaryManager
from .....shared.image_normalizer import ImageNormalizer
from .models import PicturesGeneratorResponse
from .corrector import CorretImageDimentions
# from .generator import 

from dataclasses import dataclass

@dataclass
class UrlGeneratorError:
    cause: str

@dataclass
class UrlGeneratorContent:
    id: str
    url: str

@dataclass
class UrlGeneratorResponse:
    success: bool
    error: str | None
    data: UrlGeneratorContent | None


class PicturesGenerator:
    def __init__(self):
        self.url_generator = CloudinaryManager() # Needs an activation!
        self.image_normalizer = ImageNormalizer
        self.correct_image = CorretImageDimentions()
        self.meli_image_manager = MeliImageManager()
    
    def create(self, product: Product, token: AuthResponse) -> PicturesGeneratorResponse:
        """
        
        Args:
            product (Product):
            token (AuthResponse):
        Returns:
            (PicturesGeneratorResponse):
        """
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
    
    def __create_urls(self, images_paths: list[str]) -> PicturesGeneratorResponse:
        """
        Args:
            images_paths (list[str]):
        """
        urls: list[UrlGeneratorResponse] = []
        failed_urls: list[str] = []
        
        for img in images_paths:
            temp_image = self.correct_image.corret(img)
            url_response = self.__upload_image(temp_image)
            if not url_response.success:
                failed_urls.append(f"Imagem: {img}, causa: {url_response.error.cause}")
            urls.append(url_response)
            os.remove(temp_image) # Removes the temp image.
        
        if failed_urls:
            logging.warning(f"Falha ao gerar uma url para a imagem: {failed_urls}")
        
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
        
        
    
    def __upload_image(self, image_path: str):
        """
        Args:
            
        Returns:
            
        """
        response = self.url_generator.upload_image(image_path)
        
        return UrlGeneratorResponse(
                success=True,
                error=None,
                data=UrlGeneratorContent(
                    id=response.get("image_id"),
                    url=response.get("secure_url")
                )
            )
        
    
    def __create_meli_ids(self, urls: list[UrlGeneratorResponse], token: AuthResponse) -> PicturesGeneratorResponse:
        """
        Args:
            urls (list[str]):
        """
        failed_pictures_ids: list[str] = []
        meli_pictures_ids: list[str] = []
        
        for url in urls:
            meli_picture_id = self.__upload_url(url.data.url, token)
            if not meli_picture_id.success:
                failed_pictures_ids.append(f"url:{url.data.url}, causa: {meli_picture_id.error.message}")
            meli_pictures_ids.append(meli_picture_id.data.get("id")) # Gets the meli image id
            self.url_generator.delete_image(url.data.id) # Removes the online image from account
        
        if failed_pictures_ids:
            logging.warning(f"Falha ao gerar um ID para a url: {failed_pictures_ids}")
        
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
            url (str):
            token (AuthResponse):
        Returns:
            (MeliResponse): 
        """
        meli_id_response = self.meli_image_manager.get_meli_picture(image_url=url, access_token=token.access_token)
        
        if not meli_id_response.success:
            logging.error(f"{meli_id_response.error.message}. Exception: {meli_id_response.error.exception}")
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=meli_id_response.error
            )
        
        print(f"{meli_id_response.data = }")
        
        return PicturesGeneratorResponse(
            success=True,
            result=meli_id_response.data
        )
