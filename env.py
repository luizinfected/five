import os
from dotenv import load_dotenv

load_dotenv()

# NEED ON DEV SIDE
SECRET_KEY = os.getenv('SECRET_KEY')    
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
LOCAL_MYSQL_CONNECTION_STR=  os.getenv('LOCAL_MYSQL_CONNECTION_STR')
IS_DEV= os.getenv('IS_DEV')


# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
RDS_USER= os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_HOST= os.getenv('RDS_HOST')
RDS_PORT= os.getenv('RDS_PORT')
RDS_DATABASE= os.getenv('RDS_DATABASE')


