""" Conectar as ferramentas de conexão com o mercado livre e demais funcionalidades do programa """

from .models import MeliCredentialsProtocol
from .manager import AuthManager, AuthResponse

class MeliAuthAdapter:
    """ Adpta o formato padrão de colunas de credenciais com o método de refresh token """
    
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
    
    def refresh_token(self, credentials: MeliCredentialsProtocol) -> AuthResponse:
        """ Refresh token configurado para suportar o modelo de colunas com credenciais """
        return self.auth_manager.get_refresh_token(
            credentials.client_id,
            credentials.client_secret,
            credentials.redirect_uri,
            credentials.refresh_token
        )
