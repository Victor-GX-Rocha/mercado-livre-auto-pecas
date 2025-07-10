""" Status checker for products. """

from src.infra.api.mercadolivre.models import MeliResponse, MeliRequestFail
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.models import ProdutosStatusDataclass
from src.infra.db.repo import ProdutosStatusRepository
from src.infra.db.repo.models import ResponseCode
from src.core import log
from src.app.shared.validators import (
    ValidatorsProtocol, 
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator, 
    OperationValidator
)


class StatusChecker:
    """  """
    def __init__(
            self, 
            log: log, 
            repo: ProdutosStatusRepository, 
            items_requests: ItemsRequests
        ) -> None:
        """
        Args:
            repo (ProdutosStatusRepository): Repository for produto_status table.
            items_requests (ItemsRequests): Requests for mercado libre items.
        """
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
        self.validator = OperationValidator(self.log, self.repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "mercado_livre_id"
            ])
        ]
    
    def execute(self, lines: list[ProdutosStatusDataclass], token: AuthResponse) -> None:
        """
        Check the status of a product.
        Args:
            line (ProdutosStatusDataclass): Produtos_status table line as dataclass.
            token (AuthResponse): Meli token.
        """
        for line in lines:
            try:
                
                if not self.validator.validate(line, self.validators):
                    return
                
                product_name: str = f"Produto [DB-ID: {line.id} | MELI-ID: {line.mercado_livre_id}]"
                
                self.repo.update.executing(line.id)
                
                status: str = self._get_status(
                    line=line, 
                    token=token, 
                    product_name=product_name
                )
                
                self.repo.update.log_success(
                    id=line.id, 
                    status=status
                )
                
            except MeliRequestFail as e:
                log.dev.exception(f"{self.__class__.__name__}: {e}")
                self.repo.update.log_error(
                    id=line.id, 
                    return_code=ResponseCode.PROGRAM_ERROR, 
                    log_erro=e
                )
            except Exception as e:
                log.dev.exception(f"{self.__class__.__name__}: {e}")
                self.repo.update.log_error(
                    id=line.id, 
                    return_code=ResponseCode.PROGRAM_ERROR, 
                    log_erro=f"Falha inesperada: {e}"
                )
    
    def _get_status(self, line: ProdutosStatusDataclass, token: AuthResponse, product_name: str) -> str:
        """
        Gets the product status
        Args:
            line (ProdutosStatusDataclass): Produtos_status table line as dataclass.
            token (AuthResponse): Meli token.
            product_name (str): Identifier for current product.
        Returns:
            str: Product status.
        Raises:
            MeliRequestFail: Meli request fail.
        """
        status_response: MeliResponse = self.items_requests.get_item_info(
            access_token=token.access_token, 
            item_id=line.mercado_livre_id
        )
        
        if not status_response.success:
            raise MeliRequestFail(status_response.error)
        
        elif not status_response.data.get("status"):
            raise MeliRequestFail(f"{product_name} dado de status ausente ({status_response.data.get("status")}). Detalhes: {status_response.error}")
        
        return status_response.data.get("status")
