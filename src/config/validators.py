""" Difine the valitarors who will be used on the EnvManager. """

import os
from typing import Protocol, List, Dict

from src.core import log

from .exceptions import (
    MissingConfigVariableError,
    MissingConfigValueError,
    InvalidConfigVariableError,
    EmptyFileError,
    FileValidationError
)


class EnvValidator(Protocol):
    def validate(self, env_data: Dict[str, str]) -> None:
        """Contrato para validadores"""


class RequiredKeysValidator:
    def __init__(self, required_keys: list[str]):
        self.required_keys = required_keys
    
    def validate(self, env_data: Dict[str, str]) -> None:
        missing = [key for key in self.required_keys if key not in env_data]
        if missing:
            log.user.warning(f"Variáveis ausentes: {missing}")
            raise MissingConfigVariableError(f"Variáveis ausentes: {missing}")

class EmptyValueValidatorAlert:
    def __init__(self, ignore_keys: list[str]):
        self.ignore_keys = ignore_keys
        self.ignore_keys.extend(ignore_keys)
        # self.ignore_keys = self.ignore_keys.append('STILL_ON')
    
    def validate(self, env_data: Dict[str, str]) -> None:
        ignore_keys = self.ignore_keys
        # ignore_keys.append('STILL_ON')
        missing: list = [key for key, value in env_data.items() if key not in self.ignore_keys and value == ""]
        if missing:
            print('Chamado')
            log.user.warning(f'Cuidado! Existem valores de variável ausente nas chaves: {missing}')
            # raise MissingConfigValueError(f'Valor de variável ausente nas chaves: {missing}')

class RequiredEmptyValueValidator:
    def __init__(self, required_values_keys: list[str]):
        self.required_values_keys = required_values_keys
    
    def validate(self, env_data: Dict[str, str]) -> None:
        missing: list = [key for key, value in env_data.items() if key in self.required_values_keys and value == ""]
        
        if missing:
            message: str = f'Valor de variável **obrigatório** ausente nas chaves: {missing} \n\nDesligando o programa para fins de correção...'
            log.user.warning(message)
            raise MissingConfigValueError(message)

class RequiredSystem:
    def __init__(self, keys: List[str], ignore_keys: List[str]) -> None:
        """ 
        Args:
            keys (List[str]): Mandatory Keys
            ignore_keys (List[str]): Keys that shuld be ignored
        """
        self.required_values_keys = keys
        self.ignore_keys = ignore_keys 
    
    def validate(self, env_data: Dict[str, str]) -> None:
        
        validators: list[EnvValidator] = [
            RequiredKeysValidator(required_keys=self.required_values_keys),
            EmptyValueValidatorAlert(ignore_keys=self.ignore_keys),
            RequiredEmptyValueValidator(required_values_keys=self.required_values_keys)
        ]
        
        for validator in validators:
            validator.validate(env_data)


class TypeConversionValidator:
    def __init__(self, key: str, expected_type: type):
        self.key = key
        self.expected_type = expected_type
    
    def validate(self, env_data: Dict[str, str]) -> None:
        value = env_data.get(self.key)
        try:
            self.expected_type(value)
        except ValueError:
            message: str = f"{self.key} deve ser {self.expected_type.__name__}"
            log.user.warning(message)
            raise InvalidConfigVariableError(message)

class FileValidator:
    """ Validador de arquivo que pode ser usado diretamente ou via protocolo """
    
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            message: str = f"Arquivo '{file_path}' não encontrado"
            log.user.error(message)
            raise FileNotFoundError(message)
        self.file_path = file_path
    
    def validate(self, _: Dict[str, str] = None) -> None:
        """
        Interface compatível com EnvValidator Protocol.
        O parâmetro env_data é ignorado para validação específica de arquivo
        """
        try:
            if self._is_zero_size():
                raise EmptyFileError(f"Arquivo '{self.file_path}' está vazio")
            elif self._contains_only_whitespace():
                raise EmptyFileError(f"Arquivo '{self.file_path}' contém apenas espaços")
        except PermissionError:
            raise FileValidationError(f"Sem permissão para ler o arquivo '{self.file_path}'")
    
    def _is_zero_size(self) -> bool:
        return os.path.getsize(self.file_path) == 0
    
    def _contains_only_whitespace(self) -> bool:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            while chunk := f.read(4096):
                if any(not c.isspace() for c in chunk):
                    return False
            return True
