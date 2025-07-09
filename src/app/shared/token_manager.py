""" Manager the creation of meercado libre API token for an user application """

from typing import Optional

from src.infra.db.repo.models import ResponseCode
from src.infra.db.repo.models import DataclassTable
from src.infra.api.mercadolivre.auth import MeliAuthCredentials, AuthResponse
from src.infra.db.repo.interfaces.base_protocol import TableRepositoryProtocol


# Criar um modélo de repositorie para usar como typing

class MeliTokenManager:
    """ Gets and validation the creation of a token. """
    def __init__(
        self, 
        repo: TableRepositoryProtocol, 
        meli_auth: MeliAuthCredentials
    ) -> None:
        """
        
        Args:
            repo (TableRepositoryProtocol): Table repository.
            meli_auth (MeliAuthCredentials): Mercado libre auth tools.
        """
        self.repo = repo
        self.auth = meli_auth
    
    def get_token(self, lines: list[DataclassTable]) -> Optional[AuthResponse]:
        """
        Get an mercado libre auth token and valids the process.
        Args:
            line (list[DataclassTable]): Table line.
        Returns:
            AuthResponse: If the request was successful, else None.
        """
        for line in lines: # Note: Later, change this "if not" to "try except", aat this way, you only need to return None.
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
        Returns:
            bool: False if any value is empty, else True.
        """
        if not all([
            line.credentials.client_id,
            line.credentials.client_secret,
            line.credentials.redirect_uri,
            line.credentials.refresh_token
        ]):
            self.repo.update.log_error(
                id=line.id, 
                cod_erro=ResponseCode.TABLE_ERROR, 
                log_erro="Informações de credencial de usuário ausentes!!"
            )
            return None
        return True
    
    def _make_request(self, line: DataclassTable) -> Optional[AuthResponse]:
        """
        Makes the auth request for mercado libre. 
        Args:
            line (DataclassTable): Table line.
        Returns:
            AuthResponse: If the request was successful, else None.
        """
        token = self.auth.get_refresh_token(line.credentials)
        if not token.success:
            self.repo.update.log_error(
                id=line.id, 
                cod_erro=ResponseCode.PROGRAM_ERROR, 
                log_erro=str(token.error)
            )
            return None
        return token
