""" Manager the creation of meercado libre API token for an user application """

from typing import Any

from ...infrastructure.api.mercadolivre.auth import MeliAuthCredentials
from ...infrastructure.database.repositories.models import TableRepository, TableDataclass

# Criar um modélo de repositorie para usar como typing

class MeliTokenManager:
    """ Gets and validation the crateon af a token """
    def __init__(self, meli_auth: MeliAuthCredentials, repo: TableRepository):
        self.auth = meli_auth
        self.repo = repo
    
    def get_token(self, lines: list[TableDataclass]):
        """
        Get an mercado libre auth token and valids the process.
        """
        for line in lines:
            if not self._has_empty_column(line):
                return None
            
            response = self._make_request(line)
            if not response:
                return None
            
            print(response)
            return response
    
    def _has_empty_column(self, line: TableDataclass):
        # verify if a column is empty
        
        if not all([
            line.credentials.client_id,
            line.credentials.client_secret,
            line.credentials.redirect_uri,
            line.credentials.refresh_token
        ]):
            self.repo.update.log_error(line.id, 88, "Informações de credencial de usuário ausentes!!")
            return None
        return True
    
    def _make_request(self, line: TableDataclass):
        token = self.auth.refresh_token(line.credentials)
        if not token.success:
            # print(line.error_logers)
            self.repo.update.log_error(line.id, 89, str(token.error))
            return None
        return token