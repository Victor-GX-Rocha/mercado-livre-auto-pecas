""" Program main loop """

import time

from .core import logging
from .config import AppConfigManager

config = AppConfigManager()
database_config = config.load_database_config()


class MainLoop:
    """ Manages and controls the main program loop """
    def turn_on(self):
        """ Turns on the loop and keeps it active as long as the STILL_ON variable in the .env file is active """
        try:
            while True:
                
                app_config = config.load_app_config()
                still_on: str = app_config.still_on
                timer: int = app_config.timer
                
                if not still_on:
                    logging.info('Arquivo .env: Comando desligar.')
                    break
                
                # Services
                
                """      
                Aqui vão ficar os diferentes mini sistemas internos do programa tlg. 
                Vou rebatizar eles como services instead of "routines". At this way I can organize then insid an especialized folder.
                
                services.product() # Here I can pass the SQLAlchemy object diretcly
                services.status()
                services.categories()
                """
                
                time.sleep(timer)
        except KeyboardInterrupt as k:
            logging.info(f"Programa desligado manualmente pelo usuário {k}")
        except Exception as e:
            logging.exception(f"Exceção inesperada durante a execução do loop principal: {e}")
    
    def turn_off(self):
        """ Turn off the loop """
        try:
            # Close the database connectation
            # connect_manager.close_all_connections()
            logging.info('Desligando o bot...\n\n')
        except Exception as e:
            logging.exception(f"Exceção inesperada durante a desativação do loop principal: {e}")
