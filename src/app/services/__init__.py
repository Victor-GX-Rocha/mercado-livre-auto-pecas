""" Application services. """

from src.app.services.produtos import ProdutosApplication
from src.app.services.produtos_status import StatusApplication

__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "ProdutosApplication",
    "StatusApplication"
]
