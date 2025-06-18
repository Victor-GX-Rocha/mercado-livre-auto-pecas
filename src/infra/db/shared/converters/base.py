""" Base for dataclass converters """


# Versão provisória, organizar e formalizar depois.

from typing import List, Dict, Any, Union, Iterable
from dataclasses import is_dataclass, fields

class BaseDataclassConverter:
    """ Base converter for ORM entities to dataclasses with improved patterns """
    
    @staticmethod
    def convert(
        data: Union[object, Dict[str, Any]], 
        target_dataclass: type
    ) -> object:
        """
        Converts a single item to the target dataclass
        
        Args:
            data: Source data (ORM entity or dict)
            target_dataclass: Dataclass type to convert to
            
        Returns:
            Instance of target_dataclass with populated data
        """
        if isinstance(data, dict):
            return BaseDataclassConverter._from_dict(data, target_dataclass)
        elif hasattr(data, '__table__'):  # SQLAlchemy model check
            return BaseDataclassConverter._from_orm(data, target_dataclass)
        else:
            raise TypeError(f"Falha de conversão. Tipo de dado não suportado: {type(data)}")
    
    @staticmethod
    def convert_many(
        items: Iterable[Union[object, Dict[str, Any]]], 
        target_dataclass: type
    ) -> List[object]:
        """
        Converts multiple items to the target dataclass
        
        Args:
            items: Iterable of source data
            target_dataclass: Dataclass type to convert to
            
        Returns:
            List of converted items
        """
        return [BaseDataclassConverter.convert(item, target_dataclass) for item in items]
    
    @staticmethod
    def _from_dict(data: Dict[str, Any], target_dataclass: type) -> object:
        """
        Convert from dictionary to dataclass using field mapping
        
        Args:
            data (Dict[str, Any]): Dictionary to converto into dataclass
            target_dataclass (type): Dataclass type to convert to
        Returns:
            object: A dataclass object
        """
        if not is_dataclass(target_dataclass):
            raise TypeError("target_dataclass Deve ser um dataclass")
        
        # Get field names from dataclass
        field_names = {f.name for f in fields(target_dataclass)}
        
        # Filter and map data
        filtered_data = {
            field_name: data[field_name] 
            for field_name in field_names 
            if field_name in data
        }
        
        return target_dataclass(**filtered_data)
    
    @staticmethod
    def _from_orm(orm_obj: object, target_dataclass: type) -> object:
        """Convert from ORM entity to dataclass using attribute mapping"""
        if not is_dataclass(target_dataclass):
            raise TypeError("target_dataclass Deve ser um dataclass")
        
        # Get field names from dataclass
        field_names = {f.name for f in fields(target_dataclass)}
        
        # Collect data from ORM object
        orm_data = {}
        for field_name in field_names:
            # Handle nested dataclasses
            attr = getattr(orm_obj, field_name)
            
            if is_dataclass(attr):
                # Recursive conversion for nested dataclasses
                orm_data[field_name] = BaseDataclassConverter._from_orm(attr, type(attr))
            elif isinstance(attr, list):
                # Handle lists of nested objects
                orm_data[field_name] = [
                    BaseDataclassConverter._from_orm(item, type(item[0])) 
                    for item in attr
                ]
            else:
                orm_data[field_name] = attr
        
        return target_dataclass(**orm_data)

"""
"Faça a coisa mais simples que possa funcionar hoje, mas desenhe sistemas que possam evoluir amanhã." - Adaptado de Martin Fowler

Eu não vou precisar disso agora, mas já estou desenhando o sistema que posso usar amanhã.
"""

""" 
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, source) -> DataClass:...

class ProdutoOrmConverter(BaseConverter):...

class ProdutoDictConverter(BaseConverter):...

"""

""" 
# Outro esboço
from abc import ABC, abstractmethod
from typing import Type, TypeVar

DataClassType = TypeVar("DataClassType")

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, source) -> Type[DataClassType]:...

class ProdutoOrmConverter(BaseConverter):...

class ProdutoDictConverter(BaseConverter):...
"""