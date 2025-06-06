"""  """

from dataclasses import dataclass
from typing import Protocol, Optional

@dataclass
class AuthResponse:
    access_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    scope: Optional[str]
    user_id: Optional[int]
    refresh_token: Optional[str]

class MeliCredentialsProtocol(Protocol):
    """ Tranforma as credenciais em protocolo. Define formato padrão de dados a ser seguido """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str

@dataclass
class MeliCredentials:
    """ Campos comuns a todas as tabelas que requerem autenticação """
    client_id: str
    client_secret: str
    redirect_uri: str
    refresh_token: str
