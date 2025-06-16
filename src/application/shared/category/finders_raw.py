"""
Operacao = 1 -> pesquisar usando o caminho completo da categoria. E retornar o id da categoria.
Operacao = 2 -> pesquisar por titulo_produto. Retornar o caminho completo da categoria e o id.
Operacao = 3 -> pesquisar por id. Retornar o caminho completo da categoria.
"""

import requests
from requests import RequestException
from typing import Protocol

from core.log import logging


BASE_URL: str = "https://api.mercadolibre.com"
SITE_ID: str = "MLB"

# class CategoryFinderProtocol(Protocol):
#     """ Protocol format for the finder system """
#     def find(self):...

class CategoryLeafFinder:
    ...

class CategoryPathFinder:
    """ Find the path of the category based on his ID """
    
    def run(self, category_id: str, access_token: str) -> str:
        
        path_category: str = self.find_category_path(category_id, access_token)
        
        if not path_category:
            # Adicionar log de erro na tabela.
            ...
        
        # Adicionar log de sucesso na tabela
        
        # Returns the path category
        return path_category
    
    def find_category_path(self, category_id: str, access_token: str) -> str | None:
        errors: list = []
        if not category_id:
            none_type_error: str = f'O ID de categoria não pode ser vazio!'
            logging.warning(none_type_error)
            errors.append(none_type_error)
        
        if type(category_id) != str:
            not_str_error: str = f'O ID de categoria [{category_id}] é inválido pois precisa ser uma str!'
            logging.warning(not_str_error)
            errors.append(not_str_error)
        
        if len(errors) > 0:
            return {
                'success': False,
                'data': None,
                'error': str(errors)
            }
        
        try:
            
            url: str = f"{BASE_URL}/categories/{category_id}"
            payload = {}
            headers = {'Authorization': f'Bearer {access_token}'}
            response: requests.Response = requests.request("GET", url, headers=headers, data=payload)
            
            # print(response.text)
            response.raise_for_status()
            
            
            category_response: dict = response.json()
            ml_path: dict = category_response.get("path_from_root", [])
            # print(ml_path)
            
            if not ml_path:
                print("⚠️ Categoria sem hierarquia definida.")
                # return category_response.get("name")
                return {
                    'success': False,
                    'data': category_response.get("name"),
                    'error': f"Categoria sem hierarquia definida. [{category_response.get("name")}]"
                }
            
            names = [cat["name"] for cat in ml_path]
            category_path = " > ".join(names)
            
            
            # return category_path
            
            return {
                'success': True,
                'data': category_path,
                'error': None
            }
            
        except (RequestException, Exception) as r:
            print(f'Response exception: {r} \n{response.text}')
            return {
                'success': False,
                'data': None,
                'error': {
                    'full_exception': str(r)
                }
            }

class CategoryTitleFinder:
    def __init__(self, path_finder: CategoryPathFinder):
        self.operation_base_url: str = "domain_discovery/search"
        self.path_finder = path_finder
    
    def run(self, title: str, access_token: str):
        return self.title_response(title, access_token)
        # title_response: dict = self.title_response(title)
        
        # if title_response["success"]:
        #     meli_response: dict = title_response["data"]
            
        #     title_id: str = self.get_category_id(meli_response)
        #     title_path: str = self.get_category_path(meli_response)
        
        #     return {"title_id":title_id, "title_path":title_path}
    
    def title_response(self, title: str, access_token: str) -> dict | None:
        """
        Args:
            title (str): Product title.
        Returns:
            The Meli ID founded.
        """
        errors: list = []
        if not title:
            none_type_error: str = f'O titulo passado não pode ser vazio!'
            logging.warning(none_type_error)
            errors.append(none_type_error)
        
        if type(title) != str:
            not_str_error: str = f'O título [{title}] é inválido pois precisa ser uma str!'
            logging.warning(not_str_error)
            errors.append(not_str_error)
        
        if len(errors) > 0:
            return {
                'success': False,
                'data': None,
                'error': str(errors)
            }            
        
        try:
            url: str = f"{BASE_URL}/sites/{SITE_ID}/{self.operation_base_url}?limit=8&q={title}"
            
            payload = {}
            headers = {'Authorization': f'Bearer {access_token}'}
            response: requests.Response = requests.request("GET", url, headers=headers, data=payload)
                        
            response.raise_for_status()
            
            meli_response: dict  = response.json()
            
            if len(meli_response) > 0:
                return {
                    'success': True,
                    'data': response.json(),
                    'error': None
                }
                # return meli_response[0]
            else:
                return {
                    'success': False,
                    'data': {},
                    'error': "Nenhuma categoria condizente com o título foi encontrada"
                }
                # Add a error log here
                # return []
        
        except (RequestException, Exception) as e:
            return {
                'success': False,
                'data': None,
                'error': {
                    'full_exception': str(e)
                    # 'user_message': 'user_message: CategoryTitleFinder.publicar',
                    # 'technical_details': 'technical_details: Produtos.publicar',
                }
            }
    
    def get_category_id(self, meli_response: dict) -> str:
        return meli_response.get('category_id', 'ID não retornado')
    
    # def get_category_path(self, meli_response: dict) -> str:
    #     return self.path_finder.run(meli_response.get('category_id'))["data"]

    
    def get_category_path(self, meli_response: dict, access_token: str) -> str:
        return self.path_finder.run(meli_response.get('category_id'), access_token)["data"]




    # def get_category_path_2(self, category_response: dict) -> str:
    #     # return self.path_finder.run(meli_response.get('category_id'))["data"]
    #     # category_response: dict = response.json()
        
    #     ml_path: dict = category_response.get("path_from_root", [])
    #     # print(ml_path)
        
    #     if not ml_path:
    #         print("⚠️ Categoria sem hierarquia definida.")
    #         # return category_response.get("name")
    #         return {
    #             'success': False,
    #             'data': category_response.get("name"),
    #             'error': f"Categoria sem hierarquia definida. [{category_response.get("name")}]"
    #         }
        
    #     names = [cat["name"] for cat in ml_path]
    #     category_path = " > ".join(names)
        
        
    #     # return category_path
        
    #     return {
    #         'success': True,
    #         'data': category_path,
    #         'error': None
    #     }


class CategoryIDFinder:
    def run(self, hierarquia_str: str, access_token: str) -> dict:
        """ Depois eu mudo isso, foca em entregar logo, lembra, não tenta fazer algo perfeito. """
        
        
        return self.buscar_codigo_categoria(hierarquia_str, access_token)
    
    
    def buscar_codigo_categoria(self, hierarquia_str: str, access_token: str) -> dict:
        try:
            errors: list = []
            if not hierarquia_str:
                none_type_error: str = f'O caminho de categoria não pode ser vazio!'
                logging.warning(none_type_error)
                errors.append(none_type_error)
            
            if type(hierarquia_str) != str:
                not_str_error: str = f'O caminho de categoria [{hierarquia_str}] é inválido pois precisa ser uma str!'
                logging.warning(not_str_error)
                errors.append(not_str_error)
            
            if len(errors) > 0:
                return {
                    'success': False,
                    'data': None,
                    'error': str(errors)
                }
            
            nomes = [n.strip() for n in hierarquia_str.split(">")]
            
            initial_url: str = f"{BASE_URL}/sites/{SITE_ID}/categories"
            payload = {}
            headers = {'Authorization': f'Bearer {access_token}'}
            response: requests.Response = requests.request("GET", initial_url, headers=headers, data=payload)
            
            print(response.text)
            response.raise_for_status()
            
            # categorias = requests.get(f"{BASE_URL}/sites/{SITE_ID}/categories").json()
            categorias = response.json()
            categoria_atual = None
            
            for nivel, nome in enumerate(nomes):
                categoria_atual = self.buscar_categoria_por_nome(nome, categorias)
                
                if not categoria_atual:
                    logging.error(f"Nível '{nome}' não encontrado.")
                    # print(f"[ERRO] Nível '{nome}' não encontrado.")
                    # return None
                    return {
                        'success': False,
                        'data': None,
                        'error': f"Nível '{nome}' não encontrado."
                    }
                
                if nivel < len(nomes) - 1:
                    
                    current_url: str = f"{BASE_URL}/categories/{categoria_atual['id']}"
                    current_response_raw: requests.Response = requests.request("GET", current_url, headers=headers, data=payload)
                    # print(f'\ncurrent_response_raw.text = {current_response_raw.text}')
                    
                    
                    # current_response: list[dict] = current_response_raw.json()#[0] # Pega somente o primeiro índice da lista
                    current_response: dict = current_response_raw.json()
                    # print(f'\n{nivel = }{current_response}')
                    
                    categorias = current_response.get("children_categories", [])
            
            if not categoria_atual:
                return {
                    'success': False,
                    'data': None,
                    'error': str(current_response.text)
                }
            
            if categoria_atual:
                return {
                    'success': True,
                    'data': categoria_atual,#categoria_atual["id"],#categorias[0],#["id"],
                    'error': None
                }
                
            return categoria_atual["id"] if categoria_atual else None
        
        except Exception as e:
            logging.exception('ID finder.busca_codigo_categoria')
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
    
    def buscar_categoria_por_nome(self, nome_categoria: str, categorias: dict[str, str]):
        nome_normalizado: str = nome_categoria.strip().lower()
        for cat in categorias:
            if cat["name"].strip().lower() == nome_normalizado:
                return cat
        return None

class CategoryManager:
    """ Manager and centralize all category operation types """
    def __init__(self):
        self.path_finder = CategoryPathFinder() # Op. 1 
        self.title = CategoryTitleFinder(self.path_finder) # Op. 2
        self.id_finder = CategoryIDFinder() # Op. 3


