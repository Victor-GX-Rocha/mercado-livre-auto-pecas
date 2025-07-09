""" Defines the model env objects. """

from dataclasses import dataclass

@dataclass(frozen=True)
class DatabaseConfig:
    hostname: str
    database: str
    password: str
    user: str
    port: int = 5432

@dataclass(frozen=True)
class AppConfig:
    still_on: bool
    timer: int

@dataclass
class ApiBrasilDevices:
    cpf: str
    cnpj: str
    placa: str

@dataclass
class ApiBrasilCredentials:
    email: str
    senha: str
    bearer_token: str
    device: ApiBrasilDevices
