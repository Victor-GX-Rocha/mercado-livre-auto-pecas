""" CRUD operations for Produtos table. """

# database/repositories/produtos.py

# from session import session_scope
# from session.session_manager import session_scope
from src.infra.db.repositories.session.session_manager import session_scope
from ..models.produtos import Produtos, Product, ProdutosConverter
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

converter = ProdutosConverter()

class OperationStatus:
    PUBLICATION_SUCCESS: int = 2


class ProdutosGetMethods(BaseGetMethods):
    """ Read (GET) methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
        self.converter = converter


class ProdutosUpdateMethods(BaseUpdateMethods):
    """ Update methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
    
    def publication_success(
        self,
        id: int,
        ml_id_produto: str,
        categoria: str,
        link_publicacao: str,
        produto_status: str,                
        status_operacao_id: int = OperationStatus.PUBLICATION_SUCCESS
    ) -> None:
        """
        Log a success publication message.
        Args:
            ml_id_produto: 
            categoria: 
            link_publicacao: 
            produto_status: 
            status_operacao_id: 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.ml_id_produto = ml_id_produto
            line.categoria = categoria
            line.link_publicacao = link_publicacao
            line.produto_status = produto_status
            line.status_operacao_id = status_operacao_id

    def pause_success(
        self,
        id: int,
        produto_status: str,                
        status_operacao_id: int = OperationStatus.PUBLICATION_SUCCESS
    ) -> None:
        """
        Log a success pause message.
        Args:
            produto_status: 
            status_operacao_id: 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.produto_status = produto_status
            line.status_operacao_id = status_operacao_id

class ProdutosInsertMethods(BaseDeleteMethods):
    """ Delete methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosDeleteMethods(BaseInsertMethods):
    """ Create (Insert) methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosRepository:
    """ SQL commands for table Produtos. """
    def __init__(self):
        self.get = ProdutosGetMethods(Produtos)
        self.update = ProdutosUpdateMethods(Produtos)
        self.insert = ProdutosInsertMethods(Produtos)
        self.delete = ProdutosDeleteMethods(Produtos)
