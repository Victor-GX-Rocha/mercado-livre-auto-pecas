""" Repositorie model for typing. """

from typing import Protocol, TypeVar

DataclassTable = TypeVar("DataclassTable")

class OrmTable:...

class OrmEntityProtocol(Protocol):
    def __init__(self, entity: OrmTable):
        """
        Args:
            entity (OrmTable): Any ORM table entity.
        """
        self.entity = entity

class StatusOperationGettersProtocol(Protocol):
    """ Finders based on status_operacao_id column value.  Pressets search methods for user interface. """
    
    def by_status_operacao(self, operacao: int) -> list[DataclassTable]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (List[DataclassTable]): List of DataclassTable. (Empty list if it not exists).
        """
    
    def pending_operations(self) -> list[DataclassTable]:
        """ Get pending operations """
    
    def completed_operations(self) -> list[DataclassTable]:
        """ Get completed operations """
    
    def in_process_operations(self) -> list[DataclassTable]:
        """ Get in-process operations """

class LoggersProtocol:
    """ Basic common logers for any table who conatains the cod_erro, log_erro columns"""
    def log_error(self, id: int, cod_erro: int, log_erro: str) -> None:...

class TableGetMethodsProtocol(OrmEntityProtocol, StatusOperationGettersProtocol):...
class TableUpdateMethodsProtocol(OrmEntityProtocol, LoggersProtocol):...
class TableInsertMethodsProtocol(OrmEntityProtocol):...
class TableDeleteMethodsProtocol(OrmEntityProtocol):...

class TableRepositoryProtocol(Protocol):
    def __init__(self):
        self.get = TableGetMethodsProtocol(OrmTable)
        self.update = TableUpdateMethodsProtocol(OrmTable)
        self.insert = TableInsertMethodsProtocol(OrmTable)
        self.delete = TableDeleteMethodsProtocol(OrmTable)
