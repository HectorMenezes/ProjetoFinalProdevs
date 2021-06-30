"""
O modulo implementa a rota do produto.
"""
from fastapi import APIRouter
from starlette import status
import aiohttp
from src.settings import EXTERNAL_API_URL, external_api_key


router_produto = APIRouter()


@router_produto.get('/produtos', status_code=status.HTTP_200_OK)
async def get_todos_produtos():
    """
    Acessa a API externa por meio da chave declarada do .env.
    :return: todos os produtos da API externa.
    """
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        async with session.get(EXTERNAL_API_URL + 'produtos') as response:
            return dict(status='SUCESSO', catalogo=await response.json())
