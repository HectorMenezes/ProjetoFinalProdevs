"""
Aqui são definidas as variáveis que serão usadas pelo sistema,
como banco de dados, chave de API e URL.
"""
import os

database_dsn = os.getenv('DATABASE_DSN')
external_api_key = os.getenv('EXTERNAL_KEY')
EXTERNAL_API_URL = 'https://qpgj6aa5xa.execute-api.sa-east-1.amazonaws.com/dev/'
