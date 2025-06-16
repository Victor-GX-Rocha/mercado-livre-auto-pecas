""" Product table operations. """

import os
from typing import Protocol, Any, runtime_checkable

from src.infrastructure.api.mercadolivre.auth import AuthResponse
from src.infrastructure.api.mercadolivre.items import ItemsRequests
from src.infrastructure.api.mercadolivre.models import MeliResponse
from src.infrastructure.database.models.produtos import Product
from src.infrastructure.database.repositories import ProdutosRepository
from src.application.shared.models import ValidationResponse
from src.application.shared.validators import (
    ValidatorsProtocol,
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator
)
from .generators import JsonGenerator, JsonGeneratorResponse



runtime_checkable
class ProdutosOperation(Protocol):
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        ...


class Publication(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
        self.json_generator = JsonGenerator()
        self.items_requests = ItemsRequests()
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
        - [x] Create the json
        - [x] Publish
        - [x] Add a description
        - [ ] Add compatibility
        - [ ] Update the database
        """
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            if not self.validate(line):
                continue
            
            json_response: JsonGeneratorResponse = self.create_json(line, token)
            if not json_response.success:
                continue
            
            publication_response: MeliResponse = self.publish(line, token.access_token, publication_data=json_response.result)
            if not publication_response.success:
                continue
            
            description_response: MeliResponse = self.add_description(line=line, access_token=token.access_token)
            if not description_response.success:
                continue
            
            compatibility_response = self.add_compatibility(line=line, access_token=token.access_token)
            if not compatibility_response.success:
                continue
            
            self.register_publication_success()

    
    def create_json(self, line: Product, token: AuthResponse) -> JsonGeneratorResponse:
        """
        Creates a dictionary with publication data.
        Args:
            line Product: Product dataclass table line.
        Returns:
            (dict[str, Any]): A dictiornary with the product json data
        """
        json_response = self.json_generator.build_publication_json(product=line, token=token)
        if not json_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=json_response.error)
        return json_response
    
    def publish(self, line: Product, access_token: str, publication_data: dict[str, Any]) -> MeliResponse:
        """
        Publish a the current product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to publish the product.
            publication_data (dict[str, Any]): Product data.
        Returns:
            MeliResponse:
        """
        publication_response = self.items_requests.publish(
            access_token=access_token, 
            publication_data=publication_data
        )
        
        if not publication_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=publication_response.error)
            return publication_response
        
        line.identfiers.ml_id_produto = publication_response.data.get("id")
        
        return publication_response
    
    def add_description(self, line: Product, access_token: str) -> MeliResponse:
        """
        Adds the product description.
        Args:
            line (Product): Product dataclass table line.
            access_token (str): Access token to make add description request.
        Returns:
            MeliResponse:
        """
        descripition_response: MeliResponse = self.items_requests.add_description(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            descrption=line.sale.descricao
        )
        
        if not descripition_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=descripition_response.error)
        
        return descripition_response
    
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
    
    def register_publication(self, ml_id: str, link: str, cod_produto: str) -> None:
        """
        
        Args:
            ml_id (str): 
            link (str): 
            cod_produto (str):
        """
        
        if not os.path.exists('retorno'):
            os.makedirs('retorno')
        
        arquivo = f"retorno/{cod_produto}.ml"
        with open(arquivo, "a", encoding="utf-8") as log_file:
            log_file.write(f"Ml ID: {ml_id}\n")
            log_file.write(f"Link: {link}\n")
            log_file.write("----------" * 4 + "\n")

    def register_publication_success(self):
        self.register_publication()
        self.repo.update.publication_success(line.id, status_operacao_id=2, categoria=publication_response.get("category_id"))
        # self.add_compatibility()
        ## self.update the database

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

