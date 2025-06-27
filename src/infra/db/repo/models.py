""" Models and constants for Repositories """

# database/repositories/models.py

from typing import TypeVar

TableEntity = TypeVar("TableEntity")
DataclassTable = TypeVar("DataclassTable")

class ResponseCode:
    """ Code response status. """
    PENDING: int = 0
    EXECUTING: int = 1
    SUCCESS: int = 2
    
    NOT_FOUND: int = 3
    TABLE_ERROR: int = 88
    PROGRAM_ERROR: int = 91

