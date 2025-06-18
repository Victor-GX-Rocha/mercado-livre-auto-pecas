""" ICatalog domains requests. """

from typing import Any

from src.infrastructure.api.mercadolivre.client import MLBaseClient
from src.infrastructure.api.mercadolivre.models import MeliResponse

MLB_CARS_AND_VANS: str = "MLB-CARS_AND_VANS"

class CatalogCompatibilitiesRequests:
    def __init__(self):
        self.client = MLBaseClient()
    
    def get_compatibilities(
            self, 
            access_token: str, 
            brand_ids: list[str],
            model_ids: list[str],
            sort_by: str = "BRAND",
            order: str = "desc",
            domain_id: str = MLB_CARS_AND_VANS,
            site_id: str = "MLB"
        ) ->  MeliResponse:
        """
        Get the compatibilities based on brand and model ids.
        Args:
            access_token (str): Mercado libre access token API.
            brand_ids (list[str]): Brand IDs.
            model_ids (list[str]): Model IDs.
            sort_by (str): Organization attribute.
            order (str): Order to return the data.
            domain_id (str): Domain ID.
            site_id (str): Site ID.
        Returns:
            MeliResponse:
        """
        
        payload: dict[str, Any] = {
            "domain_id": domain_id,
            "site_id": site_id,
            "known_attributes": [
                {"id": "BRAND", "value_ids": brand_ids},
                {"id": "MODEL", "value_ids": model_ids}
            ],
            "sort": {
                "attribute_id": f"{sort_by.upper()}",
                "order": f"{order.lower()}"
            }
        }
        
        headers: dict[str, str] = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response: MeliResponse = self.client.post(
            endpoint="/catalog_compatibilities/products_search/chunks",
            context="get_compatibilities",
            headers=headers,
            json=payload
        )
        
        return response
