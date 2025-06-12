""" Base common update functionalities. """

# database/repositories/base/updatters.py

from ..session import session_scope

class Loggers:
    """ Basic common logers for any table who contains the cod_erro, log_erro columns"""
    def log_error(self, id: int, cod_erro: int, log_erro: str) -> None:
        """
        Log an error inside an especifiedy line.
        Args:
            id (int): Line ID.
            cod_erro (int): Error code.
            log_erro (str): Log message.
        """
        with session_scope() as session:
            produto = session.query(self.entity).get(id)
            produto.log_erro = str(log_erro)
            produto.cod_erro = cod_erro
