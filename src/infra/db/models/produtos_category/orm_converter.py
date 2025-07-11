""" Convert the ProdutosCategoryORM entity to a dataclass instance. """

from src.infra.db.models.bases import ConvertersBase
from .data_class import ProdutosCategoryDataclass
from .orm_entity import ProdutosCategoryORM

class ProdutosCategoryConverter(ConvertersBase):
    """ Provides conversion methods to transform a ProdutosCategoryORM into ProdutosCategoryDataclass. """
    def __init__(self):
        super().__init__(ProdutosCategoryORM)
    
    def orm_convert(self, orm_obj: ProdutosCategoryORM) -> ProdutosCategoryDataclass:
        """
        Convert a single ProdutosCategoryORM entity to a ProdutosCategoryDataclass.
        
        Args:
            orm_obj (ProdutosCategoryORM): A single ProdutosCategoryORM entity.
        Returns:
            ProdutosCategoryDataclass: Converted dataclass to instance.
        """
        return ProdutosCategoryDataclass(
            id=orm_obj.id,
            credentials=orm_obj.credentials,
            controllers=orm_obj.controllers,
            category=orm_obj.category,
            cod_produto=orm_obj.cod_produto,
            atualizado=orm_obj.atualizado
        )
