""" Category requests. """

from ..client import MLBaseClient
from ..models import MeliResponse
# from ..auth import AuthResponse

class CategoryRequests:
    def __init__(self):
        self.client = MLBaseClient()
    
    def get_root_categories(self, access_token: str, site_id: str = "MLB") -> MeliResponse:
        """
        Get the root list off categories root types.
        Args:
            access_token (str): Access token to get the categories root types.
        """
        headers: dict[str, str] = {"Authorization": f"Bearer {access_token}"}
        
        response: MeliResponse = self.client.get(
            endpoint=f"/sites/{site_id}/categories",
            context="category_root_types",
            headers=headers
        )
        
        return response
    
    def get_category_data(self, category_id: str, access_token: str) -> MeliResponse:
        """
        Get data from a specific category.
        Args:
            category_id (str): The category ID. Ex.: "MLB47113".
            access_token (str): Access token to get the category data.
        """
        headers: dict[str, str] = {"Authorization": f"Bearer {access_token}"}
        
        response: MeliResponse = self.client.get(
            endpoint=f"/categories/{category_id}",
            context="category_data",
            headers=headers
        )
        
        return response
    
    def get_category_attributes(self, category_id: str, access_token: str) -> MeliResponse:
        """
        Get category attributes data.
        Args:
            category_id str: The category ID. Ex.: "MLB47113"
            access_token str: Access token to get the category attributes.
        """
        headers: dict[str, str] = {"Authorization": f"Bearer {access_token}"}
        
        response: MeliResponse = self.client.get(
            endpoint=f"/categories/{category_id}/attributes",
            context="category_attributes",
            headers=headers
        )
        
        return response
