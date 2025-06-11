"""  """

from typing import Protocol, runtime_checkable

from ....infrastructure.api.mercadolivre.auth import AuthResponse
from ....infrastructure.database.models.produtos import Product
from ....infrastructure.database.repositories import ProdutosRepository
from .json_generator import JsonGenerator


runtime_checkable
class ProdutosOperation(Protocol):
    # def __init__(self, repo: ProdutosRepository):
    #     ...
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        ...

class Publication(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository, json_generator: JsonGenerator):
        self.repo = repo
    
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        """
        - [ ] Create the json
        - [ ] Publish
        - [ ] Add a description
        - [ ] Add compatibility
        - [ ] Update the database
        """
        print(f"Executando {self.__class__.__name__}")
        # self.create_json()
        # self.publish()
        # self.add_description()
        # self.add_compatibility()
        ## self.update the database
    
    def create_json(self):...
    def publish(self):...
    def add_description(self):...
    def add_compatibility(self):...


class Edition(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository, json_generator: JsonGenerator):
        self.repo = repo
    
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Pause(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Activation(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

class Deletation(ProdutosOperation):
    def __init__(self, repo: ProdutosRepository):
        self.repo = repo
    
    def execute(self, items: list[Product], token: AuthResponse) -> None:
        print(f"Executando {self.__class__.__name__}")

