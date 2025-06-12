"""  """

from typing import Any

from .models import (
    CloudinaryUploadImageResponse,
    CloudinaryDeleteImageResponse
)

class CloudinaryResponseConveretrs:
    @staticmethod
    def upload_image(response: dict[str, str | int]) -> CloudinaryUploadImageResponse:
        return CloudinaryUploadImageResponse(
            asset_id=response.get("asset_id"),
            public_id=response.get("public_id"),
            version=response.get("version"),
            version_id=response.get("version_id"),
            signature=response.get("signature"),
            width=response.get("width"),
            height=response.get("height"),
            format=response.get("format"),
            resource_type=response.get("resource_type"),
            created_at=response.get("created_at"),
            tags=response.get("tags"),
            bytes=response.get("bytes"),
            type=response.get("type"),
            etag=response.get("etag"),
            placeholder=response.get("placeholder"),
            url=response.get("url"),
            secure_url=response.get("secure_url"),
            asset_folder=response.get("asset_folder"),
            display_name=response.get("display_name"),
            original_filename=response.get("original_filename"),
            api_key=response.get("api_key"),
        )
    
    @staticmethod
    def delete_image(response: dict[str, str | Any]) -> CloudinaryDeleteImageResponse:
        if response.get("result", "").lower() != "ok":
            return CloudinaryDeleteImageResponse(
                success=False,
                error=response.get("result", "Mensagem de erro não retornada.")
            )
        return CloudinaryDeleteImageResponse(
            success=True,
            error=None
        )

