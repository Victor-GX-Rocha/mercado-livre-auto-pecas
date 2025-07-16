""" Client interface for Mercado Libre API """

import requests
from typing import Any
from decimal import Decimal
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import MeliErrorDetail, MeliResponse, MeliContext


class MLBaseClient:
    BASE_URL: str = "https://api.mercadolibre.com"
    
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
    
    def request(self, method: str, endpoint: str, context: MeliContext, **kwargs) -> MeliResponse:
        url: str = f"{self.BASE_URL}{endpoint}"
        response = None
        
        if "json" in kwargs: # Convert Decimal type to seriazable type.
            kwargs["json"] = self.__convert_decimals(kwargs["json"])
        
        try:
            response = self.session.request(method.upper(), url, **kwargs)
            response.raise_for_status()
            
            return MeliResponse(
                success=True,
                data=response.json(),
                http_status=response.status_code
            )
            
        except requests.HTTPError as exc:
            # Erros 4xx/5xx
            
            http_error = MeliResponse(
                success=False,
                http_status=exc.response.status_code,
                error=MeliErrorDetail(
                    message=f"Erro HTTP {exc.response.status_code}",
                    context=context,  # Contexto específico
                    code=self.__get_error_code(exc.response),
                    http_status=exc.response.status_code,
                    exception=exc,
                    details=response.text if response != None else None
                )
            )
            
            # url_list: list[str] = url.split("/")
            
            # if exc.response.status_code == 404:
            #     index: int = url_list.index("items") if "items" in url_list else None
            #     ml_id: str = url_list[index+1] if index else None
            #     has_no_mlb: bool = True if not "MLB" in ml_id else False
            #     if has_no_mlb:
            #         http_error.error.message += f" | É provável que você tenha esquecido de inserir 'MLB' antes do ID do produto. O que você fez: {ml_id}. Ideal: MLB{ml_id}"
            
            
            return http_error
        
        except requests.RequestException as exc:
            # Erros de conexão, timeout, etc
            return MeliResponse(
                success=False,
                error=MeliErrorDetail(
                    message="Falha na comunicação com a API",
                    context="RequestException",
                    code=1000,  # Código interno para erros de rede
                    exception=exc,
                    details=response.text if response != None else None
                )
            )
            
        except Exception as exc:
            # Erros inesperados
            return MeliResponse(
                success=False,
                error=MeliErrorDetail(
                    message="Erro de requisição inesperado",
                    context="UnspectedException",
                    code=9999,
                    exception=exc,
                    details=response.text if response != None else None
                )
            )
    
    def get(self, endpoint: str, context: MeliContext, **kwargs):
        return self.request("GET", endpoint, context, **kwargs)
    
    def post(self, endpoint: str, context: MeliContext, **kwargs):
        return self.request("POST", endpoint, context, **kwargs)
    
    def put(self, endpoint: str, context: MeliContext, **kwargs):
        return self.request("PUT", endpoint, context, **kwargs)
    
    def delete(self, endpoint: str, context: MeliContext, **kwargs):
        return self.request("DELETE", endpoint, context, **kwargs)
    
    
    def __get_error_code(self, response: requests.Response) -> int:
        """Extrai código de erro da resposta da API"""
        try:
            return response.json().get('error_code', response.status_code)
        except:
            return response.status_code
    
    def __convert_decimals(self, obj: Any) -> Any:
        """ Converte objetos Decimal para float ou int """
        if isinstance(obj, Decimal):
            return float(obj)  # Ou int(obj) se for inteiro
        elif isinstance(obj, dict):
            return {k: self.__convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.__convert_decimals(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.__convert_decimals(item) for item in obj)
        return obj
