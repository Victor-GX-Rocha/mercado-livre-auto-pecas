""" Models for Produtos table """

from .data_class import Product
from .orm_entity import Produtos
from .orm_converter import ProdutosConverter

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "Product",
    "Produtos",
    "ProdutosConverter"
]
