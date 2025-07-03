# Projeto FIVE - API de Notas Fiscais

Este projeto é uma API desenvolvida com *FastAPI* para gerenciamento de notas fiscais, utilizando *MySQL* como banco de dados e *Alembic* para controle de versões do banco de dados.

---

## ⚙ Setup do Ambiente

### 1. Clonando o Repositório

bash
git clone https://github.com/luizinfected/five.git
cd five


---

### 2. Criando e Ativando o Ambiente Virtual

#### 💻 macOS / Linux

bash
python3 -m venv venv
source venv/bin/activate


#### 🪟 Windows

bash
python -m venv venv
venv\Scripts\activate


---

### 3. Instalando as Dependências

bash
pip install --upgrade pip
pip install -r requirements.txt


---

## ▶ Iniciando o Projeto

bash
fastapi dev main.py


---

## 🔌 Configuração do Banco de Dados

### String de conexão de exemplo:

env
MYSQL_CONNECTION_STR='mysql+pymysql://root@127.0.0.1:3306/db_project1'
SECRET_KEY='gGQqvE8CFCBLQhMv0nvWu6AhdCXV0n2wXBEi3mW1AcO5PfdKzvfdCV_Ko8aRFLipgLd9B43UJjC4anx9pdVP0Q'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
IS_DEV=True


---

## 🧬 Alembic - Comandos Úteis

### 📌 Criar nova migração

bash
alembic revision --autogenerate -m "mensagem"


### 📈 Aplicar migração específica

bash
alembic upgrade xxx:xxx --sql


### 📉 Reverter migração específica

bash
alembic downgrade xxx:xxx --sql


### 🚀 Aplicar até a última migração

bash
alembic upgrade head


### ⏪ Reverter a última migração

bash
alembic downgrade -1


### 🗂 Ver histórico das migrações

bash
alembic history


---

## 📎 Observações

- Certifique-se de que o banco de dados MySQL está rodando localmente e a string de conexão está correta.
- Antes de rodar comandos Alembic, o ambiente virtual deve estar ativado.
- Recomendamos utilizar .env para armazenar credenciais sensíveis.

---

## 📫 Contato

Para dúvidas ou sugestões, entre em contato com a equipe do Projeto FIVE.