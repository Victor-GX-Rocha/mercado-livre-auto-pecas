""" SQLAlchemy entity for table cloudinary. """

from sqlalchemy import event, Integer, String, Sequence
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import CreateSequence
from dataclasses import dataclass

from ..bases import Base


@dataclass
class CloudinaryORM(Base):
    __tablename__: str = "cloudinary"
    
    id_seq = Sequence("cloudinary_id_sq1")
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=id_seq.next_value()
    )
    
    usuario: Mapped[str] = mapped_column(String(64))
    cloud_name: Mapped[str] = mapped_column(String(64))
    api_key: Mapped[str] = mapped_column(String(64))
    api_secret: Mapped[str] = mapped_column(String(64))
    
    @classmethod
    def __declare_last__(cls):
        """ Create the sequence after create the table. """
        event.listen(
            target=cls.__table__,
            identifier="after_create",
            fn=CreateSequence(cls.id_seq)
        )
