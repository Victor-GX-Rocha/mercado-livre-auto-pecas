"""  """

from ..client import MLBaseClient
from ..models import MeliResponse, MeliErrorDetail
from .models import AuthResponse

class AuthManager:
    def __init__(self, client: MLBaseClient):
        self.client = client
    
    def get_refresh_token(self, client_id: str, client_secret: str, redirect_uri: str, refresh_token: str) -> MeliResponse:
        payload = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'refresh_token': refresh_token
        }
        
        response = self.client.post(
            endpoint='/oauth/token',
            data=payload,
            context="auth"  # Novo parâmetro para contexto
        )
        
        if not response.success:
            return response
        
        try:
            # Mapeamento explícito e seguro
            auth_data = AuthResponse(
                access_token=response.data['access_token'],
                token_type=response.data['token_type'],
                expires_in=response.data['expires_in'],
                scope=response.data['scope'],
                user_id=response.data['user_id'],
                refresh_token=response.data['refresh_token']
            )
            return MeliResponse(
                success=True,
                data=auth_data,
                http_status=response.http_status
            )
            
        except KeyError as key:
            return MeliResponse(
                success=False,
                error=MeliErrorDetail(
                    message=f"Resposta da API inválida: campo faltando {str(key)}",
                    context="auth",
                    exception=key
                )
            )
