""" Program main loop. """

import time

from .core import log
from .config import AppConfigManager
from .app.services import (
    ProdutosApplication, 
    StatusApplication
)

config = AppConfigManager()
database_config = config.load_database_config()

app_produtos = ProdutosApplication()
app_status = StatusApplication()


class MainLoop:
    """ Manages and controls the main program loop. """
    def turn_on(self):
        """ Turns on the loop and keeps it active as long as the STILL_ON variable in the .env file is active. """
        try:
            log.user.info("Iniciando o bot...")
            while True:
                
                app_config = config.load_app_config()
                
                if not app_config.still_on:
                    log.user.info('Arquivo .env: Comando desligar.')
                    break
                
                # Applications
                # app_produtos.execute()
                app_status.execute()
                time.sleep(app_config.timer)
                # break
        except KeyboardInterrupt as k:
            log.user.info(f"Programa desligado manualmente pelo usuário {k}")
        except Exception as e:
            log.dev.exception(f"Exceção inesperada durante a execução do loop principal: {e}")
    
    def turn_off(self):
        """ Turn off the loop. """
        try:
            # Close the database connectation
            # connect_manager.close_all_connections()
            log.user.info('Desligando o bot...\n\n')
        except Exception as e:
            log.dev.exception(f"Exceção inesperada durante a desativação do loop principal: {e}")
