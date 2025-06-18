""" ICatalog domains requests. """

from typing import Any

from src.infrastructure.api.mercadolivre.client import MLBaseClient
from src.infrastructure.api.mercadolivre.models import MeliResponse

MLB_CARS_AND_VANS: str = "MLB-CARS_AND_VANS"


class CatalogDomainsRequests:
    def __init__(self):
        self.client = MLBaseClient()
    
    def get_models(
            self, 
            access_token: str, 
            known_attributes: list[dict[str, str]], 
            domain_id: str = MLB_CARS_AND_VANS
        ) ->  MeliResponse:
        """
        Get the models from a attribute.
        Args:
            access_token (str): Access token to make the request.
            known_attributes (list[dict[str, str]): List of model attributes.
            domain_id (str): Domain ID.
        Returns:
            MeliResponse:
        Example:
            ```python
            known_attributes: list = [{
                "id": "BRAND",
                "value_id": "67781" # Fiat
            }]
            
            get_models_by_brand(
                access_token=access_token,
                known_attributes=known_attributes
            )
            
            >>> MeliResponse(success=True, data=[{'id': '275412', 'name': 'Mobi', 'metric': 44116}... error=None, http_status=200)
            ```
        """
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload: dict = {
            "known_attributes": known_attributes
        }
        
        response: MeliResponse = self.client.post(
            endpoint=f"/catalog_domains/{domain_id}/attributes/MODEL/top_values",
            context="get_models_by_brand",
            headers=headers,
            json=payload
        )
        
        return response
    
    def get_models_by_brand(
            self,
            access_token: str,
            brand_id: str,
            domain_id: str = MLB_CARS_AND_VANS
        ) -> MeliResponse:
        """
        Get the models by a brand ID.
        Args:
            access_token (str): Access token to make the request.
            brand_id (list[dict[str, str]): List of model attributes.
            domain_id (str): Domain ID.
        Returns:
            MeliResponse:
        """
        known_attributes = [{
            "id": "BRAND",
            "value_id": f"{brand_id}"
        }]
        
        return self.get_models(
            self, 
            access_token=access_token, 
            known_attributes=known_attributes, 
            domain_id=domain_id
        )
