""" Guarda os modelos que serão utilizados pelos recursos do associados a comunicação com o mercado livre """

from dataclasses import dataclass
from typing import Optional, Any, Union, Literal


# Define contextos válidos e já evita erros de digitação tlg
MeliContext = Literal[
    "auth",
    "category_data",
    "category_attributes",
    "RequestException",
    "image_upload"
    # "product_publish", 
    # "product_update",
    # "category_management",
    # "order_processing"
]


@dataclass
class MeliErrorDetail:
    """ Guarda as informalções de erro associadas a uma request ao mercado livre. """
    message: str                            # Mensagem amigável para UI
    context: Optional[MeliContext]          # Contexto da operação (ex: "auth")
    code: Optional[int] = None              # Código específico do Mercado Livre 
    http_status: Optional[int] = None       # Código de resposta http
    exception: Optional[Exception] = None   # Exceção original (para logs)

@dataclass
class MeliResponse:
    """ Método padronizado de retorno a uma request do mercado livre. """
    success: bool
    data: Optional[Any] = None
    error: Optional[MeliErrorDetail] = None
    http_status: Optional[int] = None
    
    # @property
    # def is_success(self) -> bool:
    #     return self.success and self.error is None
