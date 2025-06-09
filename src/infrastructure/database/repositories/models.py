""" Repositorie model for typing """

from typing import Protocol, TypeVar
# from dataclasses import # eu queria ago que realmente represente uma dataclass de forma genérica

TableDataclass = TypeVar("TableDataclass")

class OrmTable:...

class OrmEntity:
    def __init__(self, entity: OrmTable):
        """
        Args:
            entity (OrmTable): Any ORM table entity.
        """
        self.entity = entity

class StatusOperationGetters:
    """ Finders based on status_operacao_id column value.  Pressets search methods for user interface. """
    
    def by_status_operacao(self, operacao: int) -> list[TableDataclass]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (List[TableDataclass]): List of TableDataclass. (Empty list if it not exists).
        """
    
    def pending_operations(self) -> list[TableDataclass]:
        """ Get pending operations """
    
    def completed_operations(self) -> list[TableDataclass]:
        """ Get completed operations """
    
    def in_process_operations(self) -> list[TableDataclass]:
        """ Get in-process operations """

class TableGetMethods(OrmEntity, StatusOperationGetters):...
class TableUpdateMethods(OrmEntity):...
class TableInsertMethods(OrmEntity):...
class TableDeleteMethods(OrmEntity):...

class TableRepositoryProtocol(Protocol):
    def __init__(self):
        self.get = TableGetMethods(OrmTable)
        self.update = TableUpdateMethods(OrmTable)
        self.insert = TableInsertMethods(OrmTable)
        self.delete = TableDeleteMethods(OrmTable)

