
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
from src.infra.api.mercadolivre.category import CategoryRequests
from src.infra.api.mercadolivre.models import MeliResponse
from src.infra.db.models.produtos_category import ProdutosCategoryDataclass
from src.infra.db.repo import ProdutosCategroyRepository
from src.infra.db.repo.models import ResponseCode
from src.app.shared.operations import JustSleep
from src.app.shared.category.finders import IDFinderByPath, CategoryFinderResponse
from src.app.shared.validators import (
    ValidatorsProtocol, 
    EmptyColumnsValidator, 
    EmptyCredentialColumnsValidator, 
    OperationValidator
)



class InvalidValue(Exception):...
class CategoryAPIError(Exception):...
class CategoryNotFound(Exception):...
class EmptyCategoryHierarchyError(Exception):...


class CategoryIDByPath(TableOperationProtocol):
    def __init__(self, log: log, repo: ProdutosCategroyRepository, category_requests: CategoryRequests) -> None:
        self.log = log
        self.repo = repo
        self.category_requests = category_requests
        self.category_finder = IDFinderByPath()
        self.validator = OperationValidator(self.log, self.repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "category.nome_categoria"
            ])
        ]
    
    def execute(self, lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        print(self.__class__.__name__)
        for line in lines:
            try:
                
                if not self.validator.validate(line, self.validators):
                    continue
                
                self.repo.update.executing(id=line.id)
                
                if type(line.category.nome_categoria) != str:
                    raise InvalidValue("A coluna nome_categoria deve conter um texto!")
                
                response: CategoryFinderResponse = self.category_finder.find(
                    category_path=line.category.nome_categoria, 
                    access_token=token.access_token
                )
                
                if not response.success:
                    raise CategoryAPIError(f"{response.error}")
                
                # category_id: str = self.get_category_id(
                #     category_hierarchy=line.category.nome_categoria,
                #     access_token=token.access_token
                # )
                
                self.repo.update.register_category_id(
                    id=line.id,
                    category_id=response.result
                )
                
            except (CategoryAPIError, CategoryNotFound) as e:
                self.__handle_error(id=line.id, message=str(e))
            
            except InvalidValue as e:
                self.__handle_error(id=line.id, message=str(e), return_code=ResponseCode.TABLE_ERROR)
            
            except Exception as e:
                self.__handle_error(id=line.id, message=f"{[self.__class__.__name__]} Erro inesperado: {e}", log=True)
    
    
    def get_category_id(self, category_hierarchy: str, access_token: str) -> str:
        
        hierarchies_names: list[str] = self._get_hierarchies_names(category_hierarchy)
        root_categories: MeliResponse = self.category_requests.get_root_categories(access_token=access_token)
        
        if not root_categories.success:
            raise CategoryAPIError(f"Falha ao obter as categorias raízes: {root_categories.error}")
        
        categories: list[dict[str, str]] = root_categories.data
        
        for level, name in enumerate(hierarchies_names):
            current_category: dict[str, str] = self._filter_category_by_name(category_name=name, categories=categories)
            
            if level >= len(hierarchies_names) - 1:
                break
            
            # current_category_data: dict[str, Any] = current_category_data.data
            current_category_data: dict[str, Any] = self._get_category_data(current_category, access_token, name)
            categories = current_category_data.get("children_categories", [])
        
        return current_category["id"]
    
    def _get_hierarchies_names(self, category_hierarchy: str) -> list[str]:
        hierarchies_names: list[str] = [n.strip() for n in category_hierarchy.split(">")]
        if not hierarchies_names:
            raise InvalidValue(f"Caminho de hierarquia inválido!")
        return hierarchies_names
    
    def _get_category_data(self, current_category: dict[str, str], access_token: str, name: str) -> dict[str, Any]:
        current_category_id: str = current_category.get("id")
        
        current_category_data_response: MeliResponse = self.category_requests.get_category_data(
            category_id=current_category_id, 
            access_token=access_token
        )
        
        if not current_category_data_response.success:
            raise CategoryAPIError(f"Falha ao buscar dados da categoria {current_category_id}: {name}")
        
        return current_category_data_response.data
    
    def _filter_category_by_name(
        self, 
        category_name: str, 
        categories: list[dict[str, str]]
    ) -> dict[str, str] | None:
        """
        
        Args:
            category_name (str): 
            categories (list[dict[str, str]]): 
        """
        normalized_name: str = category_name.strip().lower()
        for cat in categories:
            if cat["name"].strip().lower() == normalized_name:
                return cat
        raise CategoryNotFound(f"Categoria {category_name} descontinuada pelo mercado livre.")
    
    def __handle_error(self, id: int, message: str, log: bool=False, return_code: int =ResponseCode.PROGRAM_ERROR):
        self.log.dev.exception(f"{message}") if log else None
        self.repo.update.log_error(
            id=id, 
            return_code=return_code,
            log_erro=message
        )

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
    def __init__(self, log: log, repo: ProdutosCategroyRepository, category_requests: CategoryRequests) -> None:
        self.log = log
        self.repo = repo
        self.category_requests = category_requests
        self.validator = OperationValidator(self.log, self.repo)
        self.validators: list[ValidatorsProtocol] = [
            EmptyCredentialColumnsValidator(),
            EmptyColumnsValidator([
                "category.categoria_id"
            ])
        ]
    
    def execute(self, lines: list[ProdutosCategoryDataclass], token: AuthResponse) -> None:
        print(self.__class__.__name__)
        for line in lines:
            try:
                
                if not self.validator.validate(line, self.validators):
                    continue
                
                self.repo.update.executing(id=line.id)
                category_path: str = self._get_category_path(line=line, token=token)
                self.repo.update.register_category_path(id=line.id, category_path=category_path)
                
            except (CategoryAPIError, EmptyCategoryHierarchyError) as e:
                self.__handle_error(id=line.id, message=e)
            
            except Exception as e:
                self.__handle_error(id=line.id, message=f"[{self.__class__.__name__}] Excessão inesperada: {e}", log=True)
    
    def _get_category_path(self, line: ProdutosCategoryDataclass, token: AuthResponse) -> str:
        
        response = self.category_requests.get_category_data(
            category_id=line.category.categoria_id,
            access_token=token.access_token
        )
        
        if not response.success:
            raise CategoryAPIError(str(response.error))
        
        category_data: dict[str, Any] = response.data
        path: dict = category_data.get("path_from_root", [])
        
        if not path:
            raise EmptyCategoryHierarchyError("Categoria sem hierarquia definida.")
        
        names: list[str] = [cat["name"] for cat in path]
        category_path: str = " > ".join(names)
        
        return category_path
    
    def __handle_error(self, id: int, message: str, log=False):
        self.log.dev.exception(f"{message}") if log else None
        self.repo.update.log_error(
            id=id, 
            return_code=ResponseCode.PROGRAM_ERROR, 
            log_erro=message
        )
