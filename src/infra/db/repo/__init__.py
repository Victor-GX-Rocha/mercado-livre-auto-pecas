"""
CRUD repositories for tables

Provides:
    ProdutosRepository: Repository for produtos table.
    ProdutosStatusRepository: Repository for produtos_status table.
    CloudinaryRepository: Repository for cloudinary table.
"""

from .produtos import ProdutosRepository
from .produtos_status import ProdutosStatusRepository
from .produtos_category import ProdutosCategroyRepository
from .cloud import CloudinaryRepository

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "ProdutosRepository",
    "ProdutosStatusRepository",
    "ProdutosCategroyRepository",
    
    "CloudinaryRepository"
]
