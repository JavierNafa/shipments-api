from os import getenv
from dotenv import load_dotenv

load_dotenv()

database_host = getenv('DATABASE_HOST')
database_username = getenv('DATABASE_USERNAME')
database_password = getenv('DATABASE_PASSWORD')
database_name = getenv('DATABASE_NAME')
api_port = getenv('API_PORT')
fastapi_debug = getenv('FASTAPI_DEBUG',False)
secret_key = getenv('SECRET_KEY')