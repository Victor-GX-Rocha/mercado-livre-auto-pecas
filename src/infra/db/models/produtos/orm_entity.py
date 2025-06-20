""" SQLAlchemy entity for table produtos """

from sqlalchemy import event, Integer, String, Text, Boolean, Sequence, Numeric
from sqlalchemy.orm import Mapped, mapped_column, composite #DeclarativeBase, 
from sqlalchemy.schema import CreateSequence
from dataclasses import dataclass

from ..base import Base
from .data_class import (
    MeliCredentials,
    Controlers,
    ErrorLoggers,
    Identifiers,
    SaleData,
    ShippimentData,
    CategoryData,
    TechnicalData,
    DimensionsData
)


# @dataclass
class Produtos(Base):
    __tablename__: str = "produtos"
    
    id_seq = Sequence("produtos_id_sq1")
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=id_seq.next_value()
    )
    
    client_id: Mapped[str] = mapped_column(String(32))
    client_secret: Mapped[str] = mapped_column(String(64))
    redirect_uri: Mapped[str] = mapped_column(String(256))
    refresh_token: Mapped[str] = mapped_column(String(256))
    credentials = composite(MeliCredentials, 
        "client_id",
        "client_secret",
        "redirect_uri",
        "refresh_token",
        deferred=False
    )
    
    status_operacao_id: Mapped[int] = mapped_column(Integer)
    operacao: Mapped[int] = mapped_column(Integer)
    controlers = composite(Controlers, 
        status_operacao_id, 
        operacao,
        deferred=False
    )
    
    cod_erro: Mapped[int] = mapped_column(Integer)
    log_erro: Mapped[str] = mapped_column(Text)
    error_logers = composite(ErrorLoggers, "cod_erro", "log_erro")
    
    cod_produto: Mapped[str] = mapped_column(String(16))
    sku: Mapped[str] = mapped_column(String(64))
    ml_id_produto: Mapped[str] = mapped_column(String(32))
    link_publicacao: Mapped[str] = mapped_column(Text)
    identfiers = composite(Identifiers, 
        "cod_produto",
        "sku",
        "ml_id_produto",
        "link_publicacao",
        deferred=False
    )
    
    titulo: Mapped[str] = mapped_column(Text)
    descricao: Mapped[str] = mapped_column(Text)
    imagens: Mapped[str] = mapped_column(String(1024))
    estoque: Mapped[int] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Numeric(10, 2)) #numeric(10, 2)
    moeda: Mapped[str] = mapped_column(String(4), default="MLB") #'MLB'::character varying,
    tipo_anuncio: Mapped[str] = mapped_column(String(32))
    modo_compra: Mapped[str] = mapped_column(String(32))
    termo_garantia: Mapped[str] = mapped_column(String(32))
    sale = composite(SaleData, 
        "titulo",
        "descricao",
        "imagens",
        "estoque",
        "preco",
        "moeda",
        "tipo_anuncio",
        "modo_compra",
        "termo_garantia",
        deferred=False
    )
    
    modo_envio: Mapped[str] = mapped_column(String(32))
    logistica: Mapped[str] = mapped_column(String(32))
    modo_envio_logistica: Mapped[str] = mapped_column(String(32))
    retirada_local: Mapped[bool] = mapped_column(Boolean)
    frete_gratis: Mapped[bool] = mapped_column(Boolean)
    shippiment = composite(ShippimentData, 
        "modo_envio",
        "logistica",
        "modo_envio_logistica",
        "retirada_local",
        "frete_gratis",
        deferred=False
    )
    
    categoria: Mapped[str] = mapped_column(Text)
    categoria_id: Mapped[str] = mapped_column(String(25))
    categoria_exemplo: Mapped[str] = mapped_column(String(1024))
    categoria_caminho: Mapped[str] = mapped_column(String(2048))
    category = composite(CategoryData, 
        "categoria",
        "categoria_id",
        "categoria_exemplo",
        "categoria_caminho",
        deferred=False
    )
    
    marca: Mapped[str] = mapped_column(String(32))
    condicao_produto: Mapped[str] = mapped_column(String(16))
    gtin: Mapped[str] = mapped_column(String(32))
    gtin_ausencia_motivo: Mapped[str] = mapped_column(String(32))
    numero_peca: Mapped[str] = mapped_column(String(100))
    num_inmetro: Mapped[str] = mapped_column(String(100))
    cod_oem: Mapped[str] = mapped_column(String(100))
    modelo: Mapped[str] = mapped_column(String(100))
    tipo_veiculo: Mapped[str] = mapped_column(String(100))
    tipo_combustivel: Mapped[str] = mapped_column(String(100))
    tem_compatibilidade: Mapped[str] = mapped_column(String(100))
    origem: Mapped[str] = mapped_column(String(100))
    marcas_ids: Mapped[str] = mapped_column(String(128))
    modelos_ids: Mapped[str] = mapped_column(String(128))
    anos_ids: Mapped[str] = mapped_column(String(128))
    technical = composite(TechnicalData, 
        "marca",
        "condicao_produto",
        "gtin",
        "gtin_ausencia_motivo",
        "numero_peca",
        "num_inmetro",
        "cod_oem",
        "modelo",
        "tipo_veiculo",
        "tipo_combustivel",
        "tem_compatibilidade",
        "origem",
        "marcas_ids",
        "modelos_ids",
        "anos_ids",
        deferred=False
    )
    
    altura: Mapped[str] = mapped_column(String(16))
    largura: Mapped[int] = mapped_column(Integer)
    comprimento: Mapped[int] = mapped_column(Integer)
    peso: Mapped[int] = mapped_column(Integer)
    dimensions = composite(DimensionsData, 
        "altura", 
        "largura", 
        "comprimento", 
        "peso",
        deferred=False
    )
    
    produto_status: Mapped[str] = mapped_column(String(32), default="Ainda não publicado") #DEFAULT 'Ainda não publicado'
    produto_atualizado: Mapped[str] = mapped_column(String(1), default="N") #DEFAULT 'N'
    
    @classmethod # Registro de evento após rastreamento
    def __declare_last__(cls):
        """ Cria a sequência após criar a tabela """
        event.listen(
            target=cls.__table__,
            identifier="after_create",
            fn=CreateSequence(cls.id_seq)
        )
