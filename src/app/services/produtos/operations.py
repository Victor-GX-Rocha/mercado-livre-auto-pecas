""" Product table operations. """

import os
import re
from typing import Protocol, Any, runtime_checkable

from src.core.log import log
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.api.mercadolivre.catalog_compatibilities import CatalogCompatibilitiesRequests
from src.infra.db.models.produtos import Product
from src.infra.db.repositories import ProdutosRepository
from src.app.shared.models import ValidationResponse
from src.app.shared.validators import (
    ValidatorsProtocol,
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator
)
from .generators import PayloadGenerator, PayloadGeneratorResponse


@runtime_checkable
class ProdutosOperation(Protocol):
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        ...

class JustSleep:
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        """ Change the status operation to another number to make it "sleep" """
        
        for line in lines:
            self.repo.update.got_to_sleep(line.id)

class InvalidOperation:
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        """ Allerts the user that this operation do not exists. """
        
        for line in lines:
            self.repo.update.log_error(line.id, cod_erro=88, log_erro=f"Operação inválida: {line.controlers.operacao}")


class Publication(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository, payload_generator: PayloadGenerator, items_requests: ItemsRequests):
        self.repo = repo
        self.payload_generator = payload_generator
        self.items_requests = items_requests
        self.comp_requests = CatalogCompatibilitiesRequests()
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "sale.imagens",
                "sale.preco",
                "sale.tipo_anuncio",
                "technical.marcas_ids",
                "technical.modelos_ids",
                "technical.anos_ids"
                
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
            if not self._validate(line):
                continue
            
            payload_response: PayloadGeneratorResponse = self.__create_payload(line, token=token)
            if not payload_response.success:
                continue
            
            publication_response: MeliResponse = self.__publish(line, token.access_token, payload_data=payload_response.result)
            if not publication_response.success:
                continue
            
            description_response: MeliResponse = self.__add_description(line, access_token=token.access_token)
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
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=payload_response.error)
        print(f"Payload criado com sucesso: payload_response")
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
            log.dev.error(str(publication_response))
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=publication_response.error)
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
        
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {line.sale.titulo} publicado com sucesso!")
        
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
            log.dev.error(str(descripition_response))
            self.repo.update.log_error(line.id, cod_erro=89, log_erro=descripition_response.error)
        
        print(f"Descrição atualizada com sucesso: description_response")
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
        marcas_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.marcas_ids)]
        modelos_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.modelos_ids)]
        anos_ids: list[str] = [id for id in re.split(r'[;,]', line.technical.anos_ids)]
        
        
        compatibilities_response = self.comp_requests.get_compatibilities(
            access_token=access_token,
            brand_ids=marcas_ids,
            model_ids=modelos_ids,
            years_ids=anos_ids
        )
        
        # print(str(compatibilities_response))
        
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
            log.dev.error(str(compatibility_addition_response))
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
            log.user.warning(f"{causes}")
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
        print(f"__register_publication")
        
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
        print(f"__register_publication_success")
        ml_id: str = publication_data.get("id", "Ml ID não retornado")
        link: str = publication_data.get("permalink", "Link não encontrado")
        cod_produto: str = line.identfiers.cod_produto
        category_id: str = publication_data.get("category_id")
        status: str = publication_data.get("status")
        
        self.repo.update.publication_success(
            line.id,
            ml_id_produto=ml_id,
            categoria=category_id,
            link_publicacao=link,
            produto_status=status,
            status_operacao_id=2
        )
        print(f"self.repo.update.publication_success")




class Edition(ProdutosOperation):
    def __init__(
        self, 
        repo: ProdutosRepository,
        items_requests: ItemsRequests,
        payload_generator: PayloadGenerator
    ) -> None:
        self.repo = repo
        self.items_requests = items_requests
        self.payload_generator = payload_generator
        
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            fails: list[str] = []
            
            try:
                # Pause:
                pause_response: MeliResponse = self.items_requests.edit(
                    access_token=token.access_token,
                    item_id=line.identfiers.ml_id_produto,
                    edition_data={"status":"paused"}
                )
                
                log.dev.info(f"[BD-ID {line.id}] Pausando o produto")
                if not pause_response.success:
                    log.dev.exception(str(pause_response))
                    self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=pause_response.error)
                    return
                
                
                # Editing:
                
                # - Change description
                get_description_response = self.items_requests.get_description(
                    access_token=token.access_token,
                    item_id=line.identfiers.ml_id_produto
                )
                
                if get_description_response.success:
                    if not get_description_response.data.get("plain_text"):
                        description_response = self.items_requests.add_description(
                            access_token=token.access_token, 
                            item_id=line.identfiers.ml_id_produto,
                            descrption=line.sale.descricao
                        )
                        if not description_response.success:
                            log.user.warning(f"Falha no processo de adicionar a descrição: {description_response.error}")
                            fails.append(description_response.error)
                            
                    if line.sale.descricao != get_description_response.data.get("plain_text"):
                        description_response = self.items_requests.add_description(
                            access_token=token.access_token, 
                            item_id=line.identfiers.ml_id_produto,
                            descrption=line.sale.descricao,
                            change_description=True
                        )
                        if not description_response.success:
                            log.user.warning(f"Falha no processo de mudança da descrição: {description_response.error}")
                            fails.append(description_response.error)
                
                
                # - Change another data
                
                # - - Get product data
                product_data_response: MeliResponse = self.items_requests.get_item_info(
                    access_token=token.access_token,
                    item_id=line.identfiers.ml_id_produto
                )
                
                if product_data_response.success:
                    
                    edition_payload: PayloadGeneratorResponse = self.payload_generator.build_edition_payload(
                        product=line,
                        product_data=product_data_response.data,
                        token=token
                    )
                    
                    if not edition_payload.success:
                        log.user.warning(f"Falha no processo de edição dos dados do produto: {edition_payload.error}")
                        fails.append(edition_payload.error)
                else:
                    log.user.warning(f"Falha no processo de obter dados do produto: {product_data_response.error}")
                    fails.append(product_data_response.error)
                
                
                # Reactivating:
                activate_response: MeliResponse = self.items_requests.edit(
                    access_token=token.access_token,
                    item_id=line.identfiers.ml_id_produto,
                    edition_data={"status":"active"}
                )
                
                log.dev.info(f"[BD-ID {line.id}] Reativando o produto")
                if not activate_response.success:
                    log.user.warning(str(activate_response))
                    fails.append(f"Falha no processo de reativação produto {activate_response.error}")
                
                if fails:
                    self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=fails)
                    return
                
                log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {line.sale.titulo} editado com sucesso!")
                self.repo.update.log_success_code(id=line.id)
                
            except Exception as e:
                message: str = f"Exceção inesperada durante o processo de edição: fails:{fails} Exc: {e}"
                log.dev.exception(message)
                self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=message)
                



# Turn back to here to apply DRY in this classes

class Pause(ProdutosOperation):
    def __init__(
        self, 
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ) -> None:
        self.repo = repo
        self.items_requests = items_requests
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                # "produto_status"
                "identfiers.ml_id_produto"
            ])
        ]
        self.oper_status: str = "paused"
        self.log_action_name: str = "pausado"
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        """  
        # When I try to edit a product, I need to verify if his status is the same of the editatiton that I'm doing!
        # There is possible that the request works, but the status is not changed.
        """
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            self.pause(line=line, access_token=token.access_token)
    
    def pause(self, line: Product, access_token: str) -> None:
        """
        Pause a product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to pause the product.
        """
        
        if not self._validate(line):
            return
        
        pause_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status": self.oper_status}
        )
        
        if not pause_response.success:
            log.dev.exception(str(pause_response))
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=pause_response.error)
        
        if pause_response.data.get("status") != self.oper_status:
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=pause_response.error)
        
        status_product: str = pause_response.data.get("status")
        
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {self.log_action_name} com sucesso!")
        line.produto_status = status_product
        self.repo.update.pause_success(line.id, line.produto_status)
    
    def _validate(self, line: Product) -> bool:
        """
        Vaidate if the product is able to be paused.
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
            log.user.warning(f"{causes}")
            self.repo.update.log_error(line.id, cod_erro=88, log_erro=causes)
            return False
        return True

class Activation(ProdutosOperation):
    def __init__(
        self, 
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ) -> None:
        self.repo = repo
        self.items_requests = items_requests
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                # "produto_status"
                "identfiers.ml_id_produto"
            ])
        ]
        self.oper_status: str = "active"
        self.log_action_name: str = "ativado"
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            self.activate(line=line, access_token=token.access_token)
    
    def activate(self, line: Product, access_token: str) -> None:
        """
        Activate a product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to activate the product.
        """
        
        if not self._validate(line):
            return
        
        print(self.oper_status)
        
        pause_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status": self.oper_status}
        )
        
        if not pause_response.success:
            log.dev.exception(str(pause_response))
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=pause_response.error)
        
        status_product: str = pause_response.data.get("status")
        print(f"{status_product = }")
        
        if status_product != self.oper_status:
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=pause_response.error)
        
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {self.log_action_name} com sucesso!")
        line.produto_status = status_product
        self.repo.update.activation_success(line.id, line.produto_status)
    
    def _validate(self, line: Product) -> bool:
        """
        Vaidate if the product is able to be paused.
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
            log.user.warning(f"{causes}")
            self.repo.update.log_error(line.id, cod_erro=88, log_erro=causes)
            return False
        return True

class Deletation(ProdutosOperation):
    def __init__(
        self, 
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ) -> None:
        self.repo = repo
        self.items_requests = items_requests
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                # "produto_status"
                "identfiers.ml_id_produto"
            ])
        ]
        self.oper_status: str = "deleted"
        self.log_action_name: str = "excluído"
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            self.delete(line=line, access_token=token.access_token)
    
    def delete(self, line: Product, access_token: str) -> None:
        """
        Delete a product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to delete the product.
        """
        
        if not self._validate(line):
            return
        
        print(self.oper_status)
        causes: list[str] = []
        
        closed_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status": "closed"}
        )
        
        if not closed_response.success:
            log.dev.exception(str(closed_response))
            causes.append(str(closed_response.error))
            # self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=closed_response.error)
        
        print("closed_response:", closed_response.success)
        
        # Delete response
        
        delete_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"deleted": "true"}
        )
        
        if not delete_response.success:
            log.dev.exception(str(delete_response))
            causes.append(str(delete_response.error))
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=causes)
            return
        
        
        if not delete_response.data:
            return
        
        
        status_product: str = delete_response.data.get("status")
        print(f"{status_product = }")
        print(f"{delete_response.data.get("deleted") = }")
        
        if status_product not in ("closed", "deleted"):
            self.repo.update.log_error(id=line.id, cod_erro=89, log_erro=delete_response.error)
            return
        
        
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto deletado com sucesso!")
        line.produto_status = status_product
        self.repo.update.deletation_success(line.id, line.produto_status)
    
    def _validate(self, line: Product) -> bool:
        """
        Vaidate if the product is able to be deleted.
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
            log.user.warning(f"{causes}")
            self.repo.update.log_error(line.id, cod_erro=88, log_erro=causes)
            return False
        return True
