""" CRUD operations for Produtos table """

# database/repositories/produtos.py

from ..models.produtos import Produtos, Product, ProdutosConverter
from session import session_scope
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
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosInsertMethods(BaseDeleteMethods):
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosDeleteMethods(BaseInsertMethods):
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosRepository:
    def __init__(self):
        self.get = ProdutosGetMethods(Produtos)
        self.update = ProdutosUpdateMethods(Produtos)
        self.insert = ProdutosInsertMethods(Produtos)
        self.delete = ProdutosDeleteMethods(Produtos)
