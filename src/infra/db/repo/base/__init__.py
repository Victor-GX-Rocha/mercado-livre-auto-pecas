"""
Base shared CRUD commands for tables

Provides:
    
"""

from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "BaseGetMethods",
    "BaseUpdateMethods",
    "BaseDeleteMethods",
    "BaseInsertMethods",
]
