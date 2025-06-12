""" Shared models. """

from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResponse:
    is_valid: bool = False 
    reason: Optional[str] = None
    causes: Optional[list] = None
