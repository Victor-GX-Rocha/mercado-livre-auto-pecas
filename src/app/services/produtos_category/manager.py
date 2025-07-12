"""  """

from src.core import log
from src.infra.api.mercadolivre.auth import AuthResponse, MeliAuthCredentials
from src.infra.db.models.produtos_category import ProdutosCategoryDataclass
from src.infra.db.repo import ProdutosCategroyRepository
from src.infra.api.mercadolivre.items import ItemsRequests
from src.app.shared.operations import TableOperationFactoryProtocol, InvalidOperation
from src.app.shared.token_manager import MeliTokenManager
from src.app.models import ApplicationProtocol
from src.app.shared.oganizer import GroupBy
from .operations import CategoryIDByPath, CategoryIDByTitle, PathByCategoryID



class ProdutosCategoryFactory(TableOperationFactoryProtocol):
    def __init__(
        self, log: log, 
        repo: ProdutosCategroyRepository, 
        items_requests: ItemsRequests
    ) -> None:
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
    
    def create(self, operation_id: int):
        
        if operation_id == 1:
            return CategoryIDByPath(self.log, self.repo)
        
        elif operation_id == 2 or operation_id == 21:
            return CategoryIDByTitle(self.log, self.repo, self.items_requests)
        
        elif operation_id == 3:
            return PathByCategoryID()
        
        return InvalidOperation(self.log, self.repo)



class ProdutosCategoryApplication(ApplicationProtocol):
    def __init__(self) -> None:
        self.log = log
        self.repo = ProdutosCategroyRepository()
        self.meli_auth = MeliAuthCredentials()
        self.items_requests = ItemsRequests()
        self.operation_factory = ProdutosCategoryFactory(
            log=self.log,
            repo=self.repo,
            items_requests=self.items_requests
        )
        self.token_manager = MeliTokenManager(
            repo=self.repo, 
            meli_auth=self.meli_auth
        )
    
    def execute(self) -> None:
        pending_lines: list[ProdutosCategoryDataclass] = self.repo.get.pending_operations()
        
        if not pending_lines:
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
