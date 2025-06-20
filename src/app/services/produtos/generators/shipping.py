""" Generate the shipping info. """

from typing import Any
from src.infra.db.models.produtos import Product
from src.infra.api.mercadolivre.auth import AuthResponse

from .models import (
    GeneratorProtocol,
    ShippingGeneratorResponse
)


class ShippingGenerator(GeneratorProtocol):
    """ Manages the generation of the product shipping data. """
    def generate(self, product: Product, token: AuthResponse) -> ShippingGeneratorResponse:
        """
        Construct the shipping data.
        Args:
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
        Returns:
            ShippingGeneratorResponse:
        """
        try:
            
            length: str = product.dimensions.comprimento
            width: str = product.dimensions.largura
            height: str = product.dimensions.altura
            weight: str = product.dimensions.peso
            
            dimensions: str = str(f'{length}x{width}x{height},{weight}')
            
            shipping_info: dict[str, Any] = {
                "mode": product.shippiment.modo_envio,
                "dimensions": dimensions,
                "local_pick_up": product.shippiment.retirada_local,
                "free_shipping": product.shippiment.frete_gratis,
                "logistic_type": "logistic_type"  # 'drop_off'
            }
            
            return ShippingGeneratorResponse(
                success=True,
                result=shipping_info
            )
            
        except Exception as e:
            message: str = f"Falha inesperada ao criar informações de envio: {e}"
            # log.dev.exception(message)
            return ShippingGeneratorResponse(
                success=False,
                result=None,
                error=[message]
            )
