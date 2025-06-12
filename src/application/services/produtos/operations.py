"""  """

from typing import Protocol, Any, runtime_checkable

from ....infrastructure.api.mercadolivre.auth import AuthResponse
from ....infrastructure.database.models.produtos import Product
from ....infrastructure.database.repositories import ProdutosRepository
from ...shared.validators import (
    ValidatorsProtocol,
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator
)
from ...shared.models import ValidationResponse
from .generators import JsonGenerator, JsonGeneratorResponse


runtime_checkable
class ProdutosOperation(Protocol):
    # def __init__(self, repo: ProdutosRepository):
    #     ...
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        ...


class Publication(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository, json_generator: JsonGenerator):
        self.repo = repo
        self.json_generator = json_generator
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "sale.imagens",
                "sale.preco",
                "sale.tipo_anuncio"
            ])
        ]
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        """
        - [x] Validate
        - [ ] Create the json
        - [ ] Publish
        - [ ] Add a description
        - [ ] Add compatibility
        - [ ] Update the database
        """
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            if not self.validate(line):
                continue
            
            json_response = self.create_json()
            if not json_response.success:
                continue
            
            # self.create_json()
            # self.publish()
            # self.add_description()
            # self.add_compatibility()
            ## self.update the database
    
    def create_json(self, line: Product) -> JsonGeneratorResponse:
        """
        Creates a dictionary with publication data.
        Args:
            line (list[Product]): 
        Returns:
            (list[dict[str, Any]]):
            None: If any error occurred.
        """
        json_response = self.json_generator.build_json(line)
        if not json_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=json_response.error)
        return json_response
    
    def publish(self):...
    def add_description(self):...
    def add_compatibility(self):...
    
    def validate(self, line: Product) -> bool:
        """
        Vaidate if the product is able to be updloaded.
        Args:
            line (Product): 
        Returns:
            bool: True if valid, else False.
        """
        causes: list = []
        for validator in self.validators:
            response = validator.validate(line)
            if not response.is_valid:
                causes.append(response.causes)
        if causes:
            self.repo.update.log_error(line.id, cod_erro=88, log_erro=causes)
            return False
        return True




class Edition(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository, json_generator: JsonGenerator):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Pause(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Activation(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Deletation(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

