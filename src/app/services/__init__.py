""" Application services. """

from .produtos import ProdutosApplication
from .produtos_status import StatusApplication
from .produtos_category import ProdutosCategoryApplication 

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosApplication",
    "StatusApplication",
    "ProdutosCategoryApplication"
]
