""" CRUD operations for Produtos table. """

# database/repositories/produtos.py

# from session import session_scope
# from session.session_manager import session_scope
from src.infrastructure.database.repositories.session.session_manager import session_scope
from ..models.produtos import Produtos, Product, ProdutosConverter
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

converter = ProdutosConverter()

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
