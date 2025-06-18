""" Manager the creation of meercado libre API token for an user application """

from typing import Optional

from ...infra.db.repositories.interfaces.base_protocol import TableRepositoryProtocol
from ...infra.api.mercadolivre.auth import MeliAuthCredentials, AuthResponse
from ...infra.db.repositories.models import DataclassTable


# Criar um modélo de repositorie para usar como typing

class MeliTokenManager:
    """ Gets and validation the creation of a token. """
    def __init__(self, repo: TableRepositoryProtocol, meli_auth: MeliAuthCredentials):
        self.repo = repo
        self.auth = meli_auth
    
    def get_token(self, lines: list[DataclassTable]) -> Optional[AuthResponse]:
        """
        Get an mercado libre auth token and valids the process.
        Args:
            line (list[DataclassTable]): Table line.
        """
        for line in lines:
            if not self._has_empty_column(line):
                return None
            
            response = self._make_request(line)
            if not response:
                return None
            
            print(response)
            return response
    
    def _has_empty_column(self, line: DataclassTable) -> Optional[bool]:
        """
        Verify if there exists an empty column.
        Args:
            line (DataclassTable): Table line.
        """
        # print(f"_has_empty_column: {line}")
        if not all([
            line.credentials.client_id,
            line.credentials.client_secret,
            line.credentials.redirect_uri,
            line.credentials.refresh_token
        ]):
            self.repo.update.log_error(line.id, 88, "Informações de credencial de usuário ausentes!!")
            return None
        return True
    
    def _make_request(self, line: DataclassTable) -> Optional[AuthResponse]:
        """
        Makes the auth request for mercado libre. 
        Args:
            line (DataclassTable): Table line.
        """
        token = self.auth.get_refresh_token(line.credentials)
        if not token.success:
            # print(line.error_logers)
            self.repo.update.log_error(line.id, 89, str(token.error))
            return None
        return token
