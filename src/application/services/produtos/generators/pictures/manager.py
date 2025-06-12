""" Manage the creation of a mercado libre images IDs """


from PIL import Image




class ImageProcessor:
    def __init__(self, imagem_path, logo_path=None):
        self.imagem_path = imagem_path
        self.logo_path = logo_path
        
    def validar_e_redimensionar_imagem(self, output_path):
        try:
            img = Image.open(self.imagem_path)
            
            # Verifica as dimensões
            largura, altura = img.size
            if largura < 500 or altura < 500:
                img = img.resize((500, 500))
            
            # Verifica o formato
            if img.format not in ['JPEG', 'JPG', 'PNG']:
                img = img.convert('RGB')
            
            # Verifica o tamanho do arquivo
            img.save(output_path, optimize=True, quality=85)
            
            return True
        except Exception as e:
            logging.error(f"Erro ao processar a imagem: {e}")
            return False


class CorretImageDimentions:
    def __init__(self, imagem_path):
        self.imagem_path = imagem_path
    
    def corret(self, imagem_path: str):
        """
        
        Args:
            imagem_path (str):
        """
        temp_path: str = f"{imagem_path}_temp.jpg"
        img = Image.open(self.imagem_path)
        img: Image.ImageFile = self.corret_dimensions(img)
        img: Image.ImageFile = self.corret_format(img)
        
        
        img.save(temp_path, optimize=True, quality=85)
        
    
    def corret_dimensions(self, img: Image.ImageFile) -> Image.ImageFile:
        """
        
        Args:
            img (Image.ImageFile):
        Returns:
            (Image.ImageFile): 
        """
        largura, altura = img.size
        if largura < 500 or altura < 500:
            img = img.resize((500, 500))
        return img
    
    def corret_format(self, img: Image.ImageFile) -> Image.ImageFile:
        """
        
        Args:
            img (Image.ImageFile):
        Returns:
            (Image.ImageFile): 
        """
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            img = img.convert('RGB')
        return img

    # def validar_e_redimensionar_imagem(self, output_path):
    #     try:
    #         img = Image.open(self.imagem_path)
            
    #         # Verifica as dimensões
    #         largura, altura = img.size
    #         if largura < 500 or altura < 500:
    #             img = img.resize((500, 500))
            
    #         # Verifica o formato
    #         if img.format not in ['JPEG', 'JPG', 'PNG']:
    #             img = img.convert('RGB')
            
    #         # Verifica o tamanho do arquivo
    #         img.save(output_path, optimize=True, quality=85)
            
    #         return True
    #     except Exception as e:
    #         logging.error(f"Erro ao processar a imagem: {e}")
    #         return False





from ......core.log import logging
from ......infrastructure.database.models.produtos import Product
from ......infrastructure.api.mercadolivre.auth import AuthResponse
from ......infrastructure.api.mercadolivre.images import MeliImageManager
from ......infrastructure.api.mercadolivre.models import MeliResponse
from .models import PicturesGeneratorResponse
# from .generator import 

class PicturesGenerator:
    def __init__(self):
        self.url_generator = 
        self.meli_image_manager = MeliImageManager()
    
    def create(self, product: Product, token: AuthResponse) -> PicturesGeneratorResponse:
        """
        
        """
        meli_pictures_ids: list[str] = self._get_ids(token)
        if not meli_pictures_ids.success:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=
            )
        
        return PicturesGeneratorResponse(
            success=True,
            result=,
            error=None
        )
    
    def _get_ids(self, product: Product, token: AuthResponse) -> list[str] | None:
        """
        
        """
        images: list[str] = self.image_normalizer.normalize_format(product.sale.imagens)
        if not images:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f'Coluna "imagens" possui conteúdo em formato inadequado: {images}'
            )
        
        url_response = self.__create_urls(images)
        if not url_response.success:
            return url_response
        
        return self.__create_meli_ids(url_response.result, token)
        
    
    def __create_urls(self, images: list[str]):
        """
        Args:
            images (list[str]):
        """
        urls: list[str] = []
        failed_urls: list[str] = []
        
        for img in images:
            url_response = self.url_generator.create(img)
            if not url_response.success:
                failed_urls.append(f"Imagem: {img}, causa: {url_response.error.cause}")
            urls.append(url_response.result)
        
        if failed_urls:
            logging.warning(f"Falha ao gerar uma url para a imagem: {failed_urls}")
        
        if not urls:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f'Nenhuma das imagens da coluna "imagens" gerou uma URL válida: {images}'
            )
        
        return PicturesGeneratorResponse(
            success=True,
            result=urls,
            error=None
        )
        
        
    def __create_meli_ids(self, urls: list[str], token: AuthResponse):
        """
        Args:
            urls (list[str]):
        """
        failed_pictures_ids: list[str] = []
        meli_pictures_ids: list[str] = []
        
        for url in urls:
            meli_picture_id = self.__upload_url(url, token)
            if not meli_picture_id.success:
                failed_pictures_ids.append(f"url:{url}, causa: {meli_picture_id.error.cause}")
            meli_pictures_ids.append(meli_picture_id.data.get("id"))
        
        if failed_pictures_ids:
            logging.warning(f"Falha ao gerar um ID para a url: {failed_pictures_ids}")
        
        if not meli_pictures_ids:
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=f'Nenhuma das imagens da coluna "imagens" gerou uma ID de imagem do mercado livre válida. Causas: '
            )
        
        return None
    
    def __upload_url(self, url: str, token: AuthResponse) -> MeliResponse:
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
            logging.error(f"{meli_id_response.error.exception}. Exception: {meli_id_response.error.exception}")
            return PicturesGeneratorResponse(
                success=False,
                result=None,
                error=meli_id_response.error.message
            )
        
        print(f"{meli_id_response.data = }")
        
        return PicturesGeneratorResponse(
            success=True,
            result=meli_id_response.data
        )
