""" ICatalog domains requests. """

from typing import Any

from src.infra.api.mercadolivre.client import MLBaseClient
from src.infra.api.mercadolivre.models import MeliResponse, MeliErrorDetail

MLB_CARS_AND_VANS: str = "MLB-CARS_AND_VANS"

class CatalogCompatibilitiesRequests:
    def __init__(self):
        self.client = MLBaseClient()
    
    def get_compatibilities(
            self, 
            access_token: str, 
            brand_ids: list[str],
            model_ids: list[str],
            years_ids: list[str],
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
            years_ids (list[str]): Years IDs.
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
                {"id": "MODEL", "value_ids": model_ids},
                {"id": "VEHICLE_YEAR", "value_ids": years_ids}
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
        
        if response.success:
            if int(response.data["total"]) <= 0:
                return MeliResponse(
                    success=False,
                    data=None,
                    error=MeliErrorDetail(
                        message="O mercado livre não encontrou compatibilidades para o seu produto. Dica: Se viável, tente aumentar os filtros, insira mais marcas, modelos ou anos compatíveis.",
                        context="get_compatibilities",
                        code=88,
                        http_status=response.http_status,
                        details="Ao inserir poucas informações de IDs sobre seu produto, é provável que não sejam encontrados muitos veículos de catálogo compatíveis, ou mesmo nenhum. Revise sua publicação. Processo pulado. "
                    )
                )
        
        return response
