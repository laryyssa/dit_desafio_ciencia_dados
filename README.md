# 🚀 Desafio de Engenharia de Dados DIT

Desafio: Extrair dados de uma API de 1 em 1 minuto, criar csv desses dados e adicionar no banco usando a ferramenta Prefect e criar uma visualização de colunas expecíficas dessa tabela usando DBT.


## 📦 **1. Configuração do Projeto**

### 🔑 **1.1 Clonar o Repositório**

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/dit_desafio_eng_dados.git
cd dit_desafio_eng_dados
```

### 🌿 **1.2 Criar Ambiente Virtual**

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 🔐 **1.3 Configurar o Arquivo**

Crie um arquivo `.env` do projeto:

```ini
# url de extração
API_URL = "https://dados.mobilidade.rio/gps/brt"

# prefect
PREFECT_API_KEY = # adicione aqui sua api key que esta nesse link (https://app.prefect.cloud/my/api-keys)
PREFECT_API_URL="http://127.0.0.1:4200/api" # para executar localmente

# banco de dados
POSTGRES_USER="psql"
POSTGRES_PASSWORD="senha"
POSTGRES_DB="psqldb"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5433"

DATABASE_URL = postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

TABLE_NAME= "veiculos"

# prefect configs
DEPLOYMENT_NAME = "desafio_eng_dados"
DOCKER_POOL = "my-docker-pool"
```

###  🚀 **1.4 Subir um banco postgres usando Docker**
```bash
docker-compose up --build
```
## 🚀 **2. Executar o Prefect**
### ✅ 2.1 Iniciar o Servidor Prefect

```bash
prefect server start
```

### 📊 2.2 Rodar o Fluxo de Extração da API

Faça o primeiro comando para abrir o workspace e o segundo para executar o flow.

Execute o fluxo Prefect para extrair dados e gerar o CSV `data_extract.csv`. Os dados serão salvos como arquivos CSV na pasta `data/` e depois inseridos no banco de dados Postrgres na tabela `veiculos`.

```bash
prefect python pipeline/main.py

prefect deployment run 'exctract-data/desafio_eng_dados'
```


## 🚀 **3. Executar o DBT**

### ✅ **3.1 Testar a Conexão**

```bash
# Testar conexão DBT
cd veiculos_dbt
dbt debug
```

### 🏗️ **3.2 Executar o Projeto**
Cria uma view composta de id, latitude e longitude e velocidade do veiculo

```bash
# Rodar os modelos
cd veiculos_dbt
dbt run
```

