
import os
import re
from typing import Any

from src.core.log import log
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.api.mercadolivre.catalog_compatibilities import CatalogCompatibilitiesRequests
from src.infra.db.models.produtos import Product
from src.infra.db.repositories import ProdutosRepository
from src.infra.db.repositories.models import ResponseCode
from src.app.shared.validators import (
    ValidatorsProtocol,
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator
)
from .models import ProdutosOperationProtocol
from ..generators import PayloadGenerator, PayloadGeneratorResponse

from .tools import ProdutosValidator


class PublicationErrorHandler:
    def __init__(self, log: log, repo: ProdutosRepository):
        self.log = log
        self.repo = repo
    
    def handle_publication_request(self, line, publication_response: MeliResponse) -> None:
        if self._is_logistic_erro(line, publication_response): # Especific error
            return
        self.repo.update.log_error(
            line.id, 
            cod_erro=ResponseCode.PROGRAM_ERROR, 
            log_erro=publication_response.error
        ) # Generic error
    
    def _is_logistic_erro(self, line, publication_response: MeliResponse) -> bool:
        
        fullfilment_not_allowed_error: str = '"message":"Client not allowed to update item null logistic_type."'
        if publication_response.error.details.find(fullfilment_not_allowed_error) != -1:
            self.repo.update.log_error(
                line.id, 
                cod_erro=ResponseCode.PROGRAM_ERROR, 
                log_erro='Seu perfil ainda não é autorizado a publicar no modo "fulfillment". Este modo só é liberado após o registro que pode ser realizado através desse link: https://envios.mercadolivre.com.br/vender-com-full/contato?openSea=true. Caso queira mais informação sobre o que é modo fulfillment: [O que é o full: https://www.mercadolivre.com.br/ajuda/O-que-e-o-Mercado-Envios-Full_5162, Como vender com o full: https://envios.mercadolivre.com.br/vender-com-full].'
            )
            return True
        return False

class Publication(ProdutosOperationProtocol):
    def __init__(
        self, 
        log: log, 
        repo: ProdutosRepository, 
        payload_generator: PayloadGenerator, 
        items_requests: ItemsRequests
    ) -> None:
        self.log = log
        self.repo = repo
        self.payload_generator = payload_generator
        self.items_requests = items_requests
        self.handler = PublicationErrorHandler(log, repo)
        self.validator = ProdutosValidator(log, repo)
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
        """
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            self.repo.update.executing(id=line.id)
            
            if not self.validate(line, self.validators):
                continue
            
            payload_response: PayloadGeneratorResponse = self.__create_payload(line, token)
            if not payload_response.success:
                continue
            
            publication_response: MeliResponse = self.__publish(line, token.access_token, payload_data=payload_response.result)
            if not publication_response.success:
                continue
            
            description_response: MeliResponse = self.__add_description(line, token.access_token)
            if not description_response.success:
                continue
            
            compatibility_response: MeliResponse = self.__add_compatibility(
                line=line, 
                access_token=token.access_token, 
                publication_data=publication_response.data
            )
            if not compatibility_response.success:
                continue
            
            self.__register_publication_success(line=line, publication_data=publication_response.data)
    
    def __create_payload(self, line: Product, token: AuthResponse) -> PayloadGeneratorResponse:
        """
        Creates a dictionary with publication data.
        Args:
            line Product: Product dataclass table line.
        Returns:
            (dict[str, Any]): A dictiornary with the product payload data
        """
        payload_response = self.payload_generator.build_publication_payload(product=line, token=token)
        if not payload_response.success:
            self.repo.update.log_error(line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=payload_response.error)
        return payload_response
    
    def __publish(self, line: Product, access_token: str, payload_data: dict[str, Any]) -> MeliResponse:
        """
        Publish a the current product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to publish the product.
            payload_data (dict[str, Any]): Payload publication data.
        Returns:
            MeliResponse:
        """
        publication_response = self.items_requests.publish(
            access_token=access_token,
            publication_data=payload_data
        )
        
        if not publication_response.success:
            self.log.dev.error(str(publication_response))
            self.handler.handle_publication_request(line, publication_response)
            return publication_response
        
        line.identfiers.ml_id_produto = publication_response.data.get("id")
        ml_id: str = publication_response.data.get("id", "Ml ID não retornado")
        link: str = publication_response.data.get("permalink", "Link não encontrado")
        cod_produto: str = line.identfiers.cod_produto
        
        self.__register_publication(
            ml_id=ml_id, 
            link=link, 
            cod_produto=cod_produto
        )
        
        self.log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {line.sale.titulo} publicado com sucesso!")
        
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
            self.log.dev.error(str(descripition_response))
            self.repo.update.log_error(line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=descripition_response.error)
        
        self.log.user.info("Descrição adicionada com sucesso.")
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
        if not all([line.technical.marcas_ids, line.technical.modelos_ids, line.technical.anos_ids]):
            self.log.user.warning(f"As colunas de ID de compatibilidade não foram preenchidas.")
            return MeliResponse(success=True, data="Item não necessita de compatibilidade.")
        
        product_id: str = publication_data["id"]
        marcas_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.marcas_ids)]
        modelos_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.modelos_ids)]
        anos_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.anos_ids)]
        
        
        compatibilities_response = self.comp_requests.get_compatibilities(
            access_token=access_token,
            brand_ids=marcas_ids,
            model_ids=modelos_ids,
            years_ids=anos_ids
        )
        
        if not compatibilities_response.success:
            self.repo.update.log_error(line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=compatibilities_response.error)
            return compatibilities_response
        
        compatibilities_ids: list[str] = [result["id"] for result in compatibilities_response.data["results"]]
        
        compatibility_addition_response = self.items_requests.add_compatibilities(
            access_token=access_token, 
            product_id=product_id, 
            items_ids=compatibilities_ids
        )
        
        if not compatibility_addition_response.success:
            self.log.dev.error(str(compatibility_addition_response))
            self.repo.update.log_error(line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=compatibility_addition_response.error)
        
        return compatibility_addition_response
    
    def __register_publication(self, ml_id: str, link: str, cod_produto: str) -> None:
        """
        Register the publication ID, link, and the product ineternal code inside a .ml file.
        Args:
            ml_id (str): Publication ID.
            link (str): Publication link.
            cod_produto (str): Product internal code.
        """
        
        if not os.path.exists('retorno'):
            os.makedirs('retorno')
        
        file = f"retorno/{cod_produto}.ml"
        with open(file, "a", encoding="utf-8") as log_file:
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
        category_id: str = publication_data.get("category_id")
        status: str = publication_data.get("status")
        
        self.repo.update.publication_success(
            line.id,
            ml_id_produto=ml_id,
            categoria=category_id,
            link_publicacao=link,
            produto_status=status
        )
        print(f"self.repo.update.publication_success")
