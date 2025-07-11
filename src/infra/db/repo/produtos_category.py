""" Repository for table operacao_categoria_ml """

from src.infra.db.models.produtos_category import ProdutosCategoryORM, ProdutosCategoryConverter
from src.infra.db.repo.session.session_manager import session_scope
from .models import ResponseCode
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

class ProdutosCategroyGetMethods(BaseGetMethods):
    def __init__(self, entity: ProdutosCategoryORM):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
        self.converter = ProdutosCategoryConverter()

class ProdutosCategroyUpdateMethods(BaseUpdateMethods):...
class ProdutosCategroyDeleteMethods(BaseDeleteMethods):...
class ProdutosCategroyInsertMethods(BaseInsertMethods):...


class ProdutosCategroyRepository:
    def __init__(self):
        self.get = ProdutosCategroyGetMethods(ProdutosCategoryORM)
        self.update = ProdutosCategroyUpdateMethods(ProdutosCategoryORM)
        self.insert = ProdutosCategroyDeleteMethods(ProdutosCategoryORM)
        self.delete = ProdutosCategroyInsertMethods(ProdutosCategoryORM)
