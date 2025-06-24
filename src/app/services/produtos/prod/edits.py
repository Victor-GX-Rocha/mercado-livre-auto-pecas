""" Edit a product on mercado libre. """

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


class Editor(ProdutosOperationProtocol):
    def __init__(
        self,
        log: log,
        repo: ProdutosRepository, 
        items_requests: ItemsRequests,
        edition_data: dict[str, Any],
        log_action_name: str,
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


class Pause(Editor):
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
            log_action_name="pausado"
        )

class Activation(Editor):
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
            log_action_name="ativação"
        )


class Deletation(ProdutosOperationProtocol):
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
        self.edition_data={"deleted": "true"}, 
        self.log_action_name="deletado"
        self.allowed_status: tuple[str] = ("closed", "deleted")
    
    def execute(self, lines: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")
        for line in lines:
            self.repo.update.executing(id=line.id)
            self.operate(line=line, access_token=token.access_token)
    
    def _close(self, line: Product, access_token: str, causes: list) -> MeliResponse:
        
        closed_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data={"status": "closed"}
        )
        
        if not closed_response.success:
            self.log.dev.exception(str(closed_response))
            causes.append(str(closed_response.error))
            closed_response.error=causes
        
        print("closed_response:", closed_response.success)
        return closed_response
    
    def _delete(self, line: Product, access_token: str, causes: list) -> MeliResponse:
        
        delete_response: MeliResponse = self.items_requests.edit(
            access_token=access_token,
            item_id=line.identfiers.ml_id_produto,
            edition_data=self.edition_data
        )
        
        if not delete_response.success:
            self.log.dev.exception(str(delete_response))
            causes.append(str(delete_response.error))
            self.repo.update.log_error(id=line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=causes)
            delete_response.error = causes
        
        return delete_response
    
    def operate(self, line: Product, access_token: str) -> None:
        """
        Delete a product on mercado libre.
        Args:
            line Product: Product dataclass table line.
            access_token (str): Access token to delete the product.
        """
        
        if not self.validator.validate(line, self.validators):
            return
        
        causes: list[str] = []
        
        closed_response = self._close(line, access_token, causes)
        delete_response = self._delete(line, access_token, causes)
        causes.extend()
        causes.extend()
        
        if not delete_response.data: # To avoid index errors
            return
        
        
        status_product: str = delete_response.data.get("status")
        delete_status: bool = delete_response.data.get("deleted")
        
        print(f"{status_product = }")
        print(f"{delete_status = }")
        
        if status_product not in self.allowed_status:
            causes.append({"O item não estabaleceu um dos estados": self.allowed_status})
            causes.append({"Estados estabelecidos": f"Status: {status_product} | Delete status: {delete_status}"})
            causes.append({"Delete response error": delete_response.error})
            self.repo.update.log_error(id=line.id, cod_erro=ResponseCode.PROGRAM_ERROR, log_erro=causes)
            return
        
        
        log.user.info(f"[DB-ID: {line.id} | Cod: {line.identfiers.cod_produto}] Produto {self.log_action_name} com sucesso!")
        line.produto_status = status_product
        self.repo.update.change_status_success(line.id, line.produto_status)
