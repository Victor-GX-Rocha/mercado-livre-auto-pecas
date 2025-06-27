""" Session manager for ORM queryes. """

from typing import Iterator
from sqlalchemy.orm import Session
from contextlib import contextmanager

from src.infra.db import InternalSession

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
