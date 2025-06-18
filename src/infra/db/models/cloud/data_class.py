""" Dataclass model for Cloudinary table. """

from dataclasses import dataclass
from typing import Optional

@dataclass
class CloudinaryDataclass:
    id: int
    usuario: Optional[str]
    cloud_name: Optional[str]
    api_key: Optional[str]
    api_secret: Optional[str]
