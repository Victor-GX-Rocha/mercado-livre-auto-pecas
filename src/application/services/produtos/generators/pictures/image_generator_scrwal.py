""" Manage the creation of a mercado libre images IDs """

from .....core.log import logging

import re
import os
import json
import requests

from typing import Optional
from decimal import Decimal
from PIL import Image
import cv2
import numpy as np

from core.log import logging

from database.repositories import ProductRepository



def decimal_default(obj) -> str:
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


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
            logging.error(
                f"Erro ao processar a imagem: {e}"
            )
            return False
        
    def remover_logo(self, output_path):
        if not self.logo_path:
            logging.error(
                "Caminho do logo não fornecido."
            )
            return False
            
        try:
            # Carregar a imagem original e o logo
            imagem = cv2.imread(self.imagem_path)
            logo = cv2.imread(self.logo_path, cv2.IMREAD_GRAYSCALE)
            
            # Detectar o logo na imagem
            result = cv2.matchTemplate(imagem, logo, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(result >= threshold)
            
            # Remover o logo
            for pt in zip(*loc[::-1]):
                cv2.rectangle(imagem, pt, (pt[0] + logo.shape[1], pt[1] + logo.shape[0]), (0, 0, 0), -1)
            
            # Salvar a imagem resultante
            cv2.imwrite(output_path, imagem)
            
            return True
        except Exception as e:
            logging.error(
                f"Erro ao remover o logo: {e}"
            )
            return False

class GerarImagens:
    """
    ### Administra os métodos de geração de imagem.
    Realiza as integrações com mercado livre necessárias para obter o ID de uma imagem publicada.
    """
    def __init__(self, cloud: object):
        """
        Objeto da classe CloudinaryManager
        """
        self.cloud = cloud
    
    @staticmethod
    def is_url(path_or_url: str) -> bool:
        """
        Verifica se o caminho é uma URL.
        
        path_or_url (str): O caminho ou URL a ser verificado.
        Returns (bool): True se for uma URL válida, False caso contrário.
        """
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return bool(url_pattern.match(path_or_url))
        
    def upload_images_to_cloudinary(self, product: dict[str, str]) -> dict[str, list[str]]:
        """
        Direciona a ação apropriada para a coluna de imagem do SQL.
        Analisa o conteúdo das colunas de imagem no banco de dados.
        
        - Descobre a tipagem da imagem, URL ou caminho Windows.
        - Posta uma imagem no Cloudinary.
        
        :param product: Dados do produto.
        :param cloud: Objeto da classe CloudinaryManager.
        :return: Um dicionário contendo listas de URLs e IDs das imagens processadas.
        """
        self.cloudinary_images: dict[str, list[str]] = {'URLs': [], 'IDs': []}
        
        if not product['imagens']:
            return self.cloudinary_images
        
        for image_path in product['imagens']:
            self.image_path: str = image_path.strip()
            
            if self.is_url(self.image_path):
                self.cloudinary_images['URLs'].append(self.image_path)
            else:
                # Processar a imagem antes de fazer o upload
                processor = ImageProcessor(self.image_path)
                temp_path = f"{self.image_path}_temp.jpg"
                if processor.validar_e_redimensionar_imagem(temp_path):
                    response = self.cloud.upload_image(temp_path)
                    if response:
                        self.cloudinary_images['URLs'].append(response['secure_url'])
                        self.cloudinary_images['IDs'].append(response['image_id'])
                    os.remove(temp_path)  # Remover o arquivo temporário
                else:
                    logging.error(
                        f"Erro ao processar a imagem: {self.image_path}"
                    )
        return self.cloudinary_images
        
    def upload_URLimage_to_MercadoLivre(self, image_URL: str, access_token: str) -> str:
        """
        Realiza o upload de uma URL de imagem no mercado livre e retorna seu ID.
        O mercado livre exige o uso de URLs como parâmetro para que uma imagem seja publicada.
        :image_URL: URL da imagem a ser publicada no mercado livre.
        """
        url = "https://api.mercadolibre.com/pictures"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(image_URL)
            if response.status_code not in (200, 201):
                logging.error(
                    f"Erro ao baixar a imagem: {response.status_code}"
                )
                return None
            
            files = {'file': (image_URL.split('/')[-1], response.content, 'image/jpeg')}
            response = requests.post(url, headers=headers, files=files)
            
            if response.status_code in (200, 201):
                return response.json().get("id")
            else:
                logging.error(
                    f"Erro ao fazer upload da imagem: {response.status_code}\nResposta: {response.text}"
                )
                return None
        except Exception as e:
            logging.error(
                f"Erro inesperado: {e}"
            )
            return None
        
    def upload_a_list_Of_URLimages_to_MercadoLivre(self, URLs_list: list[str], access_token: str) -> list[str]:
        """
        ###
        """
        self.mercadoLivre_IDs: list[dict] = []
        
        for url in URLs_list:
            self.mercadoLivre_ID = self.upload_URLimage_to_MercadoLivre(url, access_token)
            if self.mercadoLivre_ID:
                self.mercadoLivre_IDs.append({'id': self.mercadoLivre_ID})
        
        if not self.mercadoLivre_IDs:
            logging.error(
                "Nenhuma imagem foi carregada com sucesso. Verifique as URLs das imagens."
            )
            raise ValueError("Nenhuma imagem foi carregada com sucesso. Verifique as URLs das imagens.")
        
        return self.mercadoLivre_IDs
        
    def create_MercadoLivre_ImagesIDs(self, product: dict[str, str], access_token: str) -> list[str]:
        """
        :param cloud: Objeto da classe CloudinaryManager.
        """
        try:
            # Faz o upload das imagens no Cloudinary e retorna um dicionário com as URLs e IDs gerados.
            self.cloudinary_images: dict[str, list] = self.upload_images_to_cloudinary(product)
            
            # Posta essas URLs no mercado livre e pega os IDs das imagens retornados pelo mercado livre.
            self.mercadoLivre_imagesIDs: list[str] = self.upload_a_list_Of_URLimages_to_MercadoLivre(self.cloudinary_images['URLs'], access_token)
            
            # Apaga a lista de imagens postadas no Cloudinary, utilizando os IDs retornados do método upload_images_to_cloudinary().
            for cloudinary_image_id in self.cloudinary_images['IDs']:
                self.cloud.delete_image(cloudinary_image_id)
            
            # Retorna a lista de IDs de imagens do mercado livre gerada.
            return self.mercadoLivre_imagesIDs
        except Exception as e:
            logging.error(
                f"Erro ao criar IDs de imagens no Mercado Livre: {e}"
            )
            return []






from .....infrastructure.database.models.produtos import Product


class ImageURLGenerator:...


class MeliImagesGenerator:
    def __init__(self, url_generator):
        self.url_generator = url_generator

    # def get_image_url(self):... This step needs to be realited in another class
    
    def create(self, product: Product):
        """
        Args:
            product Product:
        """
        img_paths: list[str] = normalize_images_paths(product.sale.imagens)
        urls: list[str] = self.url_generator(img_paths)
        return [self.get_image_id(url) for url in urls]
        
    
    def get_image_id(self):...













