""" Models and constants for Repositories """

# database/repositories/models.py

from typing import TypeVar
from dataclasses import dataclass

TableEntity = TypeVar("TableEntity")
DataclassTable = TypeVar("DataclassTable")

@dataclass
class StatusOperationTypes:
    """ Types of state for column operation. """
    PENDING: int = 1
    COMPLETED: int = 2
    IN_PROCESS: int = 0

class OperationStatus:
    """ Operation execution status. """
    WAITING: int = 1
    SUCCESS: int = 2
    FINILIZED: int = 3

class ResponseCode:
    """ Code response status. """
    OK: int = 0
    NOT_FOUND: int = 88
    TABLE_ERROR: int = 90
    PROGRAM_ERROR: int = 91
