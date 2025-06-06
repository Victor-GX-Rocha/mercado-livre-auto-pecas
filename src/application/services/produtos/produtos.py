'''""" Aqui eu primeiro faço tudo e depois se pá eu pego e passo para outros aquivos """

from typing import Protocol, List, Dict

from ....core import logging

class ProdutosProtocol:
    def execute(line: Produto):
        """
        Args:
            line (Produto): Line from a SQLAlquemy database lines list
        """

class Publication(ProdutosProtocol):
    
    def execute(line):
        """  
        What I need to do here? Well:
        
        - Publicate the product
        - Add a description
        - Add compatibilities
        
        
        Publicate the product:
            - Validation some empty information
            - Create an JSON:
                - Find a category
                    - Validate the category
                - Find a product catalog
                - Create attributes
                - Create images IDs
            - Publish
            
        Add a description:
            - Use the publication id to add an description
        Add compatibilities:
            - Get what is necessary to do this
        """
        # self.publish()
        # self.add_desciption()
        # self.add_compatibilities()


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


class Edition(ProdutosProtocol):...
class Pause(ProdutosProtocol):...
class Activation(ProdutosProtocol):...
class Deletation(ProdutosProtocol):...

class ProdutosOperations:
    def __init__(self):#, product_repository: ProductRepository):
        
        # self.cloud = CloudinaryManager(product_repository)
        # self.gerar_imagens = GerarImagens(self.cloud)
        # self.gerar_json = GerarJSON(self.gerar_imagens, product_repository)
        # # self.
        # self.produto = produto
        
        self.publication = Publication()#(product_repository, self.gerar_json)
        self.edition = Edition()#(product_repository, self.gerar_json)
        self.pause = Pause()#(product_repository)
        self.activation = Activation()#(product_repository)
        self.delete = Deletation()#(product_repository)
    
    def execute(self, lines: List[Produto]):
        pass

class ProdutosOperations:
    def __init__(self):
        self.publication = Publication()
        self.edition = Edition()
        self.pause = Pause()
        self.activation = Activation()
        self.delete = Deletation()
    
    def execute(self, lines: List[Produto]):
        grouped_lines: dict[str, list[Produto]] = group.by_user(lines)
        
        for user, lines in grouped_lines.items():
            
            for line in lines:
                
'''