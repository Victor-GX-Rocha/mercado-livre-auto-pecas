""" CRUD operations for Produtos table. """

# database/repositories/produtos.py

# from session import session_scope
# from session.session_manager import session_scope
from src.infra.db.repo.session.session_manager import session_scope
from ..models.produtos import Produtos, ProdutosConverter
from .models import ResponseCode
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)


class ProdutosGetMethods(BaseGetMethods):
    """ Read (GET) methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity
        self.converter = ProdutosConverter()


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
    ) -> None:
        """
        Log a success publication message.
        Args:
            ml_id_produto: 
            categoria: 
            link_publicacao: 
            produto_status: 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.ml_id_produto = ml_id_produto
            line.categoria = categoria
            line.link_publicacao = link_publicacao
            line.produto_status = produto_status
            line.cod_retorno = ResponseCode.SUCCESS
    
    def change_status_success(
        self,
        id: int,
        produto_status: str,
    ) -> None:
        """
        Log a success activation message.
        Args:
            produto_status:
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.produto_status = produto_status
            line.cod_retorno = ResponseCode.SUCCESS
    
    def pause_success(
        self,
        id: int,
        produto_status: str,
    ) -> None:
        """
        Log a success pause message.
        Args:
            produto_status: 
        """
        self.change_status_success(
            id=id,
            produto_status=produto_status,
        )
    
    def activation_success(
        self,
        id: int,
        produto_status: str,
    ) -> None:
        """
        Log a success activation message.
        Args:
            produto_status:
        """
        self.change_status_success(
            id=id, 
            produto_status=produto_status,
        )
    
    def deletation_success(
        self,
        id: int,
        produto_status: str,
    ) -> None:
        """
        Log a success delete message.
        Args:
            produto_status:
        """
        self.change_status_success(
            id=id, 
            produto_status=produto_status,
        )

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
