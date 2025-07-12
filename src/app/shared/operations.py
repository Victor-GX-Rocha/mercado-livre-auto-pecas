"""
Shared operations.

Provides:
    TableOperationProtocol: 
    TableOperationFactoryProtocol: 
    InvalidOperation: 
    JustSleep: 
"""

from typing import Protocol, TypeVar, runtime_checkable

from src.infra.db.repo.interfaces import TableRepositoryProtocol, DataclassTableLine
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.db.repo.models import ResponseCode
from src.core import log


TableOperation = TypeVar("TableOperation")


@runtime_checkable
class TableOperationProtocol(Protocol):
    def execute(self, lines: list[DataclassTableLine], token: AuthResponse) -> None:
        """ Execute the class main funcionality. """

class TableOperationFactoryProtocol(Protocol):
    def create(self, operation_id: int) -> TableOperationProtocol:
        """ Construct and returns an object based on it's ID. """


class InvalidOperation:
    def __init__(self, log: log, repo: TableRepositoryProtocol):
        self.log = log
        self.repo = repo
    
    def execute(self, lines: list[DataclassTableLine], token: AuthResponse) -> None:
        """ Allerts the user that this operation does not exists. """
        
        for line in lines:
            self.log.user.warning(f"Operação inválida. Produto [DB-ID: {line.id}]")
            self.repo.update.log_error(
                id=line.id, 
                return_code=ResponseCode.TABLE_ERROR, 
                log_erro=f"Operação inválida: {line.controllers.operacao}"
            )

class JustSleep:
    def __init__(self, repo: TableRepositoryProtocol):
        self.repo = repo
    
    def execute(self, lines: list[DataclassTableLine], token: AuthResponse) -> None:
        """ Change the status operation to another number to make it "sleep" """
        
        for line in lines:
            self.repo.update.got_to_sleep(line.id)

