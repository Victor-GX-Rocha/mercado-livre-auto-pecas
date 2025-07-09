""" Status operations. """

from src.core import log
from src.app.shared.oganizer import GroupBy
from src.app.models import ApplicationProtocol
from src.infra.db.repo import ProdutosStatusRepository
from src.infra.db.models import ProdutosStatusDataclass
from src.app.shared.token_manager import MeliTokenManager
from src.infra.api.mercadolivre.auth import AuthResponse, MeliAuthCredentials

class StatusApplication(ApplicationProtocol):
    def __init__(self) -> None:
        self.repo = ProdutosStatusRepository()
        self.meli_auth = MeliAuthCredentials()
        self.token_manager = MeliTokenManager(
            repo=self.repo, 
            meli_auth=self.meli_auth
        )
        
    def execute(self) -> None:
        pending_lines: list[ProdutosStatusDataclass] = self.repo.get.pending_operations()
        
        if not pending_lines:
            print("Nenhuma linha pendente no momento")
            return
        
        user_lines: dict[str, list[ProdutosStatusDataclass]] = GroupBy.column(pending_lines, "credentials.client_id")
        
        for user, lines in user_lines.items():
            if token := self.token_manager.get_token(lines):
                self._execute_operations(lines, token.data)
            else:
                print(f"Falha ao obter token para usuário {user}")
    
    def _execute_operations(self, user_lines: list[ProdutosStatusDataclass], token: AuthResponse):
        oper_lines = GroupBy.column(user_lines, "controlers.operacao")
        print(f"{oper_lines.keys() = }")
        
        for oper_id, items in oper_lines.items():
            try:
                print(f"Realizar operação para upar status")
                # operation = self.operation_factory.create(oper_id)
                # operation.execute(items, token)
            except ValueError as e:
                log.user.exception(f"Erro: {e}")
            except AttributeError as e:
                log.user.exception(f"Erro de dependência: {e}")
            except Exception as e:
                log.dev.exception(f"Exceção inesperada: {e}")
