""" Organize the lines by user_id """

from typing import Dict, List, Protocol
from ...core import logging

# Replace the "Dict" for Product

class GroupingStrategy(Protocol):
    """ Protocol for group strategy """
    def group(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        ...

# 2. Implementações concretas de estratégias de agrupamento
class ClientGrouper:
    """ Group lines by client_id """
    def group(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        grouped = {}
        for item in items:
            client_id = item['client_id']
            if client_id not in grouped:
                grouped[client_id] = []
                # enviar mensagem de alguma forma.
            grouped[client_id].append(item)
        return grouped

class OperationGrouper:
    """ Agrupa produtos por operacao """
    def group(self, items: List[Dict]) -> Dict[int, List[Dict]]:
        grouped = {}
        for item in items:
            operacao = item['operacao']
            if operacao not in grouped:
                grouped[operacao] = []
                # enviar mensagem de alguma forma.
            grouped[operacao].append(item)
        return grouped


# 3. Fachada principal
class ProductOrganizerFacade:
    """Coordena as operações de agrupamento"""
    
    def __init__(
        self,
        client_grouper: GroupingStrategy = ClientGrouper(),
        operation_grouper: GroupingStrategy = OperationGrouper(),
        logger: logging.Logger = None
    ):
        self.client_grouper = client_grouper
        self.operation_grouper = operation_grouper
        self.logger = logger or logging
    
    def organize(self, products: List[Dict]) -> Dict[str, Dict[int, List[Dict]]]:
        """Organiza produtos hierarquicamente por client_id e operacao"""
        try:
            clients = self.client_grouper.group(products)
            return {
                client_id: self.operation_grouper.group(client_products)
                for client_id, client_products in clients.items()
            }
        except Exception as e:
            self._handle_error(f"Erro na organização: {e}")
            return {}
    
    def _handle_error(self, message: str):
        """Centraliza o tratamento de erros"""
        if self.logger:
            self.logger.error(message)
        raise RuntimeError(message)

# 4. Factory simplificada
class OrganizerFactory:
    @staticmethod
    def create_default():
        return ProductOrganizerFacade()
