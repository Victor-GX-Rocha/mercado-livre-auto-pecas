"""
Dataclasses models for tables

Provides:
- MeliCredentials: 
- Base: 
- Produtos: Produtos table SQLAlchemy dataclass entity
"""

from .base import MeliCredentials, Base
from .produtos import Produtos
# from .produtos import *

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "MeliCredentials",
    "Base",
    
    "Produtos"
    
    # "Controlers",
    # "ErrorLoggers",
    # "Identifiers",
    # "SaleData",
    # "ShippimentData",
    # "CategoryData",
    # "TecnicalData",
    # "DimensionsData",
    # "Product"
]
