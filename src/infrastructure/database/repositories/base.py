"""
Base classes and utilities for SQLAlchemy repository pattern.

Provides:
- session_scope: Conext manager for database sessions
- BaseGetMethods: Common read operations for repositories
- BaseUpdateMethods: Common update methods for repositories 
- BaseInsertMethods: Common insert methods for repositories 
- BaseDeleteMethods: Common delete methods for repositories 
"""

# database/repositories/base.py

from typing import Optional, Generic, Iterator, Type, TypeVar
from sqlalchemy.orm import Session
from contextlib import contextmanager

from ..database import InternalSession


TableEntity = TypeVar("TableEntity")


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Provides a transactional scope around a series of database operations.
    
    Returns:
        (Iterator[Session]): An interator of SQLAlchemy Sessions.
    Raises:
        (Exception): Rolls back transaction on any exception and re-raises the error.
    """
    session = InternalSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class BaseGetMethods(Generic[TableEntity]):
    """ Base class for common read operations (GET) in repositories. """
    def __init__(self, entity: Type[TableEntity]) -> None:
        """
        Args:
            entity: Table entity.
        """
        self.entity = entity
    
    def all(self) -> list[TableEntity]:
        """
        Get all records from the table.
        
        Returns:
            (list[TableEntity]): list of entities (empty if no records exist)
        """
        with session_scope() as session:
            return session.query(self.entity).all()
    
    def by_id(self, id: int) -> Optional[TableEntity]:
        """
        Get line record by ID.
        
        Args:
            id (int): ID of the line that shuld be seleceted
        Returns:
            (Optional[TableEntity]): A table line entity or None if the line not exists
        """
        with session_scope() as session:
            return session.query(self.entity).get(id)


class BaseUpdateMethods:
    def __init__(self, entity: Type[TableEntity]) -> None:
        """
        Args:
            entity: Table entity.
        """
        self.entity = entity
    
    def log_error(self, id: int, cod_erro: int, log_erro: str) -> None:
        """
        Args:
            id (int):
            cod_erro (int):
            log_erro (str):
        """
        with session_scope() as session:
            produto = session.query(self.entity).get(id)
            produto.log_erro = log_erro
            produto.cod_erro = cod_erro

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
