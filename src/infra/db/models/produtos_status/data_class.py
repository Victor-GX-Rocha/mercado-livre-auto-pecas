""" Dataclass model for produtos_status table. """

from dataclasses import dataclass
from typing import Optional

from src.infra.db.models.bases import MeliCredentials, Controlers

@dataclass
class ProdutosStatusDataclass:
    id: int
    credentials: MeliCredentials
    controlers: Controlers
    status_produto: Optional[str]
    mercado_livre_id: Optional[str]
