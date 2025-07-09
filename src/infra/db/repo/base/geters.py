""" Base common get functionalities. """

from src.infra.db.repo.session import session_scope
from src.infra.db.repo.models import ResponseCode, TableEntity, DataclassTable


class StatusOperationGetters:
    """ Finders based on status_operacao_id column value. Pressets search methods for user interface. """
    
    def by_column_value(self, operacao: int) -> list[DataclassTable]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (list[DataclassTable]): list of a DataclassTable objects. (Empty list if it not exists).
        """
        with session_scope() as session:
            operations = session.query(self.entity).filter(self.entity.cod_retorno == operacao).all()
            return self.converter.convert(operations)
    
    def pending_operations(self) -> list[TableEntity]:
        """ Get pending operations. """
        return self.by_column_value(ResponseCode.PENDING)
    
    def completed_operations(self) -> list[TableEntity]:
        """ Get completed operations. """
        return self.by_column_value(ResponseCode.SUCCESS)
    
    def in_process_operations(self) -> list[TableEntity]:
        """ Get in-process operations. """
        return self.by_column_value(ResponseCode.EXECUTING)
