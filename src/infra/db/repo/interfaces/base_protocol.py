""" Repositorie model for typing. """

from typing import Protocol, TypeVar
from src.infra.db.repo.models import ResponseCode

DataclassTable = TypeVar("DataclassTable")
DataclassTableLine = TypeVar("DataclassTableLine")

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
    def log_error(self, id: int, return_code: int, log_erro: str) -> None:...
    def log_success_code(self, id: int, return_code: int = ResponseCode.SUCCESS) -> None:
        """
        Log a simple message with the code sucess.
        Args:
            id (int): Line ID.
            return_code (int): Success code number. 
        """
    def got_to_sleep(self, id: int, return_code: int = ResponseCode.SUCCESS) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            return_code (int): Code number. 
        """
    def executing(self, id: int, return_code: int = ResponseCode.EXECUTING) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            return_code (int): Success code number. 
        """

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
