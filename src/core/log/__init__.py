""" Registration systems manager """

from .log import log as logging
from .dev import dev_log

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "logging",
    "dev_log"
]
