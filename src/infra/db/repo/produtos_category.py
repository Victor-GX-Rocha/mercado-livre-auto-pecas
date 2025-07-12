""" Repository for table operacao_categoria_ml """

from sqlalchemy import insert

from src.infra.db.models.produtos_category import ProdutosCategoryORM, ProdutosCategoryConverter
from src.infra.db.repo.session.session_manager import session_scope
from .models import ResponseCode
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseInsertMethods,
    BaseDeleteMethods
)

class ProdutosCategroyGetMethods(BaseGetMethods):
    def __init__(self, entity: ProdutosCategoryORM):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
        self.converter = ProdutosCategoryConverter()

class ProdutosCategroyUpdateMethods(BaseUpdateMethods):
    def register_single_result(self, id: int, category_id: str) -> None:
        """
        
        Args:
            id (int): Line id.
            category_id (str): The meli category ID.
        """
        with session_scope() as session:
            line: ProdutosCategoryORM = session.query(self.entity).get(id)
            line.categoria_id = category_id
            line.cod_retorno = ResponseCode.SUCCESS

class ProdutosCategroyInsertMethods(BaseInsertMethods):
    def add_new_result(self, cod_produto: str, category_id: str) -> None:
        """
        
        Args:
            id (int): Line id.
            category_id (str): The meli category ID.
        """
        with session_scope() as session:
            # Agora só precisa fornecer os campos essenciais
            new_record = self.entity(
                cod_produto=cod_produto,
                categoria_id=category_id,
                cod_retorno=ResponseCode.SUCCESS
            )
            session.add(new_record)


class ProdutosCategroyDeleteMethods(BaseDeleteMethods):...




class ProdutosCategroyRepository:
    def __init__(self):
        self.get = ProdutosCategroyGetMethods(ProdutosCategoryORM)
        self.update = ProdutosCategroyUpdateMethods(ProdutosCategoryORM)
        self.delete = ProdutosCategroyDeleteMethods(ProdutosCategoryORM)
        self.insert = ProdutosCategroyInsertMethods(ProdutosCategoryORM)
