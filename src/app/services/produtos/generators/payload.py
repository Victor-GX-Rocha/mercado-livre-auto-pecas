""" Generate the payload data for mercado libre requests. """

from typing import Any

from src.core import log
from src.infra.db.models.produtos import Product
from src.infra.api.mercadolivre.auth import AuthResponse
from .category import CategoryGenerator
from .attributes import AttributesGenerator
from .pictures import PicturesGenerator
from .shipping import ShippingGenerator
from .models import PayloadGeneratorResponse


class PayloadGenerator:
    """ Generate the product payloads. """
    def __init__(self):
        self.shipping_generator = ShippingGenerator()
        self.attribute_generator = AttributesGenerator()
        self.pictures_generator = PicturesGenerator()
        self.category_generator = CategoryGenerator()
    
    def build_publication_payload(self, product: Product, token: AuthResponse) -> PayloadGeneratorResponse:
        """
        Constructs the item publication payload for Mercado Livre API.
        Args:
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
        Returns:
            PayloadGeneratorResponse:
        """
        try:
            shipping = self.shipping_generator.generate(product, token)
            if not shipping.success:
                return PayloadGeneratorResponse(
                    success=False,
                    result=None,
                    error=shipping.error
                )
            
            category = self.category_generator.generate(product, token)
            if not category.success:
                return PayloadGeneratorResponse(
                    success=False,
                    result=None,
                    error=category.error
                )
            
            attributes = self.attribute_generator.generate(product, token)
            if not attributes.success:
                return PayloadGeneratorResponse(
                    success=False,
                    result=None,
                    error=attributes.error
                )
            
            pictures = self.pictures_generator.generate(product, token)
            if not pictures.success:
                return PayloadGeneratorResponse(
                    success=False,
                    result=None,
                    error=pictures.error
                )
            
            template_payload: dict[str, Any] = {
                "site_id": "MLB",
                "title": product.sale.titulo,
                "category_id": category.result,
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
            
            return PayloadGeneratorResponse(
                success=True,
                result=template_payload
            )
            
        except Exception as e:
            message: str = f"Falha inesperada no processo de criação do payload: {e}"
            log.dev.exception(message)
            return PayloadGeneratorResponse(
                success=False,
                result=None,
                error=[message]
            )
    
    def build_edition_payload(
            self, 
            product: Product,
            product_data: dict[str, Any],
            token: AuthResponse
        ) -> PayloadGeneratorResponse:
        """ Basicly, do some validations to only atualize something if it's really necessary. """
        template_payload: dict[str, str] = {}
        
        try:
            
            if product.sale.preco != product_data.get("price"):
                template_payload.update({"price": float(product.sale.preco)})
            
            if product.sale.estoque != product_data.get("available_quantity"):
                template_payload.update({"available_quantity": product.sale.estoque})
            
            if product.sale.modo_compra != product_data.get("buying_mode"):
                template_payload.update({"buying_mode": product.sale.modo_compra})
            
            if product.technical.condicao_produto != product_data.get("condition"):
                template_payload.update({"condition": product.technical.condicao_produto})
            
            if product.identfiers.sku != product_data.get("seller_custom_field"):
                template_payload.update({"seller_custom_field": product.identfiers.sku})
            
            shipping = self.shipping_generator.generate(product, token)
            if shipping.success:
                template_payload.update({"shipping": shipping.result})
            
            pictures = self.pictures_generator.generate(product, token)
            if pictures.success:
                template_payload.update({"pictures": pictures.result})
            
            return PayloadGeneratorResponse(
                success=True,
                result=template_payload
            )
            
        except Exception as e:
            return PayloadGeneratorResponse(
                success=False,
                result=template_payload,
                error=f"Exceção inesperada ao criar payload de edição: {e}"
            )
