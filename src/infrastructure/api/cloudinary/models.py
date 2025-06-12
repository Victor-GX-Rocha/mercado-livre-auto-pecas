""" Cloudinary dataclasse response models. """

from typing import Any
from dataclasses import dataclass

@dataclass
class CloudinaryUploadImageResponse:
    asset_id: str | None
    public_id: str | None
    version: int | None
    version_id: str | None
    signature: str | None
    width: int | None
    height: int | None
    format: str | None
    resource_type: str | None
    created_at: str | None
    tags: str | None
    bytes: int | None
    type: str | None
    etag: str | None
    placeholder: bool | None
    url: str | None
    secure_url: str | None
    asset_folder: str | None
    display_name: str | None
    original_filename: str | None
    api_key: str | None

@dataclass
class CloudinaryDeleteImageResponse:
    success: bool
    error: Any

@dataclass
class CloudinaryResponse:
    success: bool
    data: Any | None
    error: Any | None = None
