""" Category response models. """

from typing import Any
from dataclasses import dataclass

@dataclass
class CategoryAttributesResponse:
    success: bool
    data: list[dict[str, Any]]
