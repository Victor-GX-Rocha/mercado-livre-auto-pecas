""" An adapter to pissibilite the directly use of a "table.cretentials" with the AuthManager. """

from .models import MeliCredentialsProtocol
from .manager import AuthManager, AuthResponse

class MeliAuthCredentials:
    """ An interface between the AuthManager and credentials coluns of a table. """
    
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
    
    def get_refresh_token(self, credentials: MeliCredentialsProtocol) -> AuthResponse:
        """ 
        Gets an refresh token based an "table.credentials" object.
        Args:
            credentials (MeliCredentialsProtocol): The credentials coluns of a table.
        Returns:
            AuthResponse: A dataclass object with the auth response content.
        """
        return self.auth_manager.get_refresh_token(
            credentials.client_id,
            credentials.client_secret,
            credentials.redirect_uri,
            credentials.refresh_token
        )
