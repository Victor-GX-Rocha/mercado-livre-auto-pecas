""" Items requests. """

from typing import Any

from .client import MLBaseClient
from .models import MeliResponse, MeliErrorDetail


class ItemsRequests:
    """ Requests for /items endpoints. """
    def __init__(self):
        self.client = MLBaseClient()
        self.ROOT_ENDPOINT: str = "/items"
    
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
            endpoint=self.ROOT_ENDPOINT,
            context="item_publication",
            headers=headers,
            json=publication_data
        )
        
        return response
    
    def add_description(
        self, 
        access_token: str, 
        item_id: str, 
        descrption: str, 
        change_description: bool = False
    ) -> MeliResponse:
        """
        Add a description to a product on mercado libre.
        Args:
            access_token (str): Access token to publish the product.
            item_id (str): Item ID.
            descrption (str): Item descritpion.
        Returns:
            MeliResponse:
        """
        
        if not "MLB" in item_id:
            return self.__no_item_id(item_id, "item_description")
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload: dict[str, str] = {
            "plain_text": descrption
        }
        
        method: str = "POST" if not change_description else "PUT"
        
        response: MeliResponse = self.client.request(
            method=method,
            endpoint=f"{self.ROOT_ENDPOINT}/{item_id}/description",
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
        
        if not "MLB" in item_id:
            return self.__no_item_id(item_id, "item_description")
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"{self.ROOT_ENDPOINT}/{item_id}/description",
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
        
        if not "MLB" in item_id:
            return self.__no_item_id(item_id, "item_editation")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response: MeliResponse = self.client.put(
            endpoint=f"{self.ROOT_ENDPOINT}/{item_id}",
            context="item_editation",
            headers=headers,
            json=edition_data
        )
        
        return response
    
    def list_items(
        self, 
        access_token: str, 
        user_id: str, 
        limit: int = 50, 
        offset: int = 0
    ) -> MeliResponse:
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
            endpoint=f"/users/{user_id}{self.ROOT_ENDPOINT}/search?limit={limit}&offset={offset}",
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
        
        if not "MLB" in item_id:
            return self.__no_item_id(item_id, "get_item_info")
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"{self.ROOT_ENDPOINT}/{item_id}",
            context="get_item_info",
            headers=headers
        )
        
        return response
    
    def get_category_by_item_name(
        self,
        access_token: str, 
        item_name: str, 
        limit: int = 8, 
        site: str = "MLB"
    ) -> MeliResponse:
        """
        Searches for relevant product categories using Mercado Libre's domain discovery API.
        
        Queries the '/sites/{site}/domain_discovery/search' endpoint to find category suggestions
        based on product name. Useful for determining the appropriate category when listing new items.
        
        Args:
            access_token: Valid access token for API authorization.
            item_name: Product name or search query to find matching categories
            limit: Number of results to return (must be between 1-8 per Mercado Libre restrictions)
            site: Mercado Libre site ID (default "MLB" for Brazil)
        
        Returns:
            MeliResponse: 
                On success:
                    success=True
                    data=[
                        {
                            "category_id": str,   # Mercado Libre category ID
                            "category_name": str, # Human-readable category name
                            "attributes": list    # Required attributes for the category
                        },
                        ... 
                    ]
                On error:
                    success=False
                    error=MeliErrorDetail(
                        message=str,      # Error description
                        context=str,      # Error context
                        status_code=int   # HTTP status code (if available)
                    )
        
        Raises:
            ValueError: If limit is outside 1-8 range
        
        Examples:
            Successful response:
                >>> response = items_requests.get_category_by_item_name("valid_token", "Volante ducato", 2)
                >>> response.data
                [
                    {"category_id": "MLB439438", "category_name": "Volantes", "attributes": [...]},
                    {"category_id": "MLB116012", "category_name": "Acessórios", "attributes": [...]}
                ]
            
            Error response (invalid limit):
                >>> response = items_requests.get_category_by_item_name("token", "Produto", limit=10)
                >>> response.error
                MeliErrorDetail(
                    message="O mercado livre permite apenas um limite entre 1 e 8.",
                    context="get_category_by_item_name",
                    status_code=400
                )
            
        """
        if limit < 1 or limit > 8:
            return MeliResponse(
                success=False,
                error=MeliErrorDetail(
                    message="O mercado livre permite apenas um limite entre 1 e 8.",
                    context="get_category_by_item_name",
                )
            )
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response: MeliResponse = self.client.get(
            endpoint=f"/sites/{site}/domain_discovery/search?q={item_name}&limit={limit}",
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
            access_token (str): Valid access token for API authorization.
            product_id (str): 
            items_ids (list[str]): 
            limit (int): Number of results to insert.
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
            endpoint=f"{self.ROOT_ENDPOINT}/{product_id}/compatibilities",
            context="item_add_compatibilities",
            headers=headers,
            json=payload
        )
        return response
    
    def __no_item_id(self, item_id: str, context: str) -> MeliResponse:
        return MeliResponse(
            success=False,
            error=MeliErrorDetail(
                message=f'Você esqueceu de inserir "MLB" antes do ID do produto. Corrija {item_id} para MLB{item_id}. Processo interrompido para verificação manual. Tenha certeza se é este realmente o produto que quer operar.',
                context=context
            )
        )
