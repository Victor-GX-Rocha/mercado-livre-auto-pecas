""" Manages the category selection. """

from ..models import GeneratorProtocol
from src.infrastructure.api.mercadolivre.auth import AuthResponse
from src.infrastructure.database.models.produtos import Product


from typing import Literal, Optional
from dataclasses import dataclass, field

@dataclass
class CategoryGeneratorErrorCause:
    causes: list = field(default_factory=list)
    context: str = None
    exception: str = None

@dataclass
class CategoryGeneratorResponse:
    success: bool
    result: str
    error: Optional[CategoryGeneratorErrorCause] = None


class CategoryGenerator(GeneratorProtocol):
    def generate(self, product: Product, token: AuthResponse):
        """
        
        Args:
            product (Product): Dataclass product table.
            token (AuthResponse): Mercado libre auth dataclass token.
        Returns:
            
        Todo:
            Validations:
                - [ ] categoria         → This two are basicly the same operation.
                - [ ] categoria_id      ↳ This two are basicly the same operation.
                - [ ] categoria_caminho
                - [ ] categoria_exemplo (depreacted)
                - [ ] titulo (not used anymore)
        """
        causes: list[str] = []
        
        if product.category.categoria:
            categoria_response = self.validate_category()
            if categoria_response.is_valid:
                return CategoryGeneratorResponse(
                    success=True,
                    result=product.category.categoria
                )
        
        causes.append(f"Coluna categoria: {categoria_response.error.cause}")
        
        if product.category.categoria_id:
            categoria_id_response = self.validate_category_id()
            if categoria_id_response.is_valid:
                product.category.categoria = categoria_id_response.id_used # I can make this part inside the method
                return CategoryGeneratorResponse(
                    success=True,
                    result=product.category.categoria_id
                )
        
        causes.append(f"Coluna categoria_id: {categoria_id_response.error.cause}")
        
        if product.category.categoria_caminho:
            categoria_caminho_response = self.validate_category_path()
            if categoria_caminho_response.is_valid:
                product.category.categoria = categoria_caminho_response.id_used # This part too
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_caminho_response.id_used
                )
        
        causes.append(f"Coluna categoria caminho: {categoria_caminho_response.error.cause}")
        
        return CategoryGeneratorResponse(
            success=False,
            result=None,
            error=CategoryGeneratorErrorCause(
                causes=f"Nenhuma das colunas de categoria apresentou uma categoria válida: {causes}"
            )
        )
    
    def validate_category(self):
        raise NotImplementedError
    
    def validate_category_id(self):
        raise NotImplementedError
    
    def validate_category_path(self):
        raise NotImplementedError
    
    