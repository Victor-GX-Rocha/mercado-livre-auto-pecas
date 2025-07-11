"""
Core models and abstractions for database operations.

Provides reusable components for:
- ORM base classes.
- Common column patterns (credentials, controllers).
- Base converter implementations.

Classes:
    Base: SQLAlchemy declarative base class.
    MeliCredentials: Dataclass for Mercado Libre authentication credentials.
    OperationControllers: Dataclass for operational control attributes.
    OrmBaseModel: Abstract ORM model combining credentials and controllers.
    ConvertersBase: Base class for ORM-to-dataclass conversions.

TypeVars:
    DataclassTable: Represents a dataclass model.
    ORMTable: Represents an ORM model entity.
"""


from typing import TypeVar
from dataclasses import dataclass
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, declared_attr

DataclassTable = TypeVar("DataclassTable") # Represents a dataclass model used for business logic.
ORMTable = TypeVar("ORMTable") # Represents an ORM model mapped to database tables.

class Base(DeclarativeBase):...

@dataclass
class MeliCredentials:
    """
    Represents Mercado Libre authentication credentials.
    
    Used as a composite type in ORM models to encapsulate:
    - client_id: Application identifier.
    - client_secret: Application secret key.
    - redirect_uri: OAuth callback URI.
    - refresh_token: Token for refreshing access credentials.
    """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str

@dataclass
class OperationControllers:
    """
    Represents operational control attributes for database records.
    
    Attributes:
        operation_code: Current operation status
        return_code: Result code from last operation
        error_log: Detailed error message if operation failed
    """
    operacao: int
    cod_retorno: int
    log_erro: str

class OrmBaseModel(Base):
    """
    Abstract base class for ORM models with credential and controller composites.
    
    Provides:
    - Standard credential columns (client_id, client_secret, etc.).
    - Composite property 'credentials' mapping to MeliCredentials dataclass.
    - Standard controller columns (operation_code, return_code, etc.).
    - Composite property 'controllers' mapping to OperationControllers dataclass.
    """
    __abstract__ = True
    
    client_id: Mapped[str] = mapped_column(String(32))
    client_secret: Mapped[str] = mapped_column(String(64))
    redirect_uri: Mapped[str] = mapped_column(String(256))
    refresh_token: Mapped[str] = mapped_column(String(256))
    
    @declared_attr
    def credentials(cls):
        """
        Composite property mapping credential columns to MeliCredentials dataclass.
        
        Used for type-safe access to credential attributes as a single object.
        """
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
    def controllers(cls):
        """
        Composite property mapping control columns to OperationControllers dataclass.
        
        Provides structured access to operational control attributes.
        """
        return composite(
            OperationControllers,
            cls.operacao,
            cls.cod_retorno,
            cls.log_erro,
            deferred=False
        )


class ConvertersBase:
    """
    Base class for converting between ORM entities and dataclasses.
    
    Subclasses must implement the `orm_convert` method for specific type conversion.
    """
    def __init__(self, orm_table: ORMTable):
        """
        Initialize converter for a specific ORM type.
        
        Args:
            orm_table: The ORM model class to convert from
        """
        self.orm_table = orm_table
    
    def convert(
            self, 
            orm_objs: list[ORMTable] | ORMTable
        ) -> list[ORMTable] | DataclassTable:
        """
        Convert ORM entities to dataclass objects.
        
        Handles both single entities and collections.
        
        Args:
            orm_objs: Single ORM entity or list of entities.
        
        Returns:
            Matching dataclass object or list of objects.
        
        Raises:
            TypeError: For unsupported input types.
        
        Example:
            >>> converter.convert(single_entity)
            DataclassTable(...)
            >>> converter.convert([entity1, entity2])
            [DataclassTable(...), DataclassTable(...)]
        """
        if type(orm_objs) == self.orm_table:
            return self.orm_convert(orm_objs)
        elif type(orm_objs) == list:
            return self.orms_convert(orm_objs)
        else:
            raise TypeError(f"[{self.__class__.__name__}] Formato de dado inválido: {type(orm_objs)}")
    
    def orm_convert(self, orm_obj: ORMTable) -> DataclassTable:
        """
        Convert a single ORM entity to dataclass (MUST be implemented by subclass).
        
        Args:
            orm_obj (ORMTable): A single ORM entity.
        
        Returns:
            DataclassTable: Converted dataclass instance.
        
        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def orms_convert(self, orm_objs: list[ORMTable]) -> list[DataclassTable]:
        """
        Convert multiple ORM entities to dataclasses.
        
        Args:
            orm_objs (list[ORMTable]): List of ORM entities
        
        Returns:
            list[DataclassTable]: List of converted dataclass instances
        """
        return [self.orm_convert(orm_obj) for orm_obj in orm_objs]
