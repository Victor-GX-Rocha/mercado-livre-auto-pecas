""" Base common get functionalities. """

# database/repositories/base/getters.py

from ..session import session_scope
from .base import TableEntity, TableDataclass
from .models import StatusOperationTypes


class StatusOperationGetters:
    """ Finders based on status_operacao_id column value. Pressets search methods for user interface. """
    
    def by_status_operacao(self, operacao: int) -> list[TableDataclass]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (list[TableDataclass]): list of a TableDataclass objects. (Empty list if it not exists).
        """
        with session_scope() as session:
            operations = session.query(self.entity).filter(self.entity.status_operacao_id == operacao).all()
            return self.converter.convert(operations)
    
    def pending_operations(self) -> list[TableEntity]:
        """ Get pending operations """
        return self.by_status_operacao(StatusOperationTypes.PENDING)
    
    def completed_operations(self) -> list[TableEntity]:
        """ Get completed operations """
        return self.by_status_operacao(StatusOperationTypes.COMPLETED)
    
    def in_process_operations(self) -> list[TableEntity]:
        """ Get in-process operations """
        return self.by_status_operacao(StatusOperationTypes.IN_PROCESS)
