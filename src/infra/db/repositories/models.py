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
