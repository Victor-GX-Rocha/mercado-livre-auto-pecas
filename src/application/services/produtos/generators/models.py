""" Models for produto services. """

from typing import Optional, Any, Protocol
from dataclasses import dataclass
from abc import abstractmethod

from src.infrastructure.api.mercadolivre.auth import AuthResponse
from src.infrastructure.database.models.produtos import Product


class GeneratorProtocol(Protocol):
    """ Interface for data generators. """
    @abstractmethod
    def generate(self, product: Product, token: AuthResponse):
        """
        
        Args:
            product (Product): Dataclass product table.
            token (AuthResponse): Mercado libre auth dataclass token. 
        """


@dataclass
class GeneratorsResponse:
    success: bool
    result: list[dict]
    error: Optional[Any] = None

@dataclass
class JsonGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None

@dataclass
class ShippimentGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None
