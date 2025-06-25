""" Provides the status change of a product on mercado libre. """

from typing import Any

from src.core.log import log
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.db.models.produtos import Product
from src.infra.db.repositories import ProdutosRepository
from src.infra.db.repositories.models import ResponseCode
from src.app.shared.validators import ValidatorsProtocol, EmptyColumnsValidator, EmptyCredentialColumnsValidator
from .models import ProdutosOperationProtocol
from .tools import ProdutosValidator


class StatusChanger(ProdutosOperationProtocol):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository, 
        items_requests: ItemsRequests,
        edition_data: dict[str, Any],
        log_action_name: str,
        oper_status: str
    ) -> None:
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
        self.validator = ProdutosValidator(log, repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "identfiers.ml_id_produto"
            ])
        ]
        self.edition_data: dict[str, Any] = edition_data
        self.log_action_name: str = log_action_name
        self.oper_status = oper_status
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            self.repo.update.executing(id=line.id)
            self.operate(line=line, access_token=token.access_token)
    
    def operate(self, line: Product, access_token: str) -> None:
        """
        Realize the especialized operation.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to activate the product.
        """
        try:
            if not self.validator.validate(line, self.validators):
                return
            
            print(self.oper_status)
            
            response: MeliResponse = self.items_requests.edit(
                access_token=access_token,
                item_id=line.identfiers.ml_id_produto,
                edition_data=self.edition_data
            )
            
            if not response.success:
                self.log.dev.exception(str(response))
                self.repo.update.log_error(id=line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=response.error)
            
            status_product: str = response.data.get("status")
            print(f"{status_product = }")
            
            if status_product != self.oper_status:
                self.repo.update.log_error(id=line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=response.error)
            
            self.log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {self.log_action_name} com sucesso!")
            line.produto_status = status_product
            self.repo.update.change_status_success(line.id, line.produto_status)
        except Exception as e:
                log.dev.exception(f"{e}")
                self.repo.update.log_error(
                    id=line.id, 
                    cod_erro=ResponseCode.PROGRAM_ERROR, 
                    log_erro=f"Um erro inesperado ocorreu durante a operação: {e}"
                )
            

class Pause(StatusChanger):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ):
        super().__init__(
            log, 
            repo, 
            items_requests, 
            edition_data={"status":"paused"}, 
            log_action_name="pausado",
            oper_status="paused"
        )

class Activation(StatusChanger):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ):
        super().__init__(
            log, 
            repo, 
            items_requests, 
            edition_data={"status":"active"}, 
            log_action_name="ativação",
            oper_status="active"
        )

class Deletion(ProdutosOperationProtocol):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository, 
        items_requests: ItemsRequests
    ):
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
        self.validator = ProdutosValidator(log, repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "identfiers.ml_id_produto"
            ])
        ]
        self.edition_data: dict[str, str] = {"deleted": "true"}
        self.log_action_name: str = "deletado"
        self.allowed_status: tuple[str] = ("closed", "deleted")
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            causes: list[str] = []
            
            if not self.validator.validate(line, self.validators):
                continue
            
            self.repo.update.executing(id=line.id)
            self.delete(line=line, access_token=token.access_token, causes=causes)
    
    def delete(self, line: Product, access_token: str, causes: list) -> None:
        try:
            
            self._close(line, access_token, causes)
            delete_response = self._delete(line, access_token, causes)
            if not delete_response.success:
                return
            
            self._process_delete_result(line, delete_response, causes)
            
        except Exception as e:
            self._log_error(
                line=line, 
                operation="Deleção", 
                complement="erro inesperado", 
                causes=causes
            )
    
    def _process_delete_result(self, line: Product, delete_response: MeliResponse, causes: list) -> None:
        status_product: str = delete_response.data.get("status")
        delete_status: bool = delete_response.data.get("deleted")
        
        print(f"{status_product = }")
        print(f"{delete_status = }")
        
        if status_product not in self.allowed_status:
            causes.append(f"Status inválido: {status_product}. (Esperado: {self.allowed_status})")
            self._log_error(
                line=line, 
                causes=causes, 
                operation="Deleção", 
                complement="status inválido após exclusão"
            )
            return
        
        line.produto_status = status_product
        self._log_success(line)
    
    def _close(self, line: Product, access_token: str, causes: list) -> None:
        
        close_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status": "closed"}
        )
        
        if not close_response.success:
            causes.append(f"Erro de fechamento: {close_response.error}")
            self.log.dev.exception(f"{causes}")
        
        print("closed_response:", close_response.success)
    
    def _delete(self, line: Product, access_token: str, causes: list) -> MeliResponse:
        
        delete_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data=self.edition_data
        )
        
        if not delete_response.success:
            causes.append(f"Erro de deleção: {delete_response.error}")
            self._log_error(line, causes, "_Deleção")
            return delete_response
        
        if not delete_response.data:
            delete_response.success = False
            causes.append(f"Deleção nãou dados: {delete_response}")
            self._log_error(line, causes, "_Deleção")
            return delete_response
        
        return delete_response
    
    def _log_error(self, line: Product, causes: list, operation: str, complement: str = "falhou") -> None:
        error_msg: str = f"{operation} {complement}: {causes}"
        self.log.dev.exception(error_msg)
        self.repo.update.log_error(
            line.id, 
            cod_erro=ResponseCode.PROGRAM_ERROR, 
            log_erro=error_msg
        )
    
    def _log_success(self, line: Product):
        msg: str = (
            f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] "
            f"Produto {self.log_action_name} com sucesso!"
        )
        self.log.user.info(msg)
        self.repo.update.change_status_success(line.id, line.produto_status)
