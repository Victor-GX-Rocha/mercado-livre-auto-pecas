""" Models for Pictures responses. """

from typing import Optional, Any
from dataclasses import dataclass

# from ..models import GeneratorsResponse

@dataclass
class PicturesGeneratorResponse:
    success: bool
    result: list | Any | None
    error: Optional[Any] = None
