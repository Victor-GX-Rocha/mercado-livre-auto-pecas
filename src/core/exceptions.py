""" General exceptions base """

class AppBaseError(Exception):
    """ Root base for validation errors on the program """
    def __init__(self, message: str):
        super().__init__(message)

class ConfigValidationError(AppBaseError):
    """ Base for enviroment validation errors """
    def __init__(self, message: str = "Erro de configuração do ambiente"):
        super().__init__(message)
