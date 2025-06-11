""" Gerenciamento de Imagens no Cloudinary """

import cloudinary
import cloudinary.uploader
import cloudinary.api

from core.log import logging

from database.repositories import ProductRepository


class CloudinaryManager:
    """ Gerenciamento de Operações no Cloudinary """
    def __init__(self, product_repository: ProductRepository):
        """
        Inicializa a classe com um objeto GetDB.
        
        :param getdb: Objeto da classe GetDB para obter os detalhes de login do Cloudinary.
        """
        self.product_repository = product_repository
        self.activate()
        
    def activate(self):
        """
        Ativa a classe CloudinaryManager
        
        :param getdb: Objeto da classe GetDB para obter os detalhes de login do Cloudinary.
        """
        try:
            self.cloud_user: dict[str, str] = self.product_repository.get_cloudinary_login()[0]
            # print('cloud_user:', self.cloud_user)
            self.validate_login_details()
            self.configure()
        except Exception as e:
            self._handle_cloudinary_error("CloudinaryManager.activate", None, None, e)
            raise RuntimeError(f"Erro ao inicializar CloudinaryManager: {e}")
        
    def validate_login_details(self) -> None:
        """
        Valida se os detalhes de login do Cloudinary estão completos.
        
        Levanta uma exceção se alguma chave necessária estiver ausente.
        """
        try:
            required_keys = ['cloud_name', 'api_key', 'api_secret']
            for key in required_keys:
                if key not in self.cloud_user:
                    raise ValueError(f"Detalhes de login do Cloudinary incompletos. Chave '{key}' ausente.")
        except ValueError as v:
            logging.warning(f"{v}")
            
        
    def configure(self) -> None:
        """
        Configura as Credenciais do Cloudinary.
        
        Levanta uma exceção se a configuração falhar.
        """
        try:
            cloudinary.config(
                cloud_name=self.cloud_user['cloud_name'],
                api_key=self.cloud_user['api_key'],
                api_secret=self.cloud_user['api_secret']
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao configurar Cloudinary: {e}")
        
    def upload_image(self, image_path: str) -> dict[str, str] | None:
        """
        Faz o Upload de uma Imagem para o Cloudinary.
        
        :param image_path: O caminho da imagem a ser enviada para o Cloudinary.
        :return: Um dicionário contendo o ID da imagem e a URL segura, ou None em caso de erro.
        """
        try:
            response = cloudinary.uploader.upload(image_path)
            return {
                'image_id': response['public_id'],
                'secure_url': response['secure_url']
            }
        except Exception as e:
            self._handle_cloudinary_error("CloudinaryManager.upload_image", image_path, None, e)
            return None
        
    def delete_image(self, image_id: str) -> bool:
        """
        Deleta uma Imagem do Cloudinary.
        
        :param image_id: O ID da imagem a ser deletada do Cloudinary.
        :return: True se a imagem foi deletada com sucesso, False caso contrário.
        """
        try:
            response = cloudinary.uploader.destroy(image_id)
            return response.get('result') == 'ok'
        except Exception as e:
            self._handle_cloudinary_error("CloudinaryManager.delete_image", None, image_id, e)
            return False
        
    def create_album(self, album_name: str) -> str | None:
        """
        Cria um Álbum no Cloudinary.
        
        :param album_name: O nome do álbum a ser criado no Cloudinary.
        :return: O ID do álbum criado, ou None em caso de erro.
        """
        try:
            response = cloudinary.api.create_folder(album_name)
            album_id = response['name']
            return album_id
        except Exception as e:
            self._handle_cloudinary_error("CloudinaryManager.create_album", None, None, e)
            return None
        
    def add_to_album(self, album_id: str, image_id: str) -> bool:
        """
        Adiciona uma Imagem a um Álbum no Cloudinary.
        
        :param album_id: O ID do álbum onde a imagem será adicionada.
        :param image_id: O ID da imagem a ser adicionada ao álbum.
        :return: True se a imagem foi adicionada com sucesso, False caso contrário.
        """
        try:
            response = cloudinary.api.add_to_folder(album_id, image_id)
            return response.get('result') == 'ok'
        except Exception as e:
            self._handle_cloudinary_error("CloudinaryManager.add_to_album", None, image_id, e)
            return False
        
    def _handle_cloudinary_error(self, method_name: str, image_path: str | None, image_id: str | None, error: Exception) -> None:
        """
        Trata erros do Cloudinary e registra logs detalhados.
        
        :param method_name: Nome do método onde o erro ocorreu.
        :param image_path: Caminho da imagem (se aplicável).
        :param image_id: ID da imagem (se aplicável).
        :param error: Exceção capturada.
        """
        if isinstance(error, ValueError):
            mensagem = f"Erro de validação: {error}"
        elif isinstance(error, RuntimeError):
            mensagem = f"Erro de configuração ou inicialização: {error}"
        else:
            mensagem = f"Erro inesperado: {error}"
        
        logging.error(
            f"{mensagem}\nImagem: {image_path}\nID da Imagem: {image_id}"
        )


if __name__ == '__main__':
    pass