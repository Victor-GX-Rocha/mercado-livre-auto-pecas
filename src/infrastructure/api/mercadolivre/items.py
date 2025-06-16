""" Items requests. """

from typing import Any

from .client import MLBaseClient
from .models import MeliResponse


class ItemsRequests:
    def __init__(self):
        self.client = MLBaseClient()
    
    def publish(self, access_token: str, publication_data: dict[str, Any]) -> MeliResponse:
        """
        Publish a product on mercado libre.
        Args:
            access_token (str): Access token to publish the product.
            publication_data (dict[str, Any]):
        Returns:
            MeliResponse:
        """
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response: MeliResponse = self.client.post(
            endpoint="/items",
            context="item_publication",
            headers=headers,
            json=publication_data
        )
        
        return response
    
    def add_description(self, access_token: str, item_id: str, descrption: str) -> MeliResponse:
        """
        Publish a product on mercado libre.
        Args:
            access_token (str): Access token to publish the product.
            item_id (str): Item ID.
            descrption (str): Item descritpion.
        Returns:
            MeliResponse:
        """
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload: dict[str, str] = {
            "plain_text": descrption
        }
        
        response: MeliResponse = self.client.post(
            endpoint=f"/items/{item_id}/description",
            context="item_description",
            headers=headers,
            json=payload
        )
        
        return response
    
    def edit(self, access_token: str, item_id: str, edition_data: dict) -> MeliResponse:
        """
        Edit a published product on mercado libre.
        Args:
            access_token (str): Access token to edit the product.
            item_id (str): Item ID.
            edition_data (dict): Product terms data will be changed.
        Returns:
            MeliResponse:
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response: MeliResponse = self.client.put(
            endpoint=f"/items/{item_id}",
            context="item_editation",
            headers=headers,
            json=edition_data
        )
        
        return response
