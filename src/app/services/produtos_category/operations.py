
"""
Operacao = 1 -> pesquisar usando o caminho completo da categoria. E retornar o id da categoria.
Operacao = 2 -> pesquisar por titulo_produto. Retornar o caminho completo da categoria e o id.
Operacao = 3 -> pesquisar por id. Retornar o caminho completo da categoria.
"""
from typing import Any

from src.core import log
from src.app.shared.operations import TableOperationProtocol
from src.app.shared.token_manager import MeliTokenManager
from src.infra.api.mercadolivre.auth import AuthResponse
from src.infra.api.mercadolivre.items import ItemsRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.db.models.produtos_category import ProdutosCategoryDataclass
from src.infra.db.repo import ProdutosCategroyRepository
from src.infra.db.repo.models import ResponseCode
from src.app.shared.validators import (
    ValidatorsProtocol, 
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator, 
    OperationValidator
)

from src.app.shared.operations import JustSleep


class CategoryIDByPath(TableOperationProtocol):
    def __init__(self, log: log, repo: ProdutosCategroyRepository) -> None:
        self.log = log
        self.repo = repo
    
    def execute(self, lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        print(self.__class__.__name__)
        for line in lines:
            JustSleep(self.repo).execute()


class CategoryIDByTitle(TableOperationProtocol):
    def __init__(self, log: log, repo: ProdutosCategroyRepository, items_requests: ItemsRequests) -> None:
        self.log = log
        self.repo = repo
        self.items_requests = items_requests
        self.validator = OperationValidator(self.log, self.repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "category.titulo_produto"
            ])
        ]
    
    def execute(self, lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        print(self.__class__.__name__)
        for line in lines:
            try:
                
                if not self.validator.validate(line, self.validators):
                    continue
                
                categories_response: MeliResponse = self.items_requests.get_category_by_item_name(
                    access_token=token.access_token,
                    item_name=line.category.titulo_produto
                )
                
                print(f"{categories_response = }")
                
                if not categories_response.success: # Talvez substituir o uso desse not por um raise
                    self.repo.update.log_error( # E se eu adicionar um raise for status no meli response?
                        id=line.id, 
                        return_code=ResponseCode.PROGRAM_ERROR, 
                        log_erro=categories_response.error
                    )
                    continue
                
                self._register_results(line, categories_response.data)
                
            except Exception as e:
                self.log.dev.exception(f"Erro inesperado: {e} ")
                self.repo.update.log_error(
                    id=line.id, 
                    return_code=ResponseCode.PROGRAM_ERROR,
                    log_erro=f"Faha inesperada: {e}"
                )
    
    def _register_results(self, line: ProdutosCategroyRepository, categories_response: list[dict[str, Any]]) -> None:
        """
        
        Args:
            line (ProdutosCategroyRepository):
            categories_response (list[dict[str, Any]]): Categories content.
        """
        for index, category in enumerate(categories_response):
            category_id: str = category.get("category_id")
            
            if index == 0:
                self.repo.update.register_single_result(
                    id=line.id,
                    category_id=category_id
                )
                if line.controllers.operacao == 2:
                    return
            
            self.repo.insert.add_new_result(
                cod_produto=line.cod_produto,
                category_id=category_id
            )




class PathByCategoryID(TableOperationProtocol):
    def __init__(self, log: log, repo: ProdutosCategroyRepository) -> None:
        self.log = log
        self.repo = repo
    
    def execute(self, lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        print(self.__class__.__name__)
        for line in lines:
            JustSleep(self.repo).execute()



# from category_system import CategoryManager
# from schemas.repositories.category_ml_table import CategoryMlTable
# from API.mercado_livre.ml_manager import APIError, AuthManager

# from typing import List, Dict, Any
# from core.log import logging

# auth = AuthManager()

# class Operation_1:
#     """ Operacao = 1 -> pesquisar usando o caminho completo da categoria. E retornar o id da categoria. """
#     def __init__(self, category_manager: CategoryManager, category_repository: CategoryMlTable):
#         self.category_manager = category_manager
#         self.category_repository = category_repository
#         self.auth = auth
    
#     def run(self, lines):
#         for line in lines:
#             # get token
#             if not all(
#                 [
#                     line["client_id"],
#                     line["client_secret"],
#                     line["redirect_uri"],
#                     line["refresh_token"]
#                 ]
#             ):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     cod_erro=91,
#                     log_erro='Informações de credencial de usuário ausentes!!',
#                 )
#                 continue
            
#             token = self.auth.get_refresh_token(
#                 client_id=line["client_id"],
#                 client_secret=line["client_secret"],
#                 redirect_uri=line["redirect_uri"],
#                 refresh_token=line["refresh_token"]
#             )
            
#             if not token.get('success'):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     log_erro=str(token.get('error')),
#                 )
#                 continue
#             else:
#                 response_token = token['data']
#                 access_token = response_token['access_token']
                
#                 print(response_token)
#                 print(access_token)
            
#             if not access_token:
#                 logging.warning('[Operation_1.run] Access token não obtido!')
#                 continue
            
            
            
            
            
#             category_path: str = line["nome_categoria"]
            
#             category_id_response: dict = self.category_manager.id_finder.run(category_path, access_token=access_token)
            
#             if not category_id_response["success"]:
#                 self.category_repository.log_error(
#                     line_id=line["id"],
#                     log_erro=category_id_response["error"],
#                     cod_erro=88
#                 )
#                 continue
            
#             category_data: dict = category_id_response["data"]
#             category_id = category_data.get("id")
            
            
#             self.category_repository.category_table_log_success(
#                 line_id=line["id"],
#                 category_id=category_id,
#                 category_name=category_path
#             )
    
#     def find_id(self, category_path: str):
#         category_id: str = self.category_manager.id_finder.run(category_path)
        
#         if not category_id:
#             return None

# # category_repository.category_table_log_success(
# #     line_id=1,
# #     category_id='MLBxxxx',
# #     category_name='Acessórios para Veículos > Peças de Carros e Caminhonetes > Motor > Turbinas'
# # )


# class Operation_2:
#     """ Operacao = 2 -> pesquisar por titulo_produto. Retornar o caminho completo da categoria e o id. """
#     def __init__(self, category_manager: CategoryManager, category_repository: CategoryMlTable):
#         self.category_manager = category_manager
#         self.category_repository = category_repository
#         self.auth = auth
    
#     def run(self, lines):
#         for line in lines:
            
#             if not all(
#                 [
#                     line["client_id"],
#                     line["client_secret"],
#                     line["redirect_uri"],
#                     line["refresh_token"]
#                 ]
#             ):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     cod_erro=91,
#                     log_erro='Informações de credencial de usuário ausentes!!',
#                 )
#                 continue
            
#             token = self.auth.get_refresh_token(
#                 client_id=line["client_id"],
#                 client_secret=line["client_secret"],
#                 redirect_uri=line["redirect_uri"],
#                 refresh_token=line["refresh_token"]
#             )
            
#             if not token.get('success'):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     log_erro=str(token.get('error'))
#                 )
#                 continue
#             else:
#                 response_token = token['data']
#                 access_token = response_token['access_token']
                
#                 print(response_token)
#                 print(access_token)
            
#             if not access_token:
#                 logging.warning('[Operation_2.run] Access token não obtido!')
#                 continue
            
#             print(line)
#             title_response: dict = self.category_manager.title.run(line["titulo_produto"], access_token)
            
#             print(f"\n\ntitle response: {title_response} \n\n")
            
#             if not title_response["success"]:
#                 self.category_repository.log_error(
#                     line_id=line["id"],
#                     log_erro=title_response["error"],
#                     cod_erro=88
#                 )
#                 continue
            
#             if type(title_response["data"]) != list:
#                 logging.info('Resultado retornado pela busca por título não é uma lista')
#                 continue
            
#             meli_responses: list[dict] = title_response["data"]
#             # meli_response: dict = title_response["data"][0]
#             meli_response: dict = meli_responses[0]
            
#             if line["operacao"] == 2:
#                 print(meli_response)
#                 self.register_single_response(
#                     line=line,
#                     meli_response=meli_response,
#                     access_token=access_token
#                 )
            
#             elif line["operacao"] == 21:
#                 print(meli_responses)
#                 self.register_multiple_response(
#                     line=line,
#                     meli_responses=meli_responses,
#                     access_token=access_token
#                 )
    
#     def register_single_response(self, line: Dict[str, Any], meli_response: Dict, access_token: str):
#         """ Só preecnhe 1 """
        
#         category_path = self.category_manager.title.get_category_path(meli_response, access_token)
#         category_id = self.category_manager.title.get_category_id(meli_response)
        
#         # print(category_path, category_id)
        
#         logging.info(f"[DB-ID: {line['id']}] Registrando busca de categoria. {category_path=} {category_id=} ")
        
#         self.category_repository.category_table_log_success(
#             line_id=line["id"],
#             category_id=category_id,
#             category_name=category_path
#         )
    
#     def register_multiple_response(self, line: Dict[str, Any], meli_responses: List[Dict], access_token: str):
#         """ Mais de um """
        
#         for index, meli_response in enumerate(meli_responses):
            
#             category_path = self.category_manager.title.get_category_path(meli_response, access_token)
#             category_id = self.category_manager.title.get_category_id(meli_response)
            
#             print(category_path, category_id)
#             logging.info(f"[DB-ID: {line['id']}] Registrando busca multipla de categoria. {category_path=} {category_id=} ")
            
            
#             if index == 0:
#                 self.category_repository.category_table_log_success(
#                     line_id=line["id"],
#                     category_id=category_id,
#                     category_name=category_path
#                 )
#                 continue
            
#             self.category_repository.insert_log_success(
#                 categoria_id=category_id,
#                 nome_categoria=category_path,
#                 titulo_produto=line["titulo_produto"]
#             )


# class Operation_3:
#     """ Operacao = 3 -> pesquisar por id. Retornar o caminho completo da categoria. """
#     def __init__(self, category_manager: CategoryManager, category_repository: CategoryMlTable):
#         self.category_manager = category_manager
#         self.category_repository = category_repository
#         self.auth = auth
    
#     def run(self, lines):
#         for line in lines:
#             # Pegar token
#             if not all(
#                 [
#                     line["client_id"],
#                     line["client_secret"],
#                     line["redirect_uri"],
#                     line["refresh_token"]
#                 ]
#             ):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     cod_erro=91,
#                     log_erro='Informações de credencial de usuário ausentes!!',
#                 )
#                 continue
            
#             token = self.auth.get_refresh_token(
#                 client_id=line["client_id"],
#                 client_secret=line["client_secret"],
#                 redirect_uri=line["redirect_uri"],
#                 refresh_token=line["refresh_token"]
#             )
            
#             if not token.get('success'):
#                 self.category_repository.log_error(
#                     line_id=line['id'],
#                     log_erro=str(token.get('error')),
#                 )
#                 continue
#             else:
#                 response_token = token['data']
#                 access_token = response_token['access_token']
                
#                 print(response_token)
#                 print(access_token)
            
#             if not access_token:
#                 logging.warning('[Operation_2.run] Access token não obtido!')
#                 continue
            
            
            
#             title_response: dict = self.category_manager.title.run(line["titulo_produto"], access_token)
            
#             if not title_response["success"]:
#                 self.category_repository.log_error(
#                     line_id=line["id"],
#                     log_erro=title_response["error"],
#                     cod_erro=88
#                 )
#                 continue
            
#             if type(title_response["data"]) != list:
#                 logging.info('Resultado retornado pela busca por título não é uma lista')
#                 continue
            
            
            
            
            
            
            
#             category_id: str = line["categoria_id"]
#             path_finder_response = self.category_manager.path_finder.run(category_id, access_token=access_token)
            
#             if not path_finder_response["success"]:
#                 self.category_repository.log_error(
#                     line_id=line["id"],
#                     log_erro=path_finder_response["error"]
#                 )
#                 continue
            
#             category_path: str = str(path_finder_response["data"])
            
#             self.category_repository.category_table_log_success(
#                 line_id=line["id"],
#                 category_id=category_id,
#                 category_name=category_path
#             )


# class CategoryRoutines:
#     """ Manager and centralize all category operation types """
#     def __init__(self, category_repository: CategoryMlTable):#commands_interface: ):
#         self.category_manager = CategoryManager()
#         self.operation_1 = Operation_1(self.category_manager, category_repository)
#         self.operation_2 = Operation_2(self.category_manager, category_repository)
#         self.operation_3 = Operation_3(self.category_manager, category_repository)
        
    
#     def run(self, lines: dict):
#         if lines.get(1):
#             self.operation_1.run(lines.get(1))
#         if lines.get(2):
#             self.operation_2.run(lines.get(2))
#         if lines.get(21):
#             self.operation_2.run(lines.get(21))
#         # if lines.get(2) or lines.get(21):
#             # try:
#             #     op_2 = {}
#             #     op_2.update(lines.get(2))
#             #     op_2.update(lines.get(21))
#             #     print(f"{op_2}")
#             # except Exception as e:
#             #     logging.exception(e)
#         if lines.get(3):
#             self.operation_3.run(lines.get(3))
