""" Base common update functionalities. """

# database/repositories/base/updatters.py

from ..session import session_scope
from .base import TableEntity, TableDataclass

class Loggers:
    """ Basic common logers for any table who conatains the cod_erro, log_erro columns"""
    def log_error(self, id: int, cod_erro: int, log_erro: str) -> None:
        """
        Args:
            id (int):
            cod_erro (int):
            log_erro (str):
        """
        with session_scope() as session:
            produto = session.query(self.entity).get(id)
            produto.log_erro = log_erro
            produto.cod_erro = cod_erro
