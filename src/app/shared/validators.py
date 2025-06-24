""" Validate the product data. """

import operator
from typing import Protocol, Optional
from dataclasses import dataclass
from abc import abstractmethod

from src.infra.db.repositories.models import DataclassTable

@dataclass
class ValidationResponse:
    is_valid: bool = False 
    reason: Optional[str] = None
    causes: Optional[list] = None

class CommonValidations:
    CREDENTIAL_COLUMNS = [
        "credentials.client_id",
        "credentials.client_secret",
        "credentials.redirect_uri",
        "credentials.refresh_token"
    ]


def get_value(attr_path: str, object: object):
    attr_getter = operator.attrgetter(attr_path)
    return attr_getter(object)

class ValidatorsProtocol(Protocol):
    @abstractmethod
    def validate(self, dataclass_table: DataclassTable) -> ValidationResponse:
        """
        Validate protocol method.
        Args:
            dataclass_table (DataclassTable): Dataclasse table content.
        """
        pass


class EmptyColumnsValidator(ValidatorsProtocol):
    def __init__(self, columns_path_list: list[str]):
        self.columns_path_list = columns_path_list
        self.getters = [operator.attrgetter(path) for path in columns_path_list]
    
    def validate(self, dataclass_table) -> ValidationResponse:
        empty_columns, invalid_paths = [], []
        
        for getter, full_path in zip(self.getters, self.columns_path_list):
            try:
                column_data = getter(dataclass_table)
                if column_data in (None, ""):
                    column_name = full_path.split('.')[-1]
                    empty_columns.append(column_name)
            except AttributeError:
                invalid_paths.append(full_path)
        
        return self._format_messages(empty_columns, invalid_paths)
    
    def _format_messages(self, empty_columns, invalid_paths) -> ValidationResponse:
        messages: list = []
        messages.append(f"Colunas obrigatórias vazias: {empty_columns}") if empty_columns else None
        messages.append(f"Informação técnica: [Caminhos inválidos: {invalid_paths}]") if invalid_paths else None
        # print(messages)
        if messages:
            return ValidationResponse(causes=messages)
        return ValidationResponse(is_valid=True)

class EmptyCredentialColumnsValidator(EmptyColumnsValidator):
    def __init__(self, columns_path_list: list[str] = CommonValidations.CREDENTIAL_COLUMNS):
        self.columns_path_list = columns_path_list
        self.getters = [operator.attrgetter(path) for path in columns_path_list]
    
    def _format_messages(self, empty_columns, invalid_paths) -> ValidationResponse:
        messages: list = []
        messages.append(f"Colunas de credencial vazias!: {empty_columns}") if empty_columns else None
        messages.append(f"Informação técnica: [Caminhos inválidos: {invalid_paths}]") if invalid_paths else None
        if messages:
            return ValidationResponse(causes=messages)
        return ValidationResponse(is_valid=True)


class Validator:
    @staticmethod
    def validate(line: DataclassTable, validators: list[ValidatorsProtocol]) -> ValidationResponse:
        """
        Vaidate if the table line is able to be used.
        Args:
            line (DataclassTable): Dataclass table line.
        Returns:
            ValidationResponse: 
        """
        causes: list = []
        for validator in validators:
            response = validator.validate(line)
            if not response.is_valid:
                causes.append(response.causes)
        if causes:
            return ValidationResponse(causes=causes)
        return ValidationResponse(True)
