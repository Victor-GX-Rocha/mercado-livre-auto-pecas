""" Models for produto services. """

from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class GeneratorsResponse:
    success: bool
    result: list[dict]
    error: Optional[Any] = None

@dataclass
class JsonGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None

@dataclass
class ShippimentGeneratorResponse:
    success: bool
    result: Optional[dict[str, Any]]
    error: Optional[Any] = None
