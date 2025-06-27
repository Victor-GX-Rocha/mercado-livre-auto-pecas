"""
CRUD repositories for tables

Provides:
    ProdutosRepository: Produtos repository table
"""

from .produtos import ProdutosRepository
from .cloud import CloudinaryRepository

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosRepository",
    "CloudinaryRepository"
]
