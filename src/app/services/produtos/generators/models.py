""" Models for produto services. """

from typing import Optional, Any, Protocol
from dataclasses import dataclass
from abc import abstractmethod

from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.models.produtos import Product


class GeneratorProtocol(Protocol):
    """ Interface for data generators. """
    @abstractmethod
    def generate(self, product: Product, token: AuthResponse):
        """
        
        Args:
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
        """


@dataclass
class GeneratorsResponse:
    success: bool
    result: list[dict]
    error: Optional[Any] = None

@dataclass
class PayloadGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None

@dataclass
class ShippingGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None
