""" Manages the category selection. """

from typing import Optional
from dataclasses import dataclass, field

from src.core import log
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.models.produtos import Product
from src.app.services.produtos.generators.models import GeneratorProtocol
from src.infra.api.mercadolivre.category import CategoryRequests

from src.app.shared.category.finders import IDFinderByPath


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
    """ Manages the generatrion, validation and selection of a product category. """
    def __init__(self):
        self.category_validator = CategoryValidator()
        self.category_requests = CategoryRequests()
        self.category_finder_by_path = IDFinderByPath()
    
    def generate(self, product: Product, token: AuthResponse) -> CategoryGeneratorResponse:
        """
        Generate the product category based on its data.
        Args:
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
        Returns:
            CategoryGeneratorResponse: The Meli category for the product.
        Todo:
            Validations:
                - [x] categoria         → This two are basicly the same operation.
                - [x] categoria_id      ↳ This two are basicly the same operation.
                - [x] categoria_caminho
                - [-] categoria_exemplo (depreacted)
                - [-] titulo (not used anymore)
        """
        causes: list[str] = []
        
        if product.category.categoria:
            categoria_response = self.__validate_category(product, token, product.category.categoria)
            if categoria_response.is_valid:
                log.user.info(f"A categoria da coluna categoria foi escolhida: {categoria_response.id_used}")
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_response.id_used
                )
            
            causes.append(f"Coluna categoria: {categoria_response.causes}")
        
        if product.category.categoria_id:
            categoria_id_response = self.__validate_category(product, token, product.category.categoria_id)
            if categoria_id_response.is_valid:
                log.user.info(f"A categoria da coluna categoria_id foi escolhida: {categoria_id_response.id_used}")
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_id_response.id_used
                )
            
            causes.append(f"Coluna categoria_id: {categoria_id_response.causes}")
        
        if product.category.categoria_caminho:
            categoria_caminho_response = self.__validate_category_path(product, token)
            if categoria_caminho_response.is_valid:
                log.user.info(f"A categoria da coluna categoria_caminho foi escolhida: {categoria_caminho_response.id_used}")
                return CategoryGeneratorResponse(
                    success=True,
                    result=categoria_caminho_response.id_used
                )
            
            causes.append(f"Coluna categoria_caminho: {categoria_caminho_response.causes}")
        
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
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
            category_id (str): Category ID.
        Returns:
            CategoryGeneratorValidationResponse:
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
            product (Product): A single product record.
            token (AuthResponse): Meli authentication credentials.
            category_id (str): Category ID.
        Returns:
            CategoryGeneratorValidationResponse:
        """
        
        finder_response = self.category_finder_by_path.find(product.category.categoria_caminho, token.access_token)
        if not finder_response.success:
            return CategoryGeneratorValidationResponse(causes=finder_response.error)
        
        return self.__validate_category(
            product=product,
            token=token,
            category_id=finder_response.result
        )
