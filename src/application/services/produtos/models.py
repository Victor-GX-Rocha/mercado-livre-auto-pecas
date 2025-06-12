""" Shared models. """

from typing import Optional, Any#, Literal
from dataclasses import dataclass#, field

@dataclass
class GeneratorsResponse:
    success: bool
    result: list[dict]
    error: Optional[Any] = None
