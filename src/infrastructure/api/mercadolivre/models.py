""" Guarda os modelos que serão utilizados pelos recursos do associados a comunicação com o mercado livre """

from dataclasses import dataclass
from typing import Optional, Any, Union, Literal


# Define contextos válidos e já evita erros de digitação tlg
MeliContext = Literal[
    "RequestException",
    "UnspectedException"
    "auth",
    "category_root_types",
    "category_data",
    "category_attributes",
    "image_upload",
    "item_publication",
    "item_description",
    "item_editation"
    
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
    details: Optional[str] = None

@dataclass
class MeliResponse:
    """ Model for mercado libre request responses. """
    success: bool
    data: Optional[Any] = None
    error: Optional[MeliErrorDetail] = None
    http_status: Optional[int] = None
