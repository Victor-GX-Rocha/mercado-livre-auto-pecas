""" Application services.

Provides:
    ProdutosApplication: Operations for table `produtos`.
    StatusApplication: Operations for table `produtos_status`.
    ProdutosCategoryApplication: Operations for table `operacao_categoria_ml.`
"""

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
