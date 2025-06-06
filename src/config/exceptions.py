# database > env_system > env_exceptions.py

"""
Centralize the .env enviroment errors
"""

# from src.core.exceptions import ConfigValidationError
from ..core.exceptions import ConfigValidationError


class EnvFileNotFoundError(ConfigValidationError):
    """Arquivo .env não encontrado"""

class MissingConfigVariableError(ConfigValidationError):
    """Variável obrigatória ausente"""

class MissingConfigValueError(ConfigValidationError):
    """Valor de variável ausente"""

class InvalidConfigVariableError(ConfigValidationError):
    """Valor inválido para variável"""

class EmptyFileError(ConfigValidationError):
    """Arquivo .env vazio"""

class FileValidationError(ConfigValidationError):
    """Erro genérico"""