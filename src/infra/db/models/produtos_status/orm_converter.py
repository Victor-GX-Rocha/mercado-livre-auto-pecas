""" Converter the Produtos ORM entity to a Product dataclass object. """

from src.infra.db.models.bases import ConvertersBase
from .data_class import ProdutosStatusDataclass
from .orm_entity import ProdutosStatusORM


class ProdutosStausConverter(ConvertersBase):
    def __init__(self):
        super().__init__(ProdutosStatusORM)
    
    """ Provides conversion methodsto transform a ProdutosStatusORM into ProdutosStatusDataclass. """
    def orm_convert(self, orm_obj: ProdutosStatusORM) -> ProdutosStatusDataclass:
        """
        Convert a single Produtos ORM entity to a Product dataclass.
        
        Args:
            orm_obj (Produtos): A single Produtos ORM entity.
        Returns:
            Product: Converted dataclass to instance.
        """
        return ProdutosStatusDataclass(
            id=orm_obj.id,
            credentials=orm_obj.credentials,
            controlers=orm_obj.controlers,
            status_produto=orm_obj.status_produto,
            mercado_livre_id=orm_obj.mercado_livre_id
        )
