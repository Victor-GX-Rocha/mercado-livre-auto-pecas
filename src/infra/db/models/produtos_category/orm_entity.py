""" SQLAlchemy entity for table operacao_categoria_ml. """

from sqlalchemy.schema import CreateSequence
from sqlalchemy.orm import Mapped, mapped_column, composite
from sqlalchemy import event, Sequence, String, Text, Integer, CHAR

from src.infra.db.models.bases import OrmBaseModel
from .data_class import ProdutosCategory


class ProdutosCategoryORM(OrmBaseModel):
    
    __tablename__: str = "operacao_categoria_ml"
    id_seq = Sequence("produtos_category_sq1")
    
    id: Mapped[int] = mapped_column(
        Integer,
        id_seq,
        primary_key=True,
        server_default=id_seq.next_value()
    )
    
    categoria_id: Mapped[str] = mapped_column(String(20))
    nome_categoria: Mapped[str] = mapped_column(Text)
    titulo_produto: Mapped[str] = mapped_column(String(60))
    category = composite(
        ProdutosCategory,
        "categoria_id",
        "nome_categoria",
        "titulo_produto"
    )
    
    cod_produto: Mapped[str] = mapped_column(String(12))
    atualizado: Mapped[str] = mapped_column(CHAR(1), default='N')
    
    @classmethod
    def __declare_last__(cls):
        """ Create the sequence after create the table. """
        event.listen(
            target=cls.__table__,
            identifier="after_create",
            fn=CreateSequence(cls.id_seq)
        )
