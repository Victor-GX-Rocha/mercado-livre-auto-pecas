""" Base common update functionalities. """

from src.infra.db.repo.session import session_scope
from src.infra.db.repo.models import ResponseCode


class Loggers:
    """ Basic common logers for any table who contains the cod_retorno, log_erro columns"""
    def log_error(self, id: int, return_code: int, log_erro: str) -> None:
        """
        Log an error inside an especifiedy line.
        Args:
            id (int): Line ID.
            return_code (int): Error code.
            log_erro (str): Log message.
        """
        with session_scope() as session:
            produto = session.query(self.entity).get(id)
            produto.cod_retorno = return_code
            produto.log_erro = str(log_erro)
    
    def log_success_code(self, id: int, return_code: int = ResponseCode.SUCCESS) -> None:
        """
        Log a simple message with the code sucess.
        Args:
            id (int): Line ID.
            return_code (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = return_code
    
    def got_to_sleep(self, id: int, return_code: int = ResponseCode.SUCCESS) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            return_code (int): Code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = return_code
    
    def executing(self, id: int, return_code: int = ResponseCode.EXECUTING) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            return_code (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = return_code
