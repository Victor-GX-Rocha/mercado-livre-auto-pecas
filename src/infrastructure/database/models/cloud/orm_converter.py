""" Converter the CloudinaryORM entity to a CloudinaryDataclass object. """

from .orm_entity import CloudinaryORM
from .data_class import CloudinaryDataclass

class CloudinaryConverter:
    def convert(self, orm_objs: CloudinaryORM | list[CloudinaryORM]) -> CloudinaryDataclass | list[CloudinaryDataclass]:
        """
        Convert a single or list CloudinaryORM entityies into a CloudinaryDataclass
        Args:
            orm_objs (CloudinaryORM | list[CloudinaryORM]): A single CloudinaryORM or a list of it.
        Returns:
            CloudinaryDataclass: If the orm_objs is a CloudinaryORM.
            list[CloudinaryDataclass]: If the orm_objs is a list of CloudinaryORM.
        Raises:
            
        """
        if type(orm_objs) == CloudinaryORM:
            return self.orm_convert(orm_objs)
        elif type(orm_objs) == list:
            return [self.orm_convert(item) for item in orm_objs]
        else:
            raise TypeError(f"[{self.__class__.__name__}] Formato de dado inválido: {type(orm_objs)}")
    
    def orm_convert(self, orm_object: CloudinaryORM) -> CloudinaryDataclass:
        """
        Converts a Cloudinary table ORM objeto into a Cloudinary dataclass.
        Args:
            CloudinaryORM: Cloudinary table ORM entity.
        Returns:
            CloudinaryDataclass: Dataclass with the Cloudinary table data.
        """
        return CloudinaryDataclass(
            id=orm_object.id,
            usuario=orm_object.usuario,
            cloud_name=orm_object.cloud_name,
            api_key=orm_object.api_key,
            api_secret=orm_object.api_secret
        )
