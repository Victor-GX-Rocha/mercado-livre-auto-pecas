""" Common models for multiple tables """

from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):...


@dataclass
class MeliCredentials:
    """ Authentication credential columns for mercado libre tokens """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str
