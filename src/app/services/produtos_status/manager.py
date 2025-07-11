""" Status operations. """

from src.core import log
from src.app.shared.oganizer import GroupBy
from src.app.models import ApplicationProtocol
from src.app.shared.operations import InvalidOperation, TableOperationProtocol, TableOperationFactoryProtocol
from src.app.shared.token_manager import MeliTokenManager
from src.infra.db.repo import ProdutosStatusRepository
from src.infra.db.models import ProdutosStatusDataclass
from src.infra.api.mercadolivre.auth import AuthResponse, MeliAuthCredentials
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.db.repo import ProdutosStatusRepository
from .check_status import StatusChecker


class StatusOperationFactory(TableOperationFactoryProtocol):
    def __init__(
        self,
        log: log,
        repo: ProdutosStatusRepository, 
        items_requests: ItemsRequests = None
    ) -> None:
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
    
    def create(self, operation_id: int) -> TableOperationProtocol:
        match operation_id:
            case 1:
                return StatusChecker(self.log, self.repo, self.items_requests)
            case _:
                return InvalidOperation(self.log, self.repo)


class StatusApplication(ApplicationProtocol):
    def __init__(self) -> None:
        self.log = log
        self.repo = ProdutosStatusRepository()
        self.meli_auth = MeliAuthCredentials()
        self.items_requests = ItemsRequests()
        self.token_manager = MeliTokenManager(
            repo=self.repo, 
            meli_auth=self.meli_auth
        )
        self.operation_factory = StatusOperationFactory(
            log=self.log,
            repo=self.repo,
            items_requests=self.items_requests
        )
    
    def execute(self) -> None:
        pending_lines: list[ProdutosStatusDataclass] = self.repo.get.pending_operations()
        
        if not pending_lines:
            # print("Nenhuma linha pendente no momento")
            return
        
        user_lines: dict[str, list[ProdutosStatusDataclass]] = GroupBy.column(pending_lines, "credentials.client_id")
        
        for user, lines in user_lines.items():
            if token := self.token_manager.get_token(lines):
                self._execute_operations(lines, token.data)
            else:
                print(f"Falha ao obter token para usuário {user}")
    
    def _execute_operations(self, user_lines: list[ProdutosStatusDataclass], token: AuthResponse) -> None:
        oper_lines = GroupBy.column(user_lines, "controllers.operacao")
        # print(f"{oper_lines.keys() = }")
        
        for oper_id, items in oper_lines.items():
            try:
                print(f"Realizando operação para upar status")
                operation = self.operation_factory.create(oper_id)
                operation.execute(items, token)
            except ValueError as e:
                self.log.user.exception(f"Erro: {e}")
            except AttributeError as e:
                self.log.user.exception(f"Erro de dependência: {e}")
            except Exception as e:
                self.log.dev.exception(f"Exceção inesperada: {e}")
