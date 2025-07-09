"""
Dataclasses models for tables

Provides:
- MeliCredentials: 
- Base: 
- Produtos: Produtos table SQLAlchemy dataclass entity
"""

from .bases import MeliCredentials, Base
from .produtos import Produtos, Product
from .produtos_status import ProdutosStatusORM, ProdutosStatusDataclass, ProdutosStausConverter
# from .produtos import *

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "MeliCredentials", "Base",
    
    "Produtos", "Product",
    "ProdutosStatusORM", "ProdutosStatusDataclass", "ProdutosStausConverter"
]
