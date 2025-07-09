""" Aplications protocols. """

from typing import Protocol

class ApplicationProtocol(Protocol):
    def execute(self) -> None:
        ...
