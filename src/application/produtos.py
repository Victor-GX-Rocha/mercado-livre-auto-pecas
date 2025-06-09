""" Operations for Produtos table """

from typing import Protocol

from ..infrastructure.database.models.produtos import Produtos, Product
from ..infrastructure.database.repositories import ProdutosRepository
from .shared.oganizer import GroupBy

class ProdutosProtocol(Protocol):
    """ Protocol for Produtos operations and interfaces """
    def execute(self, lines: list[Product]) -> None:...



class Publication(ProdutosProtocol):
    def execute(self, lines: list[Product]) -> None:...
    
class Edition(ProdutosProtocol):
    def execute(self, lines: list[Product]) -> None:...
    
class Pause(ProdutosProtocol):
    def execute(self, lines: list[Product]) -> None:...
    
class Activation(ProdutosProtocol):
    def execute(self, lines: list[Product]) -> None:...
    
class Deletation(ProdutosProtocol):
    def execute(self, lines: list[Product]) -> None:...
    


class Produtos:
    """ Manager the execution of all Produtos table operations. """
    def __init__(self) -> None:
        self.repo = ProdutosRepository()
        self.publication = Publication()
        self.edition = Edition()
        self.pause = Pause()
        self.activation = Activation()
        self.deletation = Deletation()
    
    def execute(self):
        """  """
        pending_lines: list[Product] = self.repo.get.pending_operations()
        
        if not pending_lines:
            return
        
        user_lines: dict[list[Product]] = GroupBy.column(pending_lines)
        
        for user, lines in user_lines.items():
            ...




