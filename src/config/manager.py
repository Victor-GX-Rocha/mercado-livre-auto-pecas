""" Environment variable manager """

import sys
from typing import Dict, List, Optional

from ..core import logging
from .exceptions import (
    # EnvFileNotFoundError,
    ConfigValidationError
)
from .validators import (
    EnvValidator,
    FileValidator,
    # EmptyValueValidatorAlert,
    RequiredKeysValidator,
    TypeConversionValidator,
    # RequiredEmptyValueValidator,
    RequiredSystem
)
from .models import (
    AppConfig,
    DatabaseConfig,
    ApiBrasilCredentials,
    ApiBrasilDevices
)


FALLBACK_TIMER: int = 2
DATABASE_REQUIRED_KEYS: list = ["HOSTNAME", "DATABASE", "PASSWORD", "USER"]
IGNORED_KEYS: list = ["STILL_ON"]

class RealTimeEnvManager:
    def __init__(self, env_file: str = '.env') -> None:
        self.env_file = env_file
        
        self._app_validators: list[EnvValidator] = [
            FileValidator(self.env_file),
            # EmptyValueValidatorAlert(["TIMER"]),
            RequiredKeysValidator(["TIMER", "STILL_ON"]),
            TypeConversionValidator("TIMER", int)
        ]
    
    def _read_env_file(self) -> Dict[str, str]:
        try:
            with open(self.env_file, 'r', encoding='utf-8') as file:
                return self._parse_env(file)
        # except FileNotFoundError:
        #     raise EnvFileNotFoundError(f"Arquivo {self.env_file} não encontrado")
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            raise ConfigValidationError("Falha na leitura do ambiente") from e
    
    def _parse_env(self, file) -> Dict[str, str]:
        env_vars: Dict = {}
        for line in file:
            line = line.strip()
            
            if line.startswith('#'): # Ignora linhas de comentário
                continue
            
            if not '=' in line:
                continue
            
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()
        return env_vars
    
    def _validate(self, env_data: Dict[str, str], validators: List) -> None:
        for validator in validators:
            validator.validate(env_data)
    
    def load_app_config(self) -> AppConfig:
        env_data = self._read_env_file()
        self._validate(env_data, self._app_validators)
        
        return AppConfig(
            still_on=bool(env_data.get("STILL_ON", False)),
            timer=int(env_data.get("TIMER", FALLBACK_TIMER))
        )

class AppConfigManager(RealTimeEnvManager):
    def __init__(self) -> None:
        super().__init__()
        self._db_config: Optional[DatabaseConfig] = None
        self.verify_off_command()
    
    def load_database_config(self) -> DatabaseConfig:
        """ Loads and validates the configurations """
        if self._db_config is None: # Cache
            env_data = self._read_env_file()
            RequiredSystem(
                keys=DATABASE_REQUIRED_KEYS,
                ignore_keys=IGNORED_KEYS
            ).validate(env_data)
            
            self._db_config = DatabaseConfig(
                hostname=env_data["HOSTNAME"],
                database=env_data["DATABASE"],
                password=env_data["PASSWORD"],
                user=env_data["USER"],
                port=int(env_data.get("PORT", "5432"))
            )
        
        return self._db_config
    
    @property
    def database_url(self) -> str:
        """ Create connection URL. """
        db = self.load_database_config()
        return f"postgresql+psycopg2://{db.user}:{db.password}@{db.hostname}:{db.port}/{db.database}"
    
    def get_cloud_user_name(self) -> str:
        """ Get the name of cloudinary user.  """
        env_data = self._read_env_file()
        RequiredKeysValidator(["CLOUDINARY_USER"]).validate(env_data)
        return env_data["CLOUDINARY_USER"]
    
    def verify_off_command(self) -> None:
        """ If STILL_ON == False. Auto turn off the program """
        if not self.load_app_config().still_on:
            logging.info(f'Arquivo .env: Comando STILL_ON ordem "desligar".\n\nSe deseja ligar o bot, preencha STILL_ON no arquivo .env -> Ex.: STILL_ON=ON\n')
            sys.exit()

