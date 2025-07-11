
CREATE TABLE produtos (
    -- Identificador único das linhas da tabela.
    id INTEGER PRIMARY KEY,
    
    -- Credenciais de usuário do mercado livre
    client_id VARCHAR(32),
    client_secret VARCHAR(64),
    redirect_uri VARCHAR(256),
    refresh_token VARCHAR(256),
    
    -- Controle de execução
    operacao INTEGER,
    cod_retorno INTEGER,
    log_erro TEXT,
    
    -- Dados de produto ==-º-==
    -- Identificadores primarios do produto
    cod_produto VARCHAR(16),
    sku VARCHAR(64),
    ml_id_produto VARCHAR(32),
    
    -- Identificadores secundarios
    titulo TEXT,
    descricao TEXT,
    link_publicacao TEXT,
    
    -- Dados de status
    produto_status VARCHAR(32) DEFAULT 'Ainda não publicado',
    produto_atualizado character(1) DEFAULT 'N',
    
    -- Dados de venda
    tipo_anuncio VARCHAR(32),
    modo_compra VARCHAR(32),
    termo_garantia VARCHAR(64),
    moeda VARCHAR(4) DEFAULT 'MLB',
    preco numeric(10,2),
    estoque INTEGER,
    imagens VARCHAR(1024),
    
    -- Dados de qualidade
    marca VARCHAR(32),
    condicao_produto VARCHAR(16),
    
    -- Dados de envio
    modo_envio VARCHAR(32),
    logistica VARCHAR(32),
    modo_envio_logistica VARCHAR(32),
    retirada_local boolean,
    frete_gratis boolean,
    
    -- Categoria
    categoria TEXT,
    categoria_id VARCHAR(25),
    categoria_exemplo VARCHAR(1024),
    categoria_caminho VARCHAR(2048),
    
    -- Dados técnicos
    gtin VARCHAR(32),
    gtin_ausencia_motivo VARCHAR(32),
    numero_peca VARCHAR(100),
    num_inmetro VARCHAR(100),
    cod_oem VARCHAR(100),
    modelo VARCHAR(100),
    tipo_veiculo VARCHAR(100),
    tipo_combustivel VARCHAR(100),
    tem_compatibilidade VARCHAR(100),
    origem VARCHAR(100),
    marcas_ids VARCHAR(128),
    modelos_ids VARCHAR(128),
    anos_ids VARCHAR(128),
    
    -- Dados de dimensões
    altura VARCHAR(16),
    largura INTEGER,
    comprimento INTEGER,
    peso INTEGER,
);

ALTER TABLE produtos RENAME COLUMN cod_erro TO cod_retorno;
ALTER TABLE produtos DROP COLUMN status_operacao_id;

---

CREATE TABLE produtos_desativados (
  id INTEGER PRIMARY KEY,
  client_id VARCHAR(32),
  client_secret VARCHAR(64),
  redirect_uri VARCHAR(256),
  refresh_token VARCHAR(256),
  operacao INTEGER,
  cod_erro INTEGER,
  log_erro TEXT,
  ml_id_produto VARCHAR(32),
  status_produto_ml_id INTEGER,
  cod_produto VARCHAR(16),
  sku VARCHAR(16),
  motivo TEXT,
);

CREATE TABLE produtos_status(
  id INTEGER PRIMARY KEY,
  
  -- Credenciais de usuário do mercado livre
  client_id VARCHAR(32),
  client_secret VARCHAR(64),
  redirect_uri VARCHAR(256),
  refresh_token VARCHAR(256),
  
  -- Controle de execução
  operacao INTEGER,
  cod_retorno INTEGER,
  log_erro TEXT,
  
  -- Dados do produto
  status_produto VARCHAR(16),
  mercado_livre_id VARCHAR(16)
);

CREATE TABLE operacao_categoria_ml (
  id INTEGER PRIMARY KEY,
  
  -- Credenciais de usuário do mercado livre
  client_id VARCHAR(32),
  client_secret VARCHAR(64),
  redirect_uri VARCHAR(256),
  refresh_token VARCHAR(256),
  
  -- Controle de execução
  operacao INTEGER,
  cod_retorno INTEGER,
  log_erro TEXT,
  
  -- Sobre o produto
  cod_produto VARCHAR(12),
  atualizado character(1) DEFAULT 'N'::bpchar,
  
  -- Categoria
  categoria_id VARCHAR(20),
  nome_categoria TEXT,
  titulo_produto VARCHAR(60)
);


CREATE TABLE cloudinary (
  id INTEGER PRIMARY KEY,
  usuario VARCHAR(64),
  cloud_name VARCHAR(64),
  api_key VARCHAR(64),
  api_secret VARCHAR(64)
);
