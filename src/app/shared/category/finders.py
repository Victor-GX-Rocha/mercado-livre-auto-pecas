""" Shared categorie finders functionalities. """

import re
from typing import Protocol, Any
from abc import abstractmethod
from dataclasses import dataclass

from src.infra.api.mercadolivre.category import CategoryRequests

@dataclass
class CategoryFinderResponse:
    success: bool = False
    result: str = None
    error: str = None


class CategoryFinderProtocol(Protocol):
    def find(self, category_term: str) -> CategoryFinderResponse:...


# class CategoryFinderByPath:
class IDFinderByPath:
    def __init__(self):
        self.category_requests = CategoryRequests()
    
    def find(self, category_path: str, access_token: str) -> CategoryFinderResponse: 
        """
        Find a category ID based on his path. 
        Args:
            category_path (str): A category path that must be by ">" or ";".
            access_token (str): Meli access token to get the category data.
        Returns:
            CategoryFinderResponse:
        Example:
            ```python
            category_path = "Acessórios para Veículos > Peças de Carros e Caminhonetes > Peças de Interior > Pedais > Pedais"
            >>> CategoryFinderByPath().find(category_path=category_path, access_token=access_token)
            CategoryFinderResponse(success=True, result='MLB270299', error=None)
            ```
        """
        
        category_names: list[str] = [nome.strip() for nome in re.split(r'[;>]', category_path)]
        categories_response = self.category_requests.get_root_categories(access_token)
        
        if not categories_response.success:
            return CategoryFinderResponse(error=f"Erro ao buscar a categorias raízes: {categories_response.error}")
        
        categories = categories_response.data
        current_category = None
        
        for level, category_name in enumerate(category_names):
            current_category = self._find_category_level_name(category_name, categories)
            
            if not current_category:
                return CategoryFinderResponse(error=f"Nível '{category_name}' não encontrado.")
            
            if level < len(category_names) - 1:
                category_data_response = self.category_requests.get_category_data(current_category["id"], access_token)
                
                if not category_data_response.success:
                    return CategoryFinderResponse(error=category_data_response.error)
                
                category_data: dict[str, Any] = category_data_response.data
                categories = category_data.get("children_categories", [])
        
        if not current_category:
            return CategoryFinderResponse(error=f"Nível '{category_name}' não encontrado.")
        
        return CategoryFinderResponse(success=True, result=current_category["id"])
    
    def _find_category_level_name(self, category_name: str, categories: list[dict[str, str]]) -> dict[str, str] | None:
        """
        Returns a category data if finds it inside the categories list.
        Args:
            category_name (str): The name of the atual category.
            categories (list[dict[str, str]]): The list of categories.
        Returns:
            (dict[str, str]): Returns the category data if it has the same name of the `category_name`. None If not.
        """
        for cat in categories:
            if cat.get("name", "").strip().lower() == category_name.strip().lower():
                return cat
        return None
    
# class ICategoryFinderBy:
#     def __init__(self):
#         self.by_path
#         self.by_title

# self.category_finder.by_path.find()
