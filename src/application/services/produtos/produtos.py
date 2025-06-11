""" Execution flow of Produtos table operations. """

from ....infrastructure.api.mercadolivre.client import MLBaseClient
from ....infrastructure.api.mercadolivre.auth import AuthResponse, AuthManager, MeliAuthCredentials
from ....infrastructure.database.models.produtos import Produtos, Product
from ....infrastructure.database.repositories import ProdutosRepository
from ...shared.oganizer import GroupBy
from ...shared.token_manager import MeliTokenManager
from .json_generator import JsonGenerator
from .operations import (
    ProdutosOperation,
    Publication,
    Edition,
    Pause,
    Activation,
    Deletation,
)

# meli_client = MLBaseClient()
# auth_manager = AuthManager(meli_client)
auth_manager = AuthManager()

class OperationFactory:
    def __init__(self, repo, json_generator=None):
        self.repo = repo
        self.json_generator = json_generator
    
    def create(self, operation_id: int) -> ProdutosOperation:
        match operation_id:
            case 1:
                return Publication(self.repo, self.json_generator)
            case 3:
                return Edition(self.repo, self.json_generator)
            case 4:
                return Pause(self.repo)
            case 5:
                return Activation(self.repo)
            case 6:
                return Deletation(self.repo)
            case _:
                raise ValueError(f"Operação inválida: {operation_id}")


class ProdutosApplication:
    def __init__(self):
        self.repo = ProdutosRepository()
        self.meli_auth = MeliAuthCredentials(auth_manager)
        self.token_manager = MeliTokenManager(meli_auth=self.meli_auth, repo=self.repo)
        self.operation_factory = OperationFactory(
            repo=self.repo,
            json_generator=JsonGenerator()
        )
    
    def execute(self) -> None:
        pending_lines = self.repo.get.pending_operations()
        
        if not pending_lines:
            print("Nenhuma linha pendente no momento")
            return
        
        user_lines = GroupBy.column(pending_lines, "credentials.client_id")
        
        for user, lines in user_lines.items():
            if token := self.token_manager.get_token(lines):
                self._execute_operations(lines, token)
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
                print(f"Erro: {e}")
            except AttributeError as e:
                print(f"Erro de dependência: {e}")
            except Exception as e:
                print(f"Exceção inesperada: {e}")
