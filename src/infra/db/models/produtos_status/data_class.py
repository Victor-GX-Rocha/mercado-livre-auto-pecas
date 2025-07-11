""" Dataclass model for produtos_status table. """

from dataclasses import dataclass
from typing import Optional

from src.infra.db.models.bases import MeliCredentials, OperationControllers

@dataclass
class ProdutosStatusDataclass:
    """ Dataclass to represents the produtos_status table. """
    id: int
    credentials: MeliCredentials
    controllers: OperationControllers
    status_produto: Optional[str]
    mercado_livre_id: Optional[str]
