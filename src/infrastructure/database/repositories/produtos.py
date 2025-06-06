"""
Repositorie for Produtos CRUD operations

"""

# database/repositories/produtos.py

from typing import List

from ..models.produtos import Produtos
from .base import (
    session_scope,
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

class ProdutosGetPresetMethods:
    """ Presset serach methods for user interface """
    def pending_operations(self) -> List[Produtos]:
        """ Get pending operations """
        return self.by_status_operacao(1)
    
    def completed_operations(self) -> List[Produtos]:
        """ Get completed operations """
        return self.by_status_operacao(2)
    
    def in_process_operations(self) -> List[Produtos]:
        """ Get in-process operations """
        return self.by_status_operacao(0)

class ProdutosGetMethods(BaseGetMethods, ProdutosGetPresetMethods):
    """ Read (GET) methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        super().__init__(entity)
    
    def by_status_operacao(self, operacao: int) -> List[Produtos]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (List[Produtos]): List of Produtos table entity. (Empty if it not exists).
        """
        with session_scope() as session:
            return session.query(self.entity).filter(self.entity.status_operacao_id == operacao).all()

    def test(self):
        with session_scope() as session:
            return session.query(Produtos).all()

# Serão implementados no futuro, no momento é apenas um esboço
class ProdutosUpdateMethods(BaseUpdateMethods):
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        super().__init__(entity)

class ProdutosInsertMethods(BaseInsertMethods):
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        super().__init__(entity)

class ProdutosDeleteMethods(BaseDeleteMethods):
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        super().__init__(entity)


class ProdutosRepository:
    def __init__(self):
        self.get = ProdutosGetMethods(Produtos)
        self.update = ProdutosUpdateMethods(Produtos)
        self.insert = ProdutosInsertMethods(Produtos)
        self.delete = ProdutosDeleteMethods(Produtos)

""" # Proposta de uso:
produtos_repo = ProdutosRepository()
produtos_repo.get.pending_operations() # Pegar operações pendentes
produtos_repo.get.by_id(12) # Caso seja necessário pegar uma linha em específico
operacao_em_tempo_real = 4
produtos_repo.get.by_status_operacao(operacao_em_tempo_real) # Caso seja necessário pegar uma operação dinamicamente
"""
