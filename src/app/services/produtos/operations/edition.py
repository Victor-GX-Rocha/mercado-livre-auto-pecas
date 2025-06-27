"""
Product edition operetarions on mercado libre.

This module implements the complete edition flow for mercado libre products.
- Initial validation.
- Description atualization.
- Temporary pause.
- Edition payload construction.
- Edition execution.
- Product reactivation.
- Errors treatment and rollback.

Provides:
    Edition: Main class who implements the edition flow.
    EditionAbortError: Excpetion for controled errors during the executiong flow.
"""

from src.core.log import log
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.db.models.produtos import Product
from src.infra.db.repo import ProdutosRepository
from src.infra.db.repo.models import ResponseCode
from src.app.shared.validators import (
    ValidatorsProtocol,
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator
)

from ..generators import PayloadGenerator, PayloadGeneratorResponse
from .models import ProdutosOperationProtocol
from .tools import ProdutosValidator


class EditionAbortError(Exception):
    """
    Exception thrown when an edit operation is aborted due to an expected error.
    
    This exception is used for errors that occur during the execution of editing steps and are considered recorveble or should interrupt the flow in a controlled manner.
    """
    def __init__(self, *args):
        super().__init__(*args)


class Edition(ProdutosOperationProtocol):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository,
        items_requests: ItemsRequests,
        payload_generator: PayloadGenerator
    ) -> None:
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
        self.payload_generator = payload_generator
        self.validator = ProdutosValidator(log, repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "identfiers.ml_id_produto"
            ])
        ]
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        """
        Validate and excute the edit operation for each operation line. 
        Args:
            line (Product): A list of database product lines as a dataclasses.
            token (AuthResponse): Token object with access token.
        """
        print(f"Executando {self.__class__.__name__}")
        
        for line in lines:
            self.current_step = None
            
            if not self.validator.validate(line, self.validators): # Já arualiza o banco com logs de validação.
                continue
            
            self.edit(line, token)
    
    def edit(self, line: Product, token: AuthResponse) -> None:
        """
        Manage the methods responsible for make the editation steps.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        """
        try:
            
            product_data: MeliResponse | None = None
            self.repo.update.executing(id=line.id)
            
            description_response: MeliResponse = self._update_description(line, token)
            product_data_response: MeliResponse = self._get_product_data(line, token)
            product_data_response: MeliResponse = self._pause(line, token, product_data_response) 
            edition_payload: PayloadGeneratorResponse = self._build_edition_payload(line, token, product_data_response)
            product_data_response: MeliResponse = self._edit(line, token, edition_payload)
            product_data_response: MeliResponse = self._reactive(line, token, product_data_response)              
            
            self._log_succss(line)
            
        except EditionAbortError as e:
            msg: str = (f"[Produto ID: {line.id}] Falha na edição - Etapa: {self.current_step} | Erro: {e}")
            log.dev.exception(msg)
            self.repo.update.log_error(
                id=line.id,
                return_code=ResponseCode.PROGRAM_ERROR, 
                log_erro=msg
            )
            self._reactive(line, token, product_data=product_data_response)
            
        except Exception as e:
            msg: str = f"Falha inesperada durante o processo de edição do produto: \nExc: {e}"
            log.dev.exception(msg)
            self.repo.update.log_error(
                id=line.id,
                return_code=ResponseCode.PROGRAM_ERROR, 
                log_erro=msg
            )
            self._reactive(line, token, product_data=product_data_response)
        
        except Exception as e:
            error_type = "AbortError" if isinstance(e, EditionAbortError) else "inesperado"
            msg = f"[Produto ID: {line.id}] Falha {error_type} - Etapa: {self.current_step} | Erro: {e}"
            
            log.dev.exception(msg)
            self.repo.update.log_error(
                id=line.id,
                return_code=ResponseCode.PROGRAM_ERROR, 
                log_erro=msg
            )
            
            self._reactive(line, token, product_data)
        finally:
            self.current_step = None
    
    def _get_product_data(self, line: Product, token: AuthResponse) -> MeliResponse:
        """ 
        Gets the product data.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        Returns:
            MeliResponse:
        """
        self.current_step = "Obter dados do produto"
        
        product_data_response: MeliResponse = self.items_requests.get_item_info(
            access_token=token.access_token,
            item_id=line.identfiers.ml_id_produto
        )
        
        if not product_data_response.success:
            raise EditionAbortError(f"Falha no processo de obter dados do produto: {product_data_response.error}")
        
        return product_data_response
    
    def _build_edition_payload(self, line: Product, token: AuthResponse, product_data: MeliResponse) -> MeliResponse:
        """ 
        Build the edition payload with product data. Necessary to make the edititon request.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
            product_data (MeliResponse):
        Returns:
            MeliResponse:
        """
        self.current_step = "Construir o payload de edição do produto"
        
        edition_payload: MeliResponse = self.payload_generator.build_edition_payload(
            product=line,
            product_data=product_data.data,
            token=token
        )
        
        print(f"{edition_payload = }")
        
        if not edition_payload.success:
            raise EditionAbortError(f"Falha no processo de geração dados de edição do produto: {edition_payload.error}")
        
        return edition_payload

    def _update_description(self, line: Product, token: AuthResponse) -> MeliResponse:
        """
        Identifies if a update on product description is necessery, if it is, update it.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        Returns:
            MeliResponse:
        """
        try:
            get_description_response = self.items_requests.get_description(
                access_token=token.access_token,
                item_id=line.identfiers.ml_id_produto
            )
            
            if not get_description_response.success:
                raise EditionAbortError(f"Falha ao obter dados de descrição durante o processo de edição.")
            
            description_plain_text: str = get_description_response.data.get("plain_text")
            
            if not description_plain_text:
                add_description_response = self._add_description(line, token)
                return add_description_response
            
            self._change_description(line, token, description_plain_text)
        except EditionAbortError:
            raise
        except Exception as e:
            raise EditionAbortError(f"Falha inesperada na descrição: {e}") from e
    
    def _add_description(self, line: Product, token: AuthResponse, change_description: bool = False) -> MeliResponse:
        """
        Adds a description for a product.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
            change_description (bool): If true, overwrite the description.
        Returns:
            MeliResponse:
        """
        add_description_response = self.items_requests.add_description(
            access_token=token.access_token, 
            item_id=line.identfiers.ml_id_produto,
            descrption=line.sale.descricao,
            change_description=change_description
        )
        if not add_description_response.success:
            raise EditionAbortError(f"Falha no processo de adicionar a descrição: {add_description_response.error}")
        
        return add_description_response
    
    def _change_description(self, line: Product, token: AuthResponse, description_plain_text: str) -> None:
        """
        If it has a description, and it's diferent, change it.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
            description_plain_text (str): Atual description of a published product.
        """
        
        if line.sale.descricao == description_plain_text:
            return
        
        self._add_description(
            line=line,
            token=token,
            change_description=True
        )
    
    def _pause(self, line: Product, token: AuthResponse, product_data: MeliResponse) -> MeliResponse | None:
        """
        Pause the product before editing to avoid inconsistency errors on user account.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        Returns:
            MeliResponse:
        """
        self.current_step = "Pausar o produto"
        
        status: str = product_data.data.get("status")
        if status == "paused":
            return product_data
        
        pause_response: MeliResponse = self.items_requests.edit(
            access_token=token.access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status":"paused"}
        )
        
        log.dev.info(f"[BD-ID {line.id}] Pausando o produto")
        if not pause_response.success:
            raise EditionAbortError(f"Falha no processo de pausar o produto para edição. Editar um produto ativo pode causar problemas de venda, processo pulado para fins de segurança. Error response: {pause_response.error}")
        
        return pause_response
    
    def _edit(self, line: Product, token: AuthResponse, edition_payload: PayloadGeneratorResponse) -> MeliResponse:
        """
        Change the product data.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
            edition_payload (PayloadGeneratorResponse):
        """
        self.current_step = "Realizar a requisição de edição do produto"
        
        edition_response: MeliResponse = self.items_requests.edit(
            access_token=token.access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data=edition_payload.result
        )
        
        print(f"{edition_response = }")
        
        if not edition_response.success:
            raise EditionAbortError(f"Falha no comando de edição do produto: {edition_response}")
        
        return edition_response
    
    def _reactive(self, line: Product, token: AuthResponse, product_data: MeliResponse) -> MeliResponse:
        """
        Reative the product after the aditation.
        Args:
            line (Product): Database product line as a dataclass.
            token (AuthResponse): Token object with access token.
        """
        
        # if not product_data: # If has no data, the product was not paused, then skip.
        #     return
        
        # if not hasattr(product_data, "data"): # If it don't have the data attribute, the edit request failed, so ther's no sense in do another
        #     return
        
        # if product_data.data: # Data pode ser None
        
        if not product_data or not hasattr(product_data, "data"):
            return
        
        status: str = product_data.data.get("status")
        if status == "active":
            return product_data
        
        if self.current_step == "Reativar o produto": # If a reactive tentative already failed, skip.
            return
        
        self.current_step = "Reativar o produto"
        
        activate_response: MeliResponse = self.items_requests.edit(
            access_token=token.access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status":"active"}
        )
        
        log.dev.info(f"[BD-ID {line.id}] Reativando o produto")
        if not activate_response.success:
            raise EditionAbortError(f"Falha no processo de reativação produto {activate_response.error}")
        
        return activate_response
    
    def _log_succss(self, line: Product) -> None:
        """
        Log a success message on database.
        Args:
            line (Product): Database product line as a dataclass.
        """
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {line.sale.titulo} editado com sucesso!")
        self.repo.update.log_success_code(id=line.id)
