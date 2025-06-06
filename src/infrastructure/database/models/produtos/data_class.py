""" Dataclass model for produtos table """

from dataclasses import dataclass
from typing import Optional

from ..base import MeliCredentials

@dataclass
class Controlers:
    """ Operation control columns """
    status_operacao_id: int
    operacao: int

@dataclass
class ErrorLoggers:
    """ Error log columns """
    cod_erro: int
    log_erro: Optional[str]

@dataclass
class Identifiers:
    """ Product unique indentiers (Inertal system and Meli) """
    cod_produto: Optional[str]
    sku: Optional[str]
    ml_id_produto: Optional[str]
    link_publicacao: Optional[str]

@dataclass
class SaleData:
    """ Product sale data """
    titulo: Optional[str]
    descricao: Optional[str]
    imagens: Optional[list]
    estoque: Optional[int]
    preco: Optional[float] #numeric(102)
    moeda: Optional[str]
    tipo_anuncio: Optional[str]
    modo_compra: Optional[str]
    termo_garantia: Optional[str]

@dataclass
class ShippimentData:
    """ Product shippiment data """
    modo_envio: Optional[str]
    logistica: Optional[str]
    modo_envio_logistica: Optional[str]
    retirada_local: Optional[bool]
    frete_gratis: Optional[bool]

@dataclass
class CategoryData:
    """ Product category information """
    categoria: Optional[str]
    categoria_id: Optional[str]
    categoria_exemplo: Optional[str]
    categoria_caminho: Optional[str]

@dataclass
class TechnicalData:
    """ Product technical data """
    marca: Optional[str]
    condicao_produto: Optional[str]
    gtin: Optional[str]
    gtin_ausencia_motivo: Optional[str]
    numero_peca: Optional[str]
    num_inmetro: Optional[str]
    cod_oem: Optional[str]
    modelo: Optional[str]
    tipo_veiculo: Optional[str]
    tipo_combustivel: Optional[str]
    tem_compatibilidade: Optional[str]
    origem: Optional[str]

@dataclass
class DimensionsData:
    """ Product dimension data """
    altura: Optional[str]
    largura: Optional[int]
    comprimento: Optional[int]
    peso: Optional[int]

@dataclass
class Product:
    """ Dataclass for `Produtos` table """
    id: int
    credentials: MeliCredentials
    controlers: Controlers
    error_logers: ErrorLoggers
    identfiers: Identifiers
    sale: SaleData
    shippiment: ShippimentData
    category: CategoryData
    technical: TechnicalData
    dimensions: DimensionsData
    produto_status: Optional[str]
    produto_atualizado: Optional[str]
