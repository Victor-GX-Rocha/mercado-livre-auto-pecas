'''# schemas/routines/operations.py

from typing import Optional, Dict, List
import requests
import time
import os

from core.log import logging
from API.mercado_livre.ml_manager import ProductManager, APIError
from bot.produto import Produto
from bot.product_interface import AuthManager
from bot.gerar_json import GerarJSON, GerarImagens
from API.cloud import CloudinaryManager

from database.repositories import ProductRepository

produto = Produto()
product_manager = ProductManager()

auth = AuthManager()



def registrar_dados(ml_id: str, link: str, cod_produto: str) -> None:
    """
    Registra uma mensagem de erro em um arquivo de texto.

    :param mensagem: A mensagem de erro a ser registrada.
    :param arquivo: O caminho do arquivo onde o erro será registrado (padrão: "logs/error_log.txt").
    """

    # Cria o diretório "logs" se não existir
    if not os.path.exists('retorno'):
        os.makedirs('retorno')
    
    # os.makedirs(os.path.dirname('retorno'), exist_ok=True)

    # Registra o erro no arquivo
    arquivo = f'retorno\\{cod_produto}.ml'
    with open(arquivo, "a", encoding="utf-8") as log_file:
        log_file.write(f"Ml ID: {ml_id}\n")
        log_file.write(f"Link: {link}\n")
        log_file.write("----------" * 4 + "\n")


class Publication:
    def __init__(self, product_repository: ProductRepository, gerar_json: GerarJSON):    
        self.product_repository = product_repository
        self.gerar_json = gerar_json
        self.produto = produto
    
    def run(self, products: List[Dict]):
        token = None
        for product in products:
            
            if not token:
                token = auth.get_refresh_token(product=product)
                if not token.get('success'):
                    self.product_repository.log_error(
                        product_id=product['id'],
                        log_erro= str(token.get('error')),
                    )
                    continue
                else:
                    response_token = token['data']
                    access_token = response_token['access_token']
            
            if not access_token:
                continue
            
            print(f"Access token: {access_token}")
            published_product: dict = self.publish(product, access_token)
            print(f"published_product: {published_product}")
            
            if not published_product:
                continue
            
            
            ml_id_produto: str = published_product.get('id') # product.get('ml_id_produto', '')
            nova_descricao: str = product.get('descricao', 'Nenhuma descrição encontrada no banco de dados...')
            categoria_escolhida: str = published_product.get('categorye')
            
            published_product_id: str = published_product.get('id', 'MLB não retornado')
            published_product_category_id: str = published_product.get('category_id', 'MLB não retornado')
            published_product_permalink: str = published_product.get('permalink', 'Link não encontrado')
            status: str = published_product.get('status')
            product_id: str = product.get('id', '')
            
            
            time.sleep(0.5)
            
            description_data: dict = self.att_description(
                product=product,
                item_id=ml_id_produto, 
                nova_descricao=nova_descricao, 
                access_token=access_token
            )
            
            if not description_data:
                continue
            
            
            registrar_dados(
                ml_id=published_product_id,
                link=published_product_permalink,
                cod_produto=product.get('cod_produto', 'cod_produto não encontrado')
            )
            
            
            self.product_repository.operation_logs.publication_log_success(
                published_product_id=published_product_id, 
                published_product_category_id=published_product_category_id, 
                published_product_permalink=published_product_permalink, 
                product_status=status,
                product_id=product_id
            )
    
    def publish(self, product: dict, access_token: str) -> Optional[Dict]:
        product_name = product.get('titulo')
        product_db_id = product.get('id')
        
        logging.info(f'Iniciando processo de publicação do produto: [DB-ID: {product_db_id}] | {product_name}')
        
        product_json: str = self.gerar_json.build_json(
            product=product, 
            access_token=access_token
        )
        
        
        publication_response: dict = self.produto.publicar(
            json_atual=product_json,
            access_token=access_token,
        )
        
        # Pega erros de requsição:
        if not publication_response.get("success"):
            logging.error(f"[Erro de requisição] publication_response: {publication_response}")
            self.product_repository.log_error(
                product_id=product['id'],
                log_erro=publication_response["error"],
            )
            return None
        
        publication_data: dict = publication_response.get("data")
        
        # Pega erros do mercado livre
        if publication_data.get("error"):
            
            try:
                erro_publication_motive: str = str([c.get("message") for c in publication_data["cause"]])
            except Exception as e:
                erro_publication_motive: str = str(publication_data)
            
            logging.error(f"Erro durante a publicação do produto: {publication_data}")
            self.product_repository.log_error(
                product_id=product['id'],
                log_erro=erro_publication_motive,
            )
            return None
        
        
        logging.info(f'Produto {product_name} publicado com sucesso!')
        return publication_data
    
    def att_description(self, product: dict, ml_id_produto: str, nova_descricao: str, access_token: str):
        
        product_descrption_att: dict = self.produto.atualizar_descricao(
            item_id=ml_id_produto, 
            nova_descricao=nova_descricao, 
            access_token=access_token
        )
        
        print(f"product_descrption_att: {product_descrption_att}")
        
        # Pega erros de requsição:
        if not product_descrption_att.get("success"):
            logging.error(f"[Erro de requisição] product_descrption_att: {product_descrption_att}")
            self.product_repository.log_error(
                product_id=product['id'],
                log_erro=product_descrption_att["error"],
            )
            return None
        
        descrption_data: dict = product_descrption_att.get("data")
        
        # Pega erros do mercado livre
        if descrption_data.get("error"):
            
            try:
                erro_description_motive: str = str([c.get("message") for c in descrption_data["cause"]])
            except Exception as e:
                erro_description_motive: str = str(descrption_data)
            
            logging.error(f'Erro ao atualizar a descrição do produto: ID {product.get('id')} | Titulo: {product.get('titulo')}\n{product_descrption_att}')
            self.product_repository.log_error(
                product_id=product['id'],
                log_erro=erro_description_motive,
            )
            return None
        
        logging.info(f'Descrição atualizada com sucesso!')
        return descrption_data


class Edition:
    """
    Edita todos os produtos com operação = 03.
    """
    def __init__(self, product_repository: ProductRepository, gerar_json: GerarJSON):    
        self.product_repository = product_repository
        self.gerar_json = gerar_json
        self.produto = produto
    
    def run(self, products: list[dict]):
        
        num_products: int = len(products)
        
        token = None
        for product in products:
            
            if not token:
                token = auth.get_refresh_token(product=product)
                if not token.get('success'):
                    self.product_repository.log_error(
                        product_id=product['id'],
                        log_erro= str(token.get('error')),
                    )
                    continue
                else:
                    response_token = token['data']
                    access_token = response_token['access_token']
            
            if not access_token:
                continue
            
            try:
                ml_product_id: str = product.get('ml_id_produto', '')
                product_price: int = product.get('preco', 0)
                product_name: str = product.get('titulo', '')
                cod_produto: str = product.get('cod_produto', '')
                product_id: str = product.get('id', '')
                
                if not ml_product_id:
                    logging.warning(f"O produto não possui ML_ID. Por favor preencha esse campo. Operação pulada.")
                    continue
                
                if product_price < 7:
                    logging.warning(f'O produto possui um valor abaixo do preço mínimo exigido pelo mercado livre. Preço atual: R${product_price}')
                    logging.info(f'Por favor, insira um preço de no mínimo R$8 reais. Operação pulada.')
                
                # Criar o json com dados de edição
                json_edit: str = self.gerar_json.json_to_edit(
                    product=product,
                    access_token=access_token
                )
                
                # Pausar o produto antes de editar (Obrigatório para evitar erros)
                pause_response: requests.Response = self.produto.pausar(
                    item_id=ml_product_id,
                    access_token=access_token
                )
                
                if not pause_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(pause_response.get('error')),
                    )
                    continue
                
                
                # Atualizar descrição
                att_desc_response: requests.Response = self.produto.atualizar_descricao(
                    item_id=ml_product_id,
                    nova_descricao=product.get('descricao', 'Descrição ausente.'),
                    access_token=access_token
                )
                
                if not att_desc_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(att_desc_response.get('error')),
                    )
                    continue
                
                
                # Editar o produto! ==-º-==
                edit_response: dict = self.produto.editar(
                    item_id=ml_product_id,
                    dados_editar=json_edit,
                    access_token=access_token
                )
                
                if not edit_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(edit_response.get('error')),
                    )
                    continue
                
                
                # Reativar o produto.
                activate_response: dict = self.produto.ativar(
                    item_id=ml_product_id,
                    access_token=access_token
                )
                
                if not activate_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(activate_response.get('error')),
                    )
                    continue
                
                
                # Atualizar o banco de dados com a mensagem de sucesso.
                self.product_repository.operation_logs.generic_sucess(
                    product_id=product_id
                )
                
                logging.info(f'Produto [DB-ID {product_id}] {product_name} editado com sucesso!')
                
            except Exception as e:
                logging.error(f"Erro inesperado ao editar produto [{__class__.__name__}] {product_id}: {e}")
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'log_erro'),
                    where_columns=('id', ),
                    params=(str(e), product_id)
                )

class Pause:
    """
    Pausa um produto.
    """
    def __init__(self, product_repository: ProductRepository):    
        self.product_repository = product_repository
        self.produto = produto
    
    def run(self, products: list[dict]):
        token = None
        for product in products:
            
            if not token:
                token = auth.get_refresh_token(product=product)
                if not token.get('success'):
                    self.product_repository.log_error(
                        product_id=product['id'],
                        log_erro= str(token.get('error')),
                    )
                    continue
                else:
                    response_token = token['data']
                    access_token = response_token['access_token']
                    # print(response_token)
                    # print(access_token)
            
            if not access_token:
                continue
            
            try:
                
                ml_product_id: str = product.get('ml_id_produto', '')
                product_id: str = product.get('id', '')
                product_name: str = product.get('titulo', '')
                
                # Pausar o produto 
                pause_response: requests.Response = self.produto.pausar(
                    item_id=ml_product_id,
                    access_token=access_token
                )
                
                if not pause_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro=str(pause_response.get('error')),
                    )
                    continue
                
                
                product_status: str = pause_response.get('data', {}).get('status')
                
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'produto_status'),
                    where_columns=('id', ),
                    params=(
                        2, product_status, # Set columns
                        product_id # where
                    )
                )
                
                logging.info(f'Produto [DB-ID {product_id}] {product_name} pausado com sucesso!')
                
            except Exception as e:
                logging.error(f"Erro inesperado ao pausar produto [{__class__.__name__}] {product_id}: {e}")
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'log_erro'),
                    where_columns=('id', ),
                    params=(2, str(e), product_id)
                )

class Activation:
    """
    Pausa um produto.
    """
    def __init__(self, product_repository: ProductRepository):    
        self.product_repository = product_repository
        self.produto = produto
    
    def run(self, products: list[dict]):
        token = None
        for product in products:
            
            if not token:
                token = auth.get_refresh_token(product=product)
                if not token.get('success'):
                    self.product_repository.log_error(
                        product_id=product['id'],
                        log_erro= str(token.get('error')),
                    )
                    continue
                else:
                    response_token = token['data']
                    access_token = response_token['access_token']
            
            if not access_token:
                continue
            
            try:
                
                ml_product_id: str = product.get('ml_id_produto', '')
                product_id: str = product.get('id', '')
                product_name: str = product.get('titulo', '')
                
                # Pausar o produto 
                activate_response: requests.Response = self.produto.ativar(
                    item_id=ml_product_id,
                    access_token=access_token
                )
                
                if not activate_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(activate_response.get('error')),
                    )
                    continue
                
                
                product_status: str = activate_response.get('data', {}).get('status')
                
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'produto_status'),
                    where_columns=('id', ),
                    params=(
                        2, product_status, # Set columns
                        product_id # where
                    )
                )
                
                logging.info(f'Produto [DB-ID {product_id}] {product_name} ativado com sucesso!')
                
            except Exception as e:
                logging.error(f"Erro inesperado ao pausar produto [{__class__.__name__}] {product_id}: {e}")
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'log_erro'),
                    where_columns=('id', ),
                    params=(str(e), product_id)
                )

class Delete:
    """
    Deleta um produto.
    """
    def __init__(self, product_repository: ProductRepository):    
        self.product_repository = product_repository
        self.produto = produto
    
    def run(self, products: list[dict]):
        token = None
        for product in products:
            
            if not token:
                token = auth.get_refresh_token(product=product)
                if not token.get('success'):
                    self.product_repository.log_error(
                        product_id=product['id'],
                        log_erro= str(token.get('error')),
                    )
                    continue
                else:
                    response_token = token['data']
                    access_token = response_token['access_token']
            
            if not access_token:
                continue
            
            try:
                
                ml_product_id: str = product.get('ml_id_produto', '')
                product_id: str = product.get('id', '')
                product_name: str = product.get('titulo', '')
                
                # Pausar o produto 
                delete_response: requests.Response = self.produto.deletar(
                    item_id=ml_product_id,
                    access_token=access_token
                )
                
                if not delete_response.get('success'):
                    self.product_repository.log_error(
                        product_id=product.get('id'),
                        log_erro= str(delete_response.get('error')),
                    )
                    continue
                
                
                product_status: str = delete_response.get('data', {}).get('status')
                
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'produto_status'),
                    where_columns=('id', ),
                    params=(
                        2, product_status, # Set columns
                        product_id # where
                    )
                )
                
                logging.info(f'Produto [DB-ID {product_id}] {product_name} deletado com sucesso!')
                
            except Exception as e:
                logging.error(f"Erro inesperado ao pausar produto [{__class__.__name__}] {product_id}: {e}")
                self.product_repository.execute_upload_command(
                    set_columns=('status_operacao_id', 'log_erro'),
                    where_columns=('id', ),
                    params=(str(e), product_id)
                )


class Operations:
    def __init__(self, product_repository: ProductRepository):
        
        self.cloud = CloudinaryManager(product_repository)
        self.gerar_imagens = GerarImagens(self.cloud)
        self.gerar_json = GerarJSON(self.gerar_imagens, product_repository)
        # self.
        self.produto = produto
        
        self.publication = Publication(product_repository, self.gerar_json)
        self.edition = Edition(product_repository, self.gerar_json)
        self.pause = Pause(product_repository)
        self.activation = Activation(product_repository)
        self.delete = Delete(product_repository)
        # self.category_validation = CategoryValidation(product_repository)
    
    # Dicionário principal[Inteiro da operação:[Lista de operações[Cada operação é um dicionário]]]
    def run(self, products: dict):
        # if not products:
        #     return
        
        if products.get(1):
            self.publication.run(products.get(1))
        if products.get(3):
            self.edition.run(products.get(3))
        if products.get(4):
            self.pause.run(products.get(4))
        if products.get(5):
            self.activation.run(products.get(5))
        if products.get(6):
            self.delete.run(products.get(6))
        # if products.get(7):
        #     self.category_validation.run(products.get(7))



'''