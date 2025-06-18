""" Product table operations. """

import os
from typing import Protocol, Any, runtime_checkable

from src.infrastructure.api.mercadolivre.auth import AuthResponse
from src.infrastructure.api.mercadolivre.items import ItemsRequests
from src.infrastructure.api.mercadolivre.models import MeliResponse
from src.infrastructure.api.mercadolivre.catalog_compatibilities import CatalogCompatibilitiesRequests
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
        self.comp_requests = CatalogCompatibilitiesRequests()
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
        Publish a product on mercado libre.
        Args:
            lines (list[Product]): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        Todo:
            - [x] Validate
            - [x] Create the json
            - [x] Publish
            - [x] Add a description
            - [x] Add compatibility
            - [x] Update the database
        """
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            if not self._validate(line):
                continue
            
            json_response: JsonGeneratorResponse = self.__create_json(line=line, token=token)
            if not json_response.success:
                continue
            
            publication_response: MeliResponse = self.__publish(line, token.access_token, publication_data=json_response.result)
            if not publication_response.success:
                continue
            
            description_response: MeliResponse = self.__add_description(line=line, access_token=token.access_token)
            if not description_response.success:
                continue
            
            compatibility_response: MeliResponse = self.__add_compatibility(
                line=line, 
                access_token=token.access_token, 
                publication_data=json_response.result
            )
            if not compatibility_response.success:
                continue
            
            self.__register_publication_success(line=line, publication_data=publication_response.data)
    
    def __create_json(self, line: Product, token: AuthResponse) -> JsonGeneratorResponse:
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
    
    def __publish(self, line: Product, access_token: str, publication_data: dict[str, Any]) -> MeliResponse:
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
    
    def __add_description(self, line: Product, access_token: str) -> MeliResponse:
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
    
    def __add_compatibility(self, line: Product, access_token: str, publication_data: dict) -> MeliResponse:
        """
        Adds a list of compatibilities to the product.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to publish the product.
            publication_data (dict[str, Any]): Product data.
        Returns:
            MeliResponse:
        """
        
        product_id: str = publication_data["id"]
        
        compatibilities_response = self.comp_requests.get_compatibilities(
            access_token=access_token,
            brand_ids=line.technical.marcas_ids,
            model_ids=line.technical.modelos_ids,
        )
        
        if not compatibilities_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=compatibilities_response.error)
            return compatibilities_response
        
        compatibilities_ids: list[str] = [result["id"] for result in compatibilities_response.data["results"]]
        
        compatibility_addition_response = self.items_requests.add_compatibilities(
            access_token=access_token, 
            product_id=product_id, 
            items_ids=compatibilities_ids
        )
        
        if not compatibility_addition_response.success:
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=compatibility_addition_response.error)
        
        return compatibility_addition_response
    
    def _validate(self, line: Product) -> bool:
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
    
    def __register_publication(self, ml_id: str, link: str, cod_produto: str) -> None:
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
    
    def __register_publication_success(self, line: Product, publication_data: dict) -> None:
        """
        Register the publication results on the database.
        Args:
            line (Product):
            publication_data (dict):
        """
        ml_id: str = publication_data.get("id", "Ml ID não retornado")
        link: str = publication_data.get("permalink", "Link não encontrado")
        cod_produto: str = line.identfiers.cod_produto
        category_id: str = publication_data.get("category_id")
        status: str = publication_data.get("status")
        
        self.__register_publication(
            ml_id=ml_id, 
            link=link, 
            cod_produto=cod_produto
        )
        
        self.repo.update.publication_success(
            line.id,
            ml_id_produto=ml_id,
            categoria=category_id,
            link_publicacao=link,
            produto_status=status,
            status_operacao_id=2
        )

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

