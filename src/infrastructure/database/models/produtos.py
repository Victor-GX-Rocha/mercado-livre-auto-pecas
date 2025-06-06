""" SQLAlchemy entity and dataclasses for table produtos """

from dataclasses import dataclass
from typing import Optional

from .base import MeliCredentials

@dataclass
class Controlers:
    """ Colunas de controle de operação """
    status_operacao_id: int
    operacao: int

@dataclass
class ErrorLoggers:
    """ Colunas de registro de erro """
    cod_erro: int
    log_erro: Optional[str]

@dataclass
class Identifiers:
    """ Identificadores únicos do produto """
    cod_produto: Optional[str]
    sku: Optional[str]
    ml_id_produto: Optional[str]
    link_publicacao: Optional[str]

@dataclass
class SaleData:
    """ Dados de venda """
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
    """ Dados de envio """
    modo_envio: Optional[str]
    logistica: Optional[str]
    modo_envio_logistica: Optional[str]
    retirada_local: Optional[bool]
    frete_gratis: Optional[bool]

@dataclass
class CategoryData:
    """ Categoria """
    categoria: Optional[str]
    categoria_id: Optional[str]
    categoria_exemplo: Optional[str]
    categoria_caminho: Optional[str]

@dataclass
class TecnicalData:
    """ Dados técnicos """
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
    """ Dados de dimensões """
    altura: Optional[str]
    largura: Optional[int]
    comprimento: Optional[int]
    peso: Optional[int]

@dataclass
class Product():
    """ Dataclass para a tabela `produtos` """
    id: int
    credentials: MeliCredentials
    controlers: Controlers
    error_logers: ErrorLoggers
    identfiers: Identifiers
    sale: SaleData
    shippiment: ShippimentData
    category: CategoryData
    technical: TecnicalData
    dimensions: DimensionsData
    produto_status: Optional[str]
    produto_atualizado: Optional[str]


""" SQLAlchemy entity for table produtos """

"""
Let's go, I need to have something in my mind.
I need to know exatly where I wnat to go.
Fot it, I can work by steps. Think, I can in first off all create the columns version of the table.
Next, adapt it for dataclass
And, in last place, organize the things in conjunt models.

I ca testing everery etape.

Andddd, because I alrealy have the models organizated with the same name of the columns table I can alrealy use them.

Ok... Maybe I can do both things.

In the end I really did. Ok, maybe I may do the same at the next try.
"""

from sqlalchemy import event, Integer, String, Text, Boolean, Sequence, Numeric
from sqlalchemy.orm import Mapped, mapped_column, composite#DeclarativeBase, 
from sqlalchemy.schema import CreateSequence

from .base import Base


@dataclass
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
        client_id,
        client_secret,
        redirect_uri,
        refresh_token,
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
    error_logers = composite(ErrorLoggers, cod_erro, log_erro)
    
    cod_produto: Mapped[str] = mapped_column(String(16))
    sku: Mapped[str] = mapped_column(String(64))
    ml_id_produto: Mapped[str] = mapped_column(String(32))
    link_publicacao: Mapped[str] = mapped_column(Text)
    identfiers = composite(Identifiers, 
        cod_produto,
        sku,
        ml_id_produto,
        link_publicacao,
        deferred=False
    )
    
    titulo: Mapped[str] = mapped_column(Text)
    descricao: Mapped[str] = mapped_column(Text)
    imagens: Mapped[list] = mapped_column(String(1024))
    estoque: Mapped[int] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Numeric(10, 2)) #numeric(10, 2)
    moeda: Mapped[str] = mapped_column(String(4), default="MLB") #'MLB'::character varying,
    tipo_anuncio: Mapped[str] = mapped_column(String(32))
    modo_compra: Mapped[str] = mapped_column(String(32))
    termo_garantia: Mapped[str] = mapped_column(String(32))
    sale = composite(SaleData, 
        titulo,
        descricao,
        imagens,
        estoque,
        preco,
        moeda,
        tipo_anuncio,
        modo_compra,
        termo_garantia,
        deferred=False
    )
    
    modo_envio: Mapped[str] = mapped_column(String(32))
    logistica: Mapped[str] = mapped_column(String(32))
    modo_envio_logistica: Mapped[str] = mapped_column(String(32))
    retirada_local: Mapped[bool] = mapped_column(Boolean)
    frete_gratis: Mapped[bool] = mapped_column(Boolean)
    shippiment = composite(ShippimentData, 
        modo_envio,
        logistica,
        modo_envio_logistica,
        retirada_local,
        frete_gratis,
        deferred=False
    )
    
    categoria: Mapped[str] = mapped_column(Text)
    categoria_id: Mapped[str] = mapped_column(String(25))
    categoria_exemplo: Mapped[str] = mapped_column(String(1024))
    categoria_caminho: Mapped[str] = mapped_column(String(2048))
    category = composite(CategoryData, 
        categoria,
        categoria_id,
        categoria_exemplo,
        categoria_caminho,
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
    technical = composite(TecnicalData, 
        marca,
        condicao_produto,
        gtin,
        gtin_ausencia_motivo,
        numero_peca,
        num_inmetro,
        cod_oem,
        modelo,
        tipo_veiculo,
        tipo_combustivel,
        tem_compatibilidade,
        origem,
        deferred=False
    )
    
    altura: Mapped[str] = mapped_column(String(16))
    largura: Mapped[int] = mapped_column(Integer)
    comprimento: Mapped[int] = mapped_column(Integer)
    peso: Mapped[int] = mapped_column(Integer)
    dimensions = composite(DimensionsData, 
        altura, 
        largura, 
        comprimento, 
        peso,
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


# Converter

from typing import List, Dict, Any, Union, Optional, Iterable
from dataclasses import is_dataclass, fields
import inspect

class BaseDataclassConverter:
    """ Base converter for ORM entities to dataclasses with improved patterns """
    
    @staticmethod
    def convert(
        data: Union[object, Dict[str, Any]], 
        target_dataclass: type
    ) -> object:
        """
        Converts a single item to the target dataclass
        
        Args:
            data: Source data (ORM entity or dict)
            target_dataclass: Dataclass type to convert to
            
        Returns:
            Instance of target_dataclass with populated data
        """
        if isinstance(data, dict):
            return BaseDataclassConverter._from_dict(data, target_dataclass)
        elif hasattr(data, '__table__'):  # SQLAlchemy model check
            return BaseDataclassConverter._from_orm(data, target_dataclass)
        else:
            raise TypeError(f"Produtos convert: Unsupported data type: {type(data)}")
    
    @staticmethod
    def convert_many(
        items: Iterable[Union[object, Dict[str, Any]]], 
        target_dataclass: type
    ) -> List[object]:
        """
        Converts multiple items to the target dataclass
        
        Args:
            items: Iterable of source data
            target_dataclass: Dataclass type to convert to
            
        Returns:
            List of converted items
        """
        return [BaseDataclassConverter.convert(item, target_dataclass) for item in items]
    
    @staticmethod
    def _from_dict(data: Dict[str, Any], target_dataclass: type) -> object:
        """Convert from dictionary to dataclass using field mapping"""
        if not is_dataclass(target_dataclass):
            raise TypeError("target_dataclass Deve ser um dataclass")
        
        # Get field names from dataclass
        field_names = {f.name for f in fields(target_dataclass)}
        
        # Filter and map data
        filtered_data = {
            field_name: data[field_name] 
            for field_name in field_names 
            if field_name in data
        }
        
        return target_dataclass(**filtered_data)
    
    @staticmethod
    def _from_orm(orm_obj: object, target_dataclass: type) -> object:
        """Convert from ORM entity to dataclass using attribute mapping"""
        if not is_dataclass(target_dataclass):
            raise TypeError("target_dataclass Deve ser um dataclass")
        
        # Get field names from dataclass
        field_names = {f.name for f in fields(target_dataclass)}
        
        # Collect data from ORM object
        orm_data = {}
        for field_name in field_names:
            # Handle nested dataclasses
            attr = getattr(orm_obj, field_name)
            
            if is_dataclass(attr):
                # Recursive conversion for nested dataclasses
                orm_data[field_name] = BaseDataclassConverter._from_orm(attr, type(attr))
            elif isinstance(attr, list):
                # Handle lists of nested objects
                orm_data[field_name] = [
                    BaseDataclassConverter._from_orm(item, type(item[0])) 
                    for item in attr
                ]
            else:
                orm_data[field_name] = attr
        
        return target_dataclass(**orm_data)


# Implementação específica para Produtos
class ProdutosConverter(BaseDataclassConverter):
    """Converter specialized for Produtos ORM entity to Product dataclass"""
    
    # Mapeamento customizado se necessário
    FIELD_MAPPING = {
        # 'shippiment': 'shipment_data',  # Exemplo de renomeação
        'credentials':'credentials',
        'controlers':'controlers',
        'error_logers':'error_logers',
        'identfiers':'identfiers',
        'sale':'sale',
        'shippiment':'shippiment',
        'category':'category',
        'technical':'technical',
        'dimensions':'dimensions',
        'produto_status':'produto_status',
        'produto_atualizado':'produto_atualizado',
    }
    
    @classmethod
    def convert(
        cls, 
        data: Union[Produtos, Dict[str, Any]], 
        target_dataclass: type = Product
    ) -> Product:
        return super().convert(data, target_dataclass)
    
    @classmethod
    def convert_many(
        cls, 
        items: Iterable[Union[Produtos, Dict[str, Any]]], 
        target_dataclass: type = Product
    ) -> List[Product]:
        return super().convert_many(items, target_dataclass)
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any], target_dataclass: type) -> Product:
        # Aplicar mapeamento customizado
        mapped_data = {
            cls.FIELD_MAPPING.get(k, k): v 
            for k, v in data.items()
        }
        return super()._from_dict(mapped_data, target_dataclass)
    
    @classmethod
    def _from_orm(cls, orm_obj: Produtos, target_dataclass: type) -> Product:
        # Implementação otimizada específica para Produtos
            return Product(
                id=orm_obj.id,
                credentials=MeliCredentials(**orm_obj.credentials),
                controlers=Controlers(**orm_obj.controlers),
                error_logers=ErrorLoggers(**orm_obj.error_logers),
                identfiers=Identifiers(**orm_obj.identfiers),
                sale=SaleData(**orm_obj.sale),
                shippiment=ShippimentData(**orm_obj.shippiment),
                category=CategoryData(**orm_obj.category),
                technical=TecnicalData(**orm_obj.technical),
                dimensions=DimensionsData(**orm_obj.dimensions),
                produto_status=orm_obj.produto_status,
                produto_atualizado=orm_obj.produto_atualizado,
            )
        # return Product(
        #     id=orm_obj.id,
        #     credentials=MeliCredentials(
        #         client_id=orm_obj.client_id,
        #         client_secret=orm_obj.client_secret,
        #         redirect_uri=orm_obj.redirect_uri,
        #         refresh_token=orm_obj.refresh_token
        #     ),
        #     # ... (outros campos) ...
        #     # Campos especiais com tratamento personalizado:
        #     produto_status=orm_obj.produto_status or "Ativo",
        #     produto_atualizado=orm_obj.produto_atualizado == "S"
        # )

# # Uso
# produtos = session.query(Produtos).limit(100).all()

# # Conversão simples
# converted = ProdutosConverter.convert_many(produtos)

# # Conversão de item único
# first_product = ProdutosConverter.convert(produtos[0])