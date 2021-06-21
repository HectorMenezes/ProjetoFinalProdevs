from fastapi import APIRouter
import aiohttp
from src.settings import external_api_url, external_api_key


router_produto = APIRouter()


@router_produto.get('/produtos')
async def get_todos_produtos():
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        async with session.get(external_api_url + 'produtos') as response:
            return dict(status='SUCESSO', catalogo=await response.json())
