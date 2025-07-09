""" Common models for multiple tables """

from typing import TypeVar
from dataclasses import dataclass
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, declared_attr

DataclassTable = TypeVar("DataclassTable")
ORMTable = TypeVar("ORMTable")

class Base(DeclarativeBase):...

@dataclass
class MeliCredentials:
    """ Authentication credential columns for mercado libre tokens """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str

@dataclass
class Controlers:
    """ Operation control columns. """
    operacao: int
    cod_retorno: int
    log_erro: str

class OrmTablesbase(Base):
    __abstract__ = True
    
    client_id: Mapped[str] = mapped_column(String(32))
    client_secret: Mapped[str] = mapped_column(String(64))
    redirect_uri: Mapped[str] = mapped_column(String(256))
    refresh_token: Mapped[str] = mapped_column(String(256))
    
    @declared_attr
    def credentials(cls):
        return composite(
            MeliCredentials,
            cls.client_id,
            cls.client_secret,
            cls.redirect_uri,
            cls.refresh_token,
            deferred=False
        )
    
    operacao: Mapped[int] = mapped_column(Integer)
    cod_retorno: Mapped[int] = mapped_column(Integer)
    log_erro: Mapped[str] = mapped_column(Text)
    
    @declared_attr
    def controlers(cls):
        return composite(
            Controlers,
            cls.operacao,
            cls.cod_retorno,
            cls.log_erro,
            deferred=False
        )


class ConvertersBase:
    """ Provides base conversion methods to create converters classes. """
    def __init__(self, orm_table: ORMTable):
        self.orm_table = orm_table
    
    def convert(
            self, 
            orm_objs: list[ORMTable] | ORMTable
        ) -> list[ORMTable] | DataclassTable:
        """
        Converts a ORM object into a Dataclass.
        Recives a list or the ORM entity directly.
        
        Args:
            orm_objs (list[ORMTable] | ORMTable): A single ORMTable entity or list of entities.
            orm_table (ORMTable): The literal ORMTable class. 
        Returns:
            (list[ORMTable] | Product): Matching Product dataclass object or list of objects.
        Raises:
            TypeError: If input is neither single entity nor lits.
        Example:
            >>> converter.convert(single_orm_entity)
            DataclassTable(...)
            >>> converter.convert([entity1, entity2])
        """
        if type(orm_objs) == self.orm_table:
            return self.orm_convert(orm_objs)
        elif type(orm_objs) == list:
            return self.orms_convert(orm_objs)
        else:
            raise TypeError(f"[{self.__class__.__name__}] Formato de dado inválido: {type(orm_objs)}")
    
    def orm_convert(self, orm_obj: ORMTable) -> DataclassTable:
        """
        (Method created to be subscribed).\n
        Convert a single ORMTable ORM entity to a DataclassTable.
        
        Args:
            orm_obj (ORMTable): A single ORMTable entity.
        Returns:
            DataclassTable: Converted object.
        """
    
    def orms_convert(self, orm_objs: list[ORMTable]) -> list[DataclassTable]:
        """
        Convert a multiple ORMTable entities to DataclassTable.
        
        Args:
            orm_objs (list[ORMTable]): list of converted dataclass instances.
        Returns:
            list[DataclassTable]: list of convert dataclass instances.
        """
        return [self.orm_convert(orm_obj) for orm_obj in orm_objs]
