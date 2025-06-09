"""
Base classes and utilities for SQLAlchemy repository pattern.

Provides:
- BaseGetMethods: Common read operations for repositories
- BaseUpdateMethods: Common update methods for repositories 
- BaseInsertMethods: Common insert methods for repositories 
- BaseDeleteMethods: Common delete methods for repositories 
"""

# database/repositories/base.py


from typing import Type, TypeVar

from ..session import session_scope
from .getters import StatusOperationGetters
from .updatters import Loggers


TableEntity = TypeVar("TableEntity")


# class BaseGetMethods(Generic[TableEntity]):
class BaseGetMethods(StatusOperationGetters):
    """ Base class for common read operations (GET) in repositories. """
    def __init__(self, entity: Type[TableEntity], converter) -> None:
        """
        Args:
            entity (Type[TableEntity]): Table entity.
            converter (): Dataclass table entity converter.
        """
        self.entity = entity
        self.converter = converter



class BaseUpdateMethods(Loggers):
    def __init__(self, entity: Type[TableEntity]) -> None:
        """
        Args:
            entity: Table entity.
        """
        self.entity = entity


class BaseDeleteMethods:
    def __init__(self, entity: Type[TableEntity]) -> None:
        """
        Args:
            entity: Table entity.
        """
        self.entity = entity

class BaseInsertMethods:
    def __init__(self, entity: Type[TableEntity]) -> None:
        """
        Args:
            entity: Table entity.
        """
        self.entity = entity
    
    # # INSERT (exemplo)
    # def insert(self, **kwargs):
    #     with session_scope() as session:
    #         instance = self.entity(**kwargs)
    #         session.add(instance)
    #         return instance
