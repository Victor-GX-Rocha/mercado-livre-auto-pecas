"""
Functionalities for table operacao_categoria_ml.

Provides:
    ProdutosCategoryORM: ORM class entity.
    ProdutosCategoryDataclass: Dataclass object.
    ProdutosCategoryConverter: Class converter.
"""

from .orm_entity import ProdutosCategoryORM
from .data_class import ProdutosCategoryDataclass
from .orm_converter import ProdutosCategoryConverter

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosCategoryORM",
    "ProdutosCategoryDataclass",
    "ProdutosCategoryConverter"
]
