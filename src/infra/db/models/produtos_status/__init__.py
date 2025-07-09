""" Models for Produtos table """

from .data_class import ProdutosStatusDataclass
from .orm_entity import ProdutosStatusORM
from .orm_converter import ProdutosStausConverter

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosStatusDataclass",
    "ProdutosStatusORM",
    "ProdutosStausConverter"
]
