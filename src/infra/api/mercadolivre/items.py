""" Items requests. """

from typing import Any

from .client import MLBaseClient
from .models import MeliResponse


class ItemsRequests:
    """ Requests for /items endpoints. """
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
        Add a description to a product on mercado libre.
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
    
    def get_description(self, access_token: str, item_id: str) -> MeliResponse:
        """
        Get a description to a product on mercado libre.
        Args:
            access_token (str): Access token to publish the product.
            item_id (str): Item ID.
            descrption (str): Item descritpion.
        Returns:
            MeliResponse:
        """
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"/items/{item_id}/description",
            context="item_description",
            headers=headers
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
    
    def list_items(self, access_token: str, user_id: str, limit: int = 50, offset: int = 0) -> MeliResponse:
        """
        List the items form a user on mercado libre.
        Args:
            access_token (str): Access token to edit the product.
            user_id (str): User ID.
        Returns:
            MeliResponse:
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"/users/{user_id}/items/search?limit={limit}&offset={offset}",
            context="items_listing",
            headers=headers
        )
        
        return response
    
    def get_items_info(self, access_token: str, items_list: str) -> MeliResponse:
        """
        List the items form a user on mercado libre.
        Args:
            access_token (str): Access token to edit the product.
            items_list (str): A "list" of meli products IDs, turned into str.
        Example:
            >>> items_list: list[str] = ["MLB78248", "MLB869448"]
            >>> items_str_list: str = ",".join(items_list)
            ... "MLB78248,MLB869448"
            >>> get_items_info(access_token, items_list=items_str_list)
            ... MeliResponse(success=True, data=[{"id":...}, {...}]...
        Returns:
            MeliResponse:
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"/items?ids={items_list}",
            context="get_items_info",
            headers=headers
        )
        
        return response
    
    def get_item_info(self, access_token: str, item_id: str) -> MeliResponse:
        """
        Get the data from of a product on mercado libre.
        Args:
            access_token (str): Access token to edit the product.
            item_id (str): Item ID.
        Returns:
            MeliResponse:
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"/items/{item_id}",
            context="get_item_info",
            headers=headers
        )
        
        return response
    
    def add_compatibilities(
        self,
        access_token: str,
        product_id: str,
        items_ids: list[str],
        limit: int = 180
    ) -> MeliResponse:
        """
        Add a list of compatibilities on a product.
        Args:
            access_token (str): 
            product_id (str): 
            items_ids (list[str]): 
            limit (int):
        Returns:
            MeliResponse:
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        products = [{
            "id": item_id, 
            "creation_source": "DEFAULT", 
            "note": "texto", 
            "restrictions": []
        } for item_id in items_ids[:limit]]
        
        payload = {"products": products}
        
        response: MeliResponse = self.client.post(
            endpoint=f"/items/{product_id}/compatibilities",
            context="item_add_compatibilities",
            headers=headers,
            json=payload
        )
        return response
