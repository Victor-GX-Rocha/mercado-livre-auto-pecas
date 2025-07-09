""" SQLAlchemy entity for table produtos_status """

from sqlalchemy import event, Sequence, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, composite
from sqlalchemy.schema import CreateSequence

from src.infra.db.models.bases import OrmTablesbase, MeliCredentials, Controlers

class ProdutosStatusORM(OrmTablesbase):
    
    __tablename__: str = "produtos_status"
    id_seq = Sequence("produtos_status_sq1")
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=id_seq.next_value()
    )
    
    status_produto: Mapped[str] = mapped_column(String(16))
    mercado_livre_id: Mapped[str] = mapped_column(String(16))
    
    @classmethod
    def __declare_last__(cls):
        """ Create the sequence after create the table. """
        event.listen(
            target=cls.__table__,
            identifier="after_create",
            fn=CreateSequence(cls.id_seq)
        )
