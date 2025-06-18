""" Converter the Produtos ORM entity to a Product dataclass object. """

from .orm_entity import Produtos
from .data_class import Product

class ProdutosConverter:
    """
    Converts between Produtos ORM entities and Product dataclass objects.
    Provides conversion methods for both single entities and collections
    """
    def convert(self, orm_objs: list[Produtos] | Produtos) -> list[Produtos] | Product:
        """
        Convert Produtos ORM entities to product dataclass objects.
        Handles both single entities and collections automatically.
        
        Args:
            orm_objs (list[Produtos] | Produtos): A single Produtos entity or list of entities.
        Returns:
            (list[Produtos] | Product): Matching Product dataclass object or list of objects.
        Raises:
            TypeError: If input is neither single entity nor lits.
        Example:
            >>> converter.convert(single_orm_entity)
            Product(...)
            >>> converter.convert([entity1, entity2])
        """
        if type(orm_objs) == Produtos:
            return self.orm_convert(orm_objs)
        elif type(orm_objs) == list:
            return self.orms_convert(orm_objs)
        else:
            raise TypeError(f"[{self.__class__.__name__}] Formato de dado inválido: {type(orm_objs)}")
    
    def orm_convert(self, orm_obj: Produtos) -> Product:
        """
        Convert a single Produtos ORM entity to a Product dataclass.
        
        Args:
            orm_obj (Produtos): A single Produtos ORM entity.
        Returns:
            Product: Converted dataclass to instance.
        """
        return Product(
            id=orm_obj.id,
            credentials=orm_obj.credentials,
            controlers=orm_obj.controlers,
            error_logers=orm_obj.error_logers,
            identfiers=orm_obj.identfiers,
            sale=orm_obj.sale,
            shippiment=orm_obj.shippiment,
            category=orm_obj.category,
            technical=orm_obj.technical,
            dimensions=orm_obj.dimensions,
            produto_status=orm_obj.produto_status,
            produto_atualizado=orm_obj.produto_atualizado,
        )
    
    def orms_convert(self, orm_objs: list[Produtos]) -> list[Product]:
        """
        Convert a multiple Pordutos ORM entities to Prodcut datclasses.
        Args:
            orm_objs (list[Produtos]): list of converted dataclass instances.
        Returns:
            list[Product]: list of convert dataclass instances.
        """
        return [self.orm_convert(orm_obj) for orm_obj in orm_objs]
