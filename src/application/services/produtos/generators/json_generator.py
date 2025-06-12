""" Generate the JSONs format for mercado libre requests """

# self.cloud = CloudinaryManager(product_repository)
# self.gerar_imagens = GerarImagens(self.cloud)
# self.repo

from typing import Any, Optional
from dataclasses import dataclass

from .....core.log import logging
from .....infrastructure.database.models.produtos import Product
from .....infrastructure.api.mercadolivre.auth import AuthResponse
from .attributes import AttributesGenerator
from .pictures import PicturesGenerator, PicturesGeneratorResponse
from .models import (
    JsonGeneratorResponse,
    ShippimentGeneratorResponse
)

# @dataclass
# class JsonGeneratorResponse:
#     success: bool
#     result: Optional[dict[str, Any]]
#     error: list

# @dataclass
# class ShippimentGeneratorResponse:
#     success: bool
#     result: Optional[dict[str, Any]]
#     error: list

# @dataclass
# class PicturesGeneratorResponse:
#     success: bool
#     result: Optional[dict[str, Any]]
#     error: list

class JsonGenerator:
    def __init__(self):
        """
        Args:
            cloud (): Cloudinary API interface. 
            # In the future, I need to think about this as any type of image uploader, not only cloudinary
        """
        self.attribute_generator = AttributesGenerator()
        self.pictures_generator = PicturesGenerator()
        self.category_generator = CategoryGenerator()
    
    def build_publication_json(self, product: Product, token: AuthResponse) -> JsonGeneratorResponse:#dict[str, Any]:
        """
        Construct a json with data for a publication on mercado libre.
        Args:
            product (Product): 
            token (AuthResponse): 
        Returns:
            (JsonGeneratorResponse):
        Todo:
            - [x] shipping.
            - [x] attributes.
            - [ ] pictures (in process)
            - [ ] category
        """
        
        shipping = self.build_shipping_info(product)
        if not shipping.success:
            return JsonGeneratorResponse(
                success=False,
                result=None,
                error=shipping.error
            )
        
        attributes = self.attribute_generator.create(product, token)
        if not attributes.success:
            return JsonGeneratorResponse(
                success=False,
                result=None,
                error=attributes.error
            )
        
        pictures = self.pictures_generator.create(product, token)
        if not pictures.success:
            return JsonGeneratorResponse(
                success=False,
                result=None,
                error=pictures.error
            )
        
        """
        Quanto ao ID, na verdade ainda falta ativar a classe do cloudinary!!!
        """
        
        category = self.category_generator.create(product, token)
        if not category.success:
            return JsonGeneratorResponse(
                success=False,
                result=None,
                error=category.errors
            )
        
        try:
            # Look for other information that can be entered here
            self.template_json: dict[str, Any] = {
                "site_id": "MLB",
                "title": product.sale.titulo,
                "category_id": category.result, Ainda falta criar isso
                "price": product.sale.preco,
                "currency_id": 'BRL',
                "available_quantity": product.sale.estoque,
                "buying_mode": product.sale.modo_compra,
                "listing_type_id": product.sale.tipo_anuncio,
                "condition": product.technical.condicao_produto,
                "seller_custom_field": product.identfiers.sku,
                "accepts_mercadopago": True,
                "attributes": attributes.result,
                "shipping": shipping.result,
                "pictures": pictures.result
            }
            
        except Exception as e:
            message: str = f"Excessão inesperada no processo de criação do JSON: {e}"
            logging.error(message)
            return JsonGeneratorResponse(
                success=False,
                result=None,
                error=[message]
            )
        
    def build_shipping_info(self, product: Product) -> ShippimentGeneratorResponse:
        """
        Build the shippiment data.
        Args:
            product: 
        """
        try:
            
            comprimento: str = product.dimensions.comprimento
            largura: str = product.dimensions.largura
            altura: str = product.dimensions.altura
            peso: str = product.dimensions.peso
            
            dimensoes: str = str(f'{comprimento}x{largura}x{altura},{peso}')
            
            shipping_info: dict[str, Any] = {
                "mode": product.shippiment.modo_envio,
                "dimensions": dimensoes,
                "local_pick_up": product.shippiment.retirada_local,
                "free_shipping": product.shippiment.frete_gratis,
                "logistic_type": "logistic_type"  # 'drop_off'
            }
            
            return ShippimentGeneratorResponse(
                success=False,
                result=shipping_info,
                error=[message]
            )
            
        except Exception as e:
            message: str = f"Falha inesperada ao criar informações de envio: {e}"
            logging.error(message)
            return ShippimentGeneratorResponse(
                success=False,
                result=None,
                error=[message]
            )
        
        
        
        
        
        
        
        
        
        
        
        
        try:
            pictures: list[str] = self.generate_images.create_MercadoLivre_ImagesIDs(product, token)
            envio: dict = self.create_shipping_info(product)
            
            atributos = Attributes(product)
            # lista_atributos: list = self.create_product_attributes(product)
            category_manager = CategoryManager(token, self.product_repository)
            chosen_category = category_manager.validate_category(product)
            
            if not chosen_category:
                # self.updb.error_message(product_id=product.get('id', ''), cod_erro='91', message='aqui')
                return False
            
            logging.info(f'Categoria escolhida: {chosen_category}')
            
            sku: str = product.get('sku', product.get('cod_produto', ''))            
            
            self.template_json: dict[str, str] = {
                "site_id": "MLB",
                "title": product.get('titulo'),
                "category_id": chosen_category, #"MLB5802",  # "MLB193623", #categoria['category_id'],
                "price": product.get('preco'),
                "currency_id": 'BRL',  # product['moeda'],
                "available_quantity": product.get('estoque'),
                "buying_mode": product.get('modo_compra'),
                "listing_type_id": product.get('tipo_anuncio'),
                "condition": product.get('condicao_produto'),
                "seller_custom_field":sku,
                "pictures": pictures,
                "accepts_mercadopago": True,
                "shipping": envio,
                # "attributes": lista_atributos,
                "attributes": atributos.attributes_list,
                
            }
            
            return json.dumps(self.template_json, indent=4, default=decimal_default)
        except Exception as e:
            logging.error(
                f"Erro ao construir JSON: {e}"
            )
            return None