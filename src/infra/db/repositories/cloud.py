""" CRUD operations for Cloudinary table. """

# database/repositories/produtos.py

# from session import session_scope
# from session.session_manager import session_scope
from src.infra.db.repositories.session import session_scope
from ..models.cloud import CloudinaryORM, CloudinaryDataclass, CloudinaryConverter
from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

converter = CloudinaryConverter()

class CloudinaryGetMethods:
    """ Read (GET) methods for Cloudinary table entity. """
    def __init__(self, entity: CloudinaryORM):
        """
        Args:
            entity (CloudinaryORM): Cloudinary table entity.
        """
        self.entity = entity
        self.converter = converter
    
    def user(self, user_name: str) -> list[CloudinaryDataclass]:
        """
        Returns a line with user credentials data.
        Args:
            user_name (str): Cloudinary user. (Identifier fo table line.)
        Returns:
            list[CloudinaryDataclass]: Returns a list with a single line what contains a user credentials data.
        """
        with session_scope() as session:
            user: list[CloudinaryORM] = session.query(CloudinaryORM).filter(CloudinaryORM.usuario == "Victor").all()
            # print(f"{user = }")
            return self.converter.convert(user)


class CloudinaryUpdateMethods:
    """ Update methods for Cloudinary table entity. """
    def __init__(self, entity: CloudinaryORM):
        """
        Args:
            entity (Cloudinary): CloudinaryORM table entity.
        """
        self.entity = entity


class CloudinaryInsertMethods(BaseDeleteMethods):
    """ Delete methods for Cloudinary table entity. """
    def __init__(self, entity: CloudinaryORM):
        """
        Args:
            entity (CloudinaryORM): Cloudinary table entity.
        """
        self.entity = entity


class CloudinaryDeleteMethods(BaseInsertMethods):
    """ Create (Insert) methods for Cloudinary table entity. """
    def __init__(self, entity: CloudinaryORM):
        """
        Args:
            entity (CloudinaryORM): Cloudinary table entity.
        """
        self.entity = entity


class CloudinaryRepository:
    """ SQL commands for table Cloudinary. """
    def __init__(self):
        self.get = CloudinaryGetMethods(CloudinaryORM)
        self.update = CloudinaryUpdateMethods(CloudinaryORM)
        self.insert = CloudinaryInsertMethods(CloudinaryORM)
        self.delete = CloudinaryDeleteMethods(CloudinaryORM)
