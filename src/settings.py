import os
from decouple import config
database_dsn = os.getenv('DATABASE_DSN')
external_api_url = 'https://qpgj6aa5xa.execute-api.sa-east-1.amazonaws.com/dev/'
external_api_key = config('EXTERNAL_KEY')
