""" Execution flow of Produtos table operations. """

from src.core import log
from src.infra.api.mercadolivre.auth import AuthResponse, MeliAuthCredentials
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.db.models.produtos import Product
from src.infra.db.repositories import ProdutosRepository
from src.app.shared.oganizer import GroupBy
from src.app.shared.token_manager import MeliTokenManager
from .generators.payload import PayloadGenerator
from .operations import (
    ProdutosOperationProtocol, 
    Publication, Edition, Pause, Activation, Deletion,
    JustSleep, InvalidOperation
)


class OperationFactory:
    def __init__(
        self, 
        repo: ProdutosRepository, 
        payload_generator: PayloadGenerator = None,
        items_requests: ItemsRequests = None
    ) -> ProdutosOperationProtocol:
        self.repo = repo
        self.payload_generator = payload_generator
        self.items_requests = items_requests
    
    def create(self, operation_id: int) -> ProdutosOperationProtocol:
        match operation_id:
            case 1:
                return Publication(log, self.repo, self.payload_generator, self.items_requests)
            case 2:
                return Edition(log, self.repo, self.items_requests, self.payload_generator)
            case 3:
                return Pause(log, self.repo, self.items_requests)
            case 4:
                return Activation(log, self.repo, self.items_requests)
            case 5:
                return Deletion(log, self.repo, self.items_requests)
            case _:
                return InvalidOperation(self.repo)
                # raise ValueError(f"Operação inválida: {operation_id}")


class ProdutosApplication:
    def __init__(self):
        self.repo = ProdutosRepository()
        self.payload_generator = PayloadGenerator()
        self.items_requests = ItemsRequests()
        self.meli_auth = MeliAuthCredentials()
        self.token_manager = MeliTokenManager(
            repo=self.repo, 
            meli_auth=self.meli_auth
        )
        self.operation_factory = OperationFactory(
            repo=self.repo,
            payload_generator=self.payload_generator, 
            items_requests=self.items_requests
        )
    
    def execute(self) -> None:
        pending_lines = self.repo.get.pending_operations()
        
        if not pending_lines:
            # print("Nenhuma linha pendente no momento")
            return
        
        user_lines = GroupBy.column(pending_lines, "credentials.client_id")
        
        for user, lines in user_lines.items():
            if token := self.token_manager.get_token(lines):
                self._execute_operations(lines, token.data)
            else:
                print(f"Falha ao obter token para usuário {user}")
    
    def _execute_operations(self, user_lines: list[Product], token: AuthResponse):
        oper_lines = GroupBy.column(user_lines, "controlers.operacao")
        print(f"{oper_lines.keys() = }")
        
        for oper_id, items in oper_lines.items():
            try:
                operation = self.operation_factory.create(oper_id)
                operation.execute(items, token)
            except ValueError as e:
                log.user.exception(f"Erro: {e}")
            except AttributeError as e:
                log.user.exception(f"Erro de dependência: {e}")
            except Exception as e:
                log.dev.exception(f"Exceção inesperada: {e}")
