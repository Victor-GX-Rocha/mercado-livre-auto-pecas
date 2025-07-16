"""
Application services.

Centralizes all services inside a same app interface.
Provides:
    App.ProdutosApplication: Operations for table `produtos`.
    App.StatusApplication: Operations for table `produtos_status`.
    App.ProdutosCategoryApplication: Operations for table `operacao_categoria_ml.`
"""

from .services.produtos import ProdutosApplication
from .services.produtos_status import StatusApplication
from .services.produtos_category import ProdutosCategoryApplication 

class App:
    produtos = ProdutosApplication()
    status = StatusApplication()
    category = ProdutosCategoryApplication ()
    
    def __init__(self):
        raise TypeError("Esta classe não deve ser instanciada. Use os atributos diretamente: App.produtos")

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "App"
]
