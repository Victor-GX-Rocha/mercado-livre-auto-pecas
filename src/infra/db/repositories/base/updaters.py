""" Base common update functionalities. """

# database/repositories/base/updatters.py

from ..session import session_scope

class OperationStatus:
    WAITING: int = 1
    EXECUTING: int = 2
    FINILIZED: int = 3

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
            produto.status_operacao_id = 3 # Operação realizda mas houve uma falha
            produto.log_erro = str(log_erro)
            produto.cod_erro = cod_erro
    
    def log_success_code(self, id: int, status_operacao_id: int = OperationStatus.FINILIZED) -> None:
        """
        Log a simple message with the code sucess.
        Args:
            id (int): Line ID.
            status_operacao_id (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.status_operacao_id = status_operacao_id
            line.cod_erro = 0
    
    def got_to_sleep(self, id: int, status_operacao_id: int = OperationStatus.FINILIZED) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            status_operacao_id (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.status_operacao_id = status_operacao_id
            line.cod_erro = 0
    
    def executing(self, id: int, status_operacao_id: int = OperationStatus.EXECUTING) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            status_operacao_id (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.status_operacao_id = status_operacao_id
