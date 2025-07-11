"""
Functionalities for table produtos_status.

Provides:
    ProdutosStatusORM: ORM class entity.
    ProdutosStatusDataclass: Dataclass object.
    ProdutosStausConverter: Class converter.
"""

from .orm_entity import ProdutosStatusORM
from .data_class import ProdutosStatusDataclass
from .orm_converter import ProdutosStausConverter

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosStatusORM",
    "ProdutosStatusDataclass",
    "ProdutosStausConverter"
]
