""" Manages the category selection. """

from typing import Literal, Optional
from dataclasses import dataclass, field

from src.infrastructure.api.mercadolivre.auth import AuthResponse
from src.infrastructure.database.models.produtos import Product
from src.application.services.produtos.generators.models import GeneratorProtocol
from src.infrastructure.api.mercadolivre.category import CategoryRequests

from src.application.shared.category.finders import IDFinderByPath


from .models import CategoryGeneratorValidationResponse
from .validators import CategoryValidator


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
    def __init__(self):
        self.category_validator = CategoryValidator()
        self.category_requests = CategoryRequests()
        self.category_finder_by_path = IDFinderByPath()
    
    def generate(self, product: Product, token: AuthResponse) -> CategoryGeneratorResponse:
        """
        
        Args:
            product (Product): Dataclass product table.
            token (AuthResponse): Mercado libre auth dataclass token.
        Returns:
            
        Todo:
            Validations:
                - [x] categoria         → This two are basicly the same operation.
                - [x] categoria_id      ↳ This two are basicly the same operation.
                - [x] categoria_caminho
                - [ ] categoria_exemplo (depreacted)
                - [ ] titulo (not used anymore)
        """
        causes: list[str] = []
        
        if product.category.categoria:
            categoria_response = self.__validate_category(product, token, product.category.categoria)
            if categoria_response.is_valid:
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_response.id_used
                )
        
        causes.append(f"Coluna categoria: {categoria_response.causes}")
        
        if product.category.categoria_id:
            categoria_id_response = self.__validate_category(product, token, product.category.categoria_id)
            if categoria_id_response.is_valid:
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_id_response.id_used
                )
        
        causes.append(f"Coluna categoria_id: {categoria_id_response.causes}")
        
        if product.category.categoria_caminho:
            categoria_caminho_response = self.__validate_category_path(product, token)
            if categoria_caminho_response.is_valid:
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_caminho_response.id_used
                )
        
        causes.append(f"Coluna categoria caminho: {categoria_caminho_response.causes}")
        
        return CategoryGeneratorResponse(
            success=False,
            result=None,
            error=CategoryGeneratorErrorCause(
                causes=f"Nenhuma das colunas de categoria apresentou uma categoria válida: {causes}"
            )
        )
    
    def __validate_category(self, product: Product, token: AuthResponse, category_id: str) -> CategoryGeneratorValidationResponse:
        """
        Validate a category ID.
        Args:
            product (Product): Dataclass product table.
            token (AuthResponse): Mercado libre auth dataclass token.
            category_id (str): Category ID.
        """
        
        data_response = self.category_requests.get_category_data(
            category_id=category_id,
            access_token=token.access_token
        )
        
        if not data_response.success:
            return CategoryGeneratorValidationResponse(
                id_used=category_id,
                causes=[f"Falha ao obter os dados da categoria {category_id} -> {data_response.error}"]
            )
        
        validation_response = self.category_validator.validate(
            product=product, 
            category_data=data_response.data
        )
        
        if not validation_response.is_valid:
            return CategoryGeneratorValidationResponse(
                id_used=category_id,
                causes=validation_response.causes
            )
        
        
        product.category.categoria = category_id
        return CategoryGeneratorValidationResponse(
            is_valid=True,
            id_used=category_id,
        )
    
    def __validate_category_path(self, product: Product, token: AuthResponse) -> CategoryGeneratorValidationResponse:
        """
        Gets the category ID by a category path and validate the ID.
        Args:
            product (Product): Dataclass product table.
            token (AuthResponse): Mercado libre auth dataclass token.
            category_id (str): Category ID.
        """
        
        finder_response = self.category_finder_by_path.find(product.category.categoria_caminho, token.access_token)
        if not finder_response.success:
            return CategoryGeneratorValidationResponse(causes=finder_response.error)
        
        return self.__validate_category(
            product=product,
            token=token,
            category_id=finder_response.result
        )
