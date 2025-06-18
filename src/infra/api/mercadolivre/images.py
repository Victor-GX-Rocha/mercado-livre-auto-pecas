""" Manager for mercado libre images requests. """

import requests

from .client import MLBaseClient
from .models import MeliResponse, MeliErrorDetail


class MeliImageManager:
    def __init__(self):
        self.client = MLBaseClient()
    
    def get_meli_picture(self, image_url: str, access_token: str) -> MeliResponse:
        """
        Get the meli pictures data.
        Args:
            image_url (str): The image url.
            access_token (str): Access token to get the images IDs.
        """
        try:
            headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}"
            }
            
            try:
                image_data_response: requests.Response = requests.get(image_url)
                image_data_response.raise_for_status()
            except requests.RequestException as e:
                return MeliResponse(
                    success=False,
                    data=None,
                    error=MeliErrorDetail(
                        message=f"Falha durante a requisição para obter os dados da url {image_url}",
                        context="image_upload",
                        code=89,
                        http_status=image_data_response.status_code,
                        exception=str(e)
                    ),
                    http_status=image_data_response.status_code
                )
            
            files = {'file': (image_url.split('/')[-1], image_data_response.content, 'image/jpeg')}
            
            response: MeliResponse = self.client.post(
                endpoint="/pictures",
                context="image_upload",
                headers=headers,
                files=files
            )
            
            return response
        
        except Exception as e:
            return MeliResponse(
                success=False,
                data=None,
                error=MeliErrorDetail(
                    message=f"Falha inesperada durante a processo de geração de um ID de imagem no mercado livre: {image_url = }",
                    context="image_upload",
                    code=89,
                    exception=str(e)
                ),
                # http_status=
            )





