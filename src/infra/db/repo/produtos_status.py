"""  """

from src.infra.db.models import ProdutosStatusORM, ProdutosStausConverter
from src.infra.db.repo.session.session_manager import session_scope
from .models import ResponseCode
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

class ProdutosGetMethods(BaseGetMethods):
    def __init__(self, entity: ProdutosStatusORM):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
        self.converter = ProdutosStausConverter()

class ProdutosUpdateMethods(BaseUpdateMethods):
    def log_success(self, id: int, status: str) -> None:
        """
        Register the result.
        Args:
            id (int): Line id.
            status (str): Product status on mercado libre.
        """
        with session_scope as session:
            line: ProdutosStatusORM = session.query(self.entity).get(id)
            line.status_produto = status
            line.cod_retorno = ResponseCode.SUCCESS

class ProdutosInsertMethods(BaseDeleteMethods):...
class ProdutosDeleteMethods(BaseInsertMethods):...

class ProdutosStatusRepository:
    """ SQL commands for table produtos_status. """
    def __init__(self):
        self.get = ProdutosGetMethods(ProdutosStatusORM)
        self.update = ProdutosUpdateMethods(ProdutosStatusORM)
        self.insert = ProdutosInsertMethods(ProdutosStatusORM)
        self.delete = ProdutosDeleteMethods(ProdutosStatusORM)
