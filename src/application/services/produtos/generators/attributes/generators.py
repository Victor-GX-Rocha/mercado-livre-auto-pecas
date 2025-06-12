""" Attributes generators for a product. """

from typing import Protocol
from abc import abstractmethod

from ......infrastructure.database.models.produtos import Product
from ......infrastructure.api.mercadolivre.auth import AuthResponse

class GeneratorsProtocol(Protocol):
    @abstractmethod
    def create(self, product: Product) -> list[dict]:
        """
        Create 0 or more attributes.
        Args:
            product (Product): Dataclasse produtos table.
        Returns:
            (list[dict]): A list of attributes dictionaries
        """
        pass

class OriginGenerator(GeneratorsProtocol):
    """ Adds the origim of the part. """
    def create(self, product: Product) -> list[dict] | None:
        if origem := product.technical.origem:
            return [{"id": "ORIGIN", "value_name": origem}]
        return []

class CompatibilityGenerator(GeneratorsProtocol):
    def __init__(self):
        self.inserters: list = [
            self.insert_fuel_type,
            self.insert_has_compatibility
        ]
    
    def create(self, product: Product) -> list[dict]:
        attributes = []
        for inserter in self.inserters:
            if data := inserter(product):
                attributes.extend(data)
        return attributes
    
    def insert_fuel_type(self, product: Product) -> list[dict]:
        if tipo_combustivel := product.technical.tipo_combustivel:
            return [{"id": "FUEL_TYPE","value_name": tipo_combustivel}]
        return []
    
    def insert_has_compatibility(self, product: Product) -> list[dict]:
        if tem_compatibilidade := product.technical.tem_compatibilidade:
            return [{"id": "HAS_COMPATIBILITIES", "value_name": tem_compatibilidade}]
        return []
    
    def injection_type(self, product: Product) -> list[dict]:
        """ Coluna temporariamente removida """
        if tipo_injecao := product.technical.tipo_injecao:
            return [{"id": "INJECTION_TYPE", "value_name": tipo_injecao.split(',')}]
        return []

class CodificationGenrator(GeneratorsProtocol):
    def __init__(self):
        self.inserters: list = [
            self._cod_oem,
            self._part_number,
            self._num_inmetro,
            self._gtin
        ]
    
    def create(self, product: Product) -> list[dict]:
        attributes = []
        for inserter in self.inserters:
            if data := inserter(product):
                attributes.extend(data)
        return attributes
    
    def _cod_oem(self, product: Product) -> list[dict]:
        if cod_oem := product.technical.cod_oem:
            return [{"id": "OEM", "value_name": cod_oem}]
        return []
    
    def _part_number(self, product: Product) -> list[dict]:
        if part_number := product.technical.numero_peca:
            return [{"id": "PART_NUMBER", "value_name": part_number}]
        return []
    
    def _num_inmetro(self, product: Product) -> list[dict]:
        if num_inmetro := product.technical.num_inmetro:
            return [{"id": "INMETRO_CERTIFICATION_REGISTRATION_NUMBER", "value_name": num_inmetro}]
        return []
    
    def _gtin(self, product: Product) -> list[dict]:
        if product.technical.gtin == "SEM GTIN":
            return self._getin_less(product)
        return [{"id": "GTIN", "value_name": product.technical.gtin}]
    
    def _getin_less(self, product: Product) -> list[dict]:
        if gtin_ausencia_motivo := product.technical.gtin_ausencia_motivo:
            return [{"id": "EMPTY_GTIN_REASON", "value_name": gtin_ausencia_motivo}]
        return [{"id": "EMPTY_GTIN_REASON", "value_name": "O produto não tem código cadastrado"}]

class NomeationGenerator(GeneratorsProtocol):
    def __init__(self):
        self.inserters: list = [
            self._marca,
            self._modelo,
            self._tipo_veiculo
        ]
    
    def create(self, product: Product) -> list[dict]:
        attributes = []
        for inserter in self.inserters:
            if data := inserter(product):
                attributes.extend(data)
        return attributes
    
    def _marca(self, product: Product) -> list[dict]:
        if marca := product.technical.marca:
            return [{"id": "BRAND", "value_name": marca}]
        return [{"id": "BRAND", "value_name": "Genérico"}]
    
    def _modelo(self, product: Product) -> list[dict]:
        if modelo := product.technical.modelo:
            return [{"id": "MODEL", "value_name": modelo}]
        return [{"id": "MODEL", "value_name": "Peça Automotiva"}]
    
    def _tipo_veiculo(self, product: Product) -> list[dict]:
        if tipo_veiculo := product.technical.tipo_veiculo:
            if tipo_veiculo != "Carro/Caminhonete":
                return [{"id": "VEHICLE_TYPE", "value_name": tipo_veiculo}]
        return []
