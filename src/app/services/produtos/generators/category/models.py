""" Category models. """

from dataclasses import dataclass
from typing import Optional, Protocol, Any

from src.infra.db.models.produtos import Product

@dataclass
class ValidationResponse:
    is_valid: bool = False
    reason: Optional[str] = None
    causes: Optional[list] = None

@dataclass
class CategoryGeneratorValidationResponse:
    is_valid: bool = False
    id_used: str = None
    reason: Optional[str] = None
    causes: Optional[list] = None

class CategoryValidateProtocol(Protocol):
    """ Validate a especific category term. """
    def validate(self, produto: Product, category_data: list[str, Any]):
        """ 
        Validate a category term.
        Args:
            produto: (Product): Dataclass table product.
            category_data: (list[str, Any]): Category data.
        """
