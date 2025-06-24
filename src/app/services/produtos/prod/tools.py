""" . """

from src.core import log
from src.infra.db.repositories import ProdutosRepository
from src.infra.db.models.produtos import Product
from src.infra.db.repositories.models import ResponseCode
from src.app.shared.validators import Validator, ValidatorsProtocol, ValidationResponse

class ProdutosValidator:
    def __init__(self, log: log, repo: ProdutosRepository):
        self.log = log
        self.repo = repo
    
    def validate(self, line: Product, validators: list[ValidatorsProtocol]) -> bool:
        """
        Vaidate if the product is able to be used.
        Args:
            line (Product): 
        Returns:
            bool: True if valid, else False.
        """
        response: ValidationResponse = Validator.validate(line, validators)
        if not response.is_valid:
            self.log.user.warning(f"{response.causes}")
            self.repo.update.log_error(line.id, cod_erro=ResponseCode.TABLE_ERROR, log_erro=response.causes)
            return False
        return True
