""" . """

from dataclasses import dataclass
from typing import Protocol, Optional, runtime_checkable

from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.models.produtos import Product

@dataclass
class ValidationResponse:
    is_valid: bool = False 
    reason: Optional[str] = None
    causes: Optional[list] = None

@runtime_checkable
class ProdutosOperationProtocol(Protocol):
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        ...

