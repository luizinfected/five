# Start project:

fastapi dev main.py 

# db_local_str example:

MYSQL_CONNECTION_STR='mysql+pymysql://root@127.0.0.1:3306/hotel_test'

# Alembic helpers

alembic revision --autogenerate -m "teste" - cria o arquivo de migração

alembic upgrade xxx:xxx --sql - ordem normal

alembic downgrade xxx:xxx --sql - ordem inversa

alembic upgrade head - avançar

alembic downgrade -1 - voltar

alembic history - lista todas migrações
