"""  """

from src.core import log
from src.infra.api.mercadolivre.auth import AuthResponse, MeliAuthCredentials
from src.infra.db.models.produtos_category import ProdutosCategoryDataclass
from src.infra.db.repo import ProdutosCategroyRepository
from src.app.shared.operations import TableOperationFactoryProtocol, InvalidOperation
from src.app.shared.token_manager import MeliTokenManager
from src.app.models import ApplicationProtocol
from src.app.shared.oganizer import GroupBy

class ProdutosCategoryFactory(TableOperationFactoryProtocol):
    def __init__(self, log: log, repo: ProdutosCategroyRepository):
        self.log = log
        self.repo = repo
    
    def create(self, operation_id: int):
        match operation_id:
            case 1:
                print("Caso: 1")
            case 2:
                print("Caso: 2")
            case 21:
                print("Caso: 2.1")
            case 3:
                print("Caso: 3")
            case _:
                return InvalidOperation()


class ProdutosCategoryApplication(ApplicationProtocol):
    def __init__(self) -> None:
        self.log = log
        self.repo = ProdutosCategroyRepository()
        self.meli_auth = MeliAuthCredentials()
        self.operation_factory = ProdutosCategoryFactory(
            log=self.log,
            repo=self.repo
        )
        self.token_manager = MeliTokenManager(
            repo=self.repo, 
            meli_auth=self.meli_auth
        )
    
    def execute(self) -> None:
        pending_lines: list[ProdutosCategoryDataclass] = self.repo.get.pending_operations()
        
        if not pending_lines:
            print("Nenhuma linha pendente no momento")
            return
        
        user_lines: dict[str, list[ProdutosCategoryDataclass]] = GroupBy.column(pending_lines, "credentials.client_id")
        
        for user, lines in user_lines.items():
            if token := self.token_manager.get_token(lines):
                self._execute_operations(lines, token.data)
            else:
                print(f"Falha ao obter token para usuário {user}")
    
    def _execute_operations(self, user_lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        oper_lines = GroupBy.column(user_lines, "controllers.operacao")
        # print(f"{oper_lines.keys() = }")
        
        for oper_id, items in oper_lines.items():
            try:
                print(f"Realizando operação para descoberta de atibutos de categoria")
                operation = self.operation_factory.create(oper_id)
                operation.execute(items, token)
            except ValueError as e:
                self.log.user.exception(f"Erro: {e}")
            except AttributeError as e:
                self.log.user.exception(f"Erro de dependência: {e}")
            except Exception as e:
                self.log.dev.exception(f"Exceção inesperada: {e}")
