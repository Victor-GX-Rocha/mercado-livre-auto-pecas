""" Generate the attributes list """

from src.core.log import logging
from src.infrastructure.database.models.produtos import Product
from src.infrastructure.api.mercadolivre.auth import AuthResponse

from ..models import GeneratorProtocol

from .validator import AttributesValidator
from .models import (
    AttributesResponse, 
    AttributeErrorDetail,
    AttributeErrorCause,
    AttributesValidatorResponse
)
from .generators import (
    AttributesGeneratorsProtocol,
    OriginGenerator,
    CompatibilityGenerator,
    CodificationGenrator,
    NomeationGenerator
)



class AttributesGenerator(GeneratorProtocol):
    """ Genrate the product attributes. """
    def __init__(self):
        self.generators: list[AttributesGeneratorsProtocol] = [
            OriginGenerator(),
            CompatibilityGenerator(),
            CodificationGenrator(),
            NomeationGenerator()
        ]
        self.validator = AttributesValidator()
    
    def generate(self, product: Product, token: AuthResponse) -> AttributesResponse:
        """
        Create the product attributes.
        Args:
            product (Product): Produtos dataclass table.
            token AuthResponse: Token for mercado libre requests.
        Returns:
            AttributesResponse: A AttributesResponse object with the attributes content. 
        """
        attributes: list[dict] = self._generate_attributes(product)
        validation_response: AttributesValidatorResponse = self.validator.validate(product, attributes, token)
        
        if not validation_response.is_valid:
            return AttributesResponse(
                success=False,
                result=None,
                error=AttributeErrorCause(
                    causes=validation_response.causes,
                    missing_values=[]
                )
            )
        
        return AttributesResponse(
            success=True,
            result=attributes
        )
    
    def _generate_attributes(self, product: Product) -> list[dict]:
        """
        Generate attrubutes.
        Args:
            product (Product): Produtos dataclass table.
        Returns:
            list[dict]: A list with the attributes dictionaries.
        """
        attributes: list[dict] = []
        warnings: list[AttributeErrorDetail] = []
        
        for generator in self.generators:
            try:
                if generated := generator.create(product):
                    attributes.extend(generated)
            except Exception as e:
                warnings.append(AttributeErrorDetail(
                    attribute_id=type(generator).__name__,
                    message=f"Falha ao gerar atributo: {str(e)}",
                    severity="warning"
                ))
        if warnings:
            logging.warning(warnings)
        return attributes
