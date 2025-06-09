"""  """

from dataclasses import dataclass

@dataclass
class StatusOperationTypes:
    """ Types of state for column operation. """
    PENDING: int = 1
    COMPLETED: int = 2
    IN_PROCESS: int = 0
