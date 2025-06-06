""" CRUD operations for Produtos table """

# database/repositories/produtos.py

from typing import List
from dataclasses import dataclass

from ..models.produtos import Produtos, Product, ProdutosConverter
from .base import session_scope


@dataclass
class StatusOperationTypes:
    PENDING: int = 1
    COMPLETED: int = 2
    IN_PROCESS: int = 0


converter = ProdutosConverter()
oper_status = StatusOperationTypes()


class StatusOperationGetters:
    """ Finders based on status_operacao_id column value.  Pressets search methods for user interface. """
    
    def by_status_operacao(self, operacao: int) -> List[Produtos]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (List[Produtos]): List of Produtos table entity. (Empty if it not exists).
        """
        with session_scope() as session:
            produtos = session.query(self.entity).filter(self.entity.status_operacao_id == operacao).all()
            return converter.convert(produtos)
    
    def pending_operations(self) -> List[Produtos]:
        """ Get pending operations """
        return self.by_status_operacao(oper_status.PENDING)
    
    def completed_operations(self) -> List[Produtos]:
        """ Get completed operations """
        return self.by_status_operacao(oper_status.COMPLETED)
    
    def in_process_operations(self) -> List[Produtos]:
        """ Get in-process operations """
        return self.by_status_operacao(oper_status.IN_PROCESS)

class ProdutosGetMethods(StatusOperationGetters):
    """ Read (GET) methods for Produtos table entity. """
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity



# Serão implementados no futuro, no momento é apenas um esboço
class ProdutosUpdateMethods:
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosInsertMethods:
    def __init__(self, entity: Produtos):
        """
        Args:
            entity (Produtos): Produtos table entity.
        """
        self.entity = entity


class ProdutosDeleteMethods:
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

""" # Proposta de uso:
produtos_repo = ProdutosRepository()
produtos_repo.get.pending_operations() # Pegar operações pendentes
produtos_repo.get.by_id(12) # Caso seja necessário pegar uma linha em específico
operacao_em_tempo_real = 4
produtos_repo.get.by_status_operacao(operacao_em_tempo_real) # Caso seja necessário pegar uma operação dinamicamente
"""
