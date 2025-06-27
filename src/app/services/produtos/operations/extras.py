

from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.models.produtos import Product
from src.infra.db.repo import ProdutosRepository
from src.infra.db.repo.models import ResponseCode

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
            self.repo.update.log_error(
                id=line.id, 
                return_code=ResponseCode.TABLE_ERROR, 
                log_erro=f"Operação inválida: {line.controlers.operacao}"
            )
