""" Models for atrributes responses. """

from typing import Literal, Optional
from dataclasses import dataclass, field

@dataclass
class AttributeErrorDetail:
    attribute_id: str                       # The generator class name.
    message: str                            # A global friendly message for user.
    severity: Literal["error", "warning"]   # "error" blocks publication.

@dataclass
class AttributeErrorCause:
    causes: list = field(default_factory=list)
    missing_values: list = field(default_factory=list)

@dataclass
class AttributesResponse:
    success: bool
    result: list[dict]
    error: Optional[AttributeErrorCause] = None
    
    # errors: list[AttributeErrorDetail] = field(default_factory=list)
    # warnings: list[AttributeErrorDetail] = field(default_factory=list)

@dataclass
class AttributesValidatorResponse:
    is_valid: bool = False
    causes: list = field(default_factory=list)
    
    # missing_values: Optional[list] = None
