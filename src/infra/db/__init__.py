""" Database conection and SQLAlchemy managers """

from .database import init_database, InternalSession
# from .repositories.base

# Automaticly intit the database when you call the packege you know what I mean?


__version__ = "v.0.0.0"
__all__ = [
    "__version__",
    
    "init_database",
    "Session"

]