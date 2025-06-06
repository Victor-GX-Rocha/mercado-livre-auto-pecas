""" Meli auth requests envioromet """

from .manager import AuthManager
from .adpter import MeliAuthAdapter

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "AuthManager",
    "MeliAuthAdapter"
]
