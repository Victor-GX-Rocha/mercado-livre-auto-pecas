""" Models for auth requests for mercado libre api. """

from dataclasses import dataclass
from typing import Protocol, Optional

@dataclass
class AuthResponse:
    """ Auth response model. """
    access_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    scope: Optional[str]
    user_id: Optional[int]
    refresh_token: Optional[str]

@dataclass
class MeliCredentials:
    """ Parameters for creation of an access token. """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str

class MeliCredentialsProtocol(Protocol):
    """ Typing protocol model for a token parameter credentials. """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str
