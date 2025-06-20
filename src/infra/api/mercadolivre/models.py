""" Mercado libre requets models. """

from dataclasses import dataclass
from typing import Optional, Any, Literal


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
    "item_editation",
    "items_listing",
    "get_item_info",
    "get_items_info"
    "item_add_compatibilities"
    "get_models_by_brand",
    "get_compatibilities"
]


@dataclass
class MeliErrorDetail:
    """ Keep mercado libre request error informations. """
    message: str
    context: Optional[MeliContext]
    code: Optional[int] = None
    http_status: Optional[int] = None
    exception: Optional[Exception] = None
    details: Optional[str] = None

@dataclass
class MeliResponse:
    """ Model for mercado libre request responses. """
    success: bool
    data: Optional[Any] = None
    error: Optional[MeliErrorDetail] = None
    http_status: Optional[int] = None
