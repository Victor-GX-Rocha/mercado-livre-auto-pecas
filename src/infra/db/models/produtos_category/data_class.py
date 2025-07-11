""" Dataclass for table operacao_categoria_ml. """

from typing import Optional
from dataclasses import dataclass
from src.infra.db.models.bases import MeliCredentials, OperationControllers

@dataclass
class ProdutosCategory:
    """
    Columns used to keep/discover a piece of category information.
    
    - categoria_id: ID of the category. Ex.: "MLB251640".
    - nome_categoria: Category path. Ex.: "Acessórios para Veículos > Segurança Veicular > Porcas de Roda"
    - titulo_produto: Product title. Ex.: "PORCA RODA SP 412D/413CDI USD"
    """
    categoria_id: Optional[str]
    nome_categoria: Optional[str]
    titulo_produto: Optional[str]


@dataclass
class ProdutosCategoryDataclass:
    """ Dataclass to represets the table operacao_categoria_ml. """
    id: int
    credentials: MeliCredentials 
    controllers: OperationControllers
    category: ProdutosCategory
    cod_produto: str
    atualizado: str
