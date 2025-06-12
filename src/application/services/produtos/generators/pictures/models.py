""" Models for Pictures responses. """

from dataclasses import dataclass
from ...models import GeneratorsResponse

@dataclass
class PicturesGeneratorResponse(GeneratorsResponse):...
    # error: Optional[Any] = None
