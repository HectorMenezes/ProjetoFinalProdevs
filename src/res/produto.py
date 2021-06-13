from fastapi import APIRouter
import aiohttp
from src.settings import external_api_url, external_api_key


router_produto = APIRouter()


@router_produto.get('/produtos')
async def get_todos_produtos():
    headers = {
        'x-api-key': 'x0lrm4xjPLWiXor2K4Qy1Dhes391B4n9BGqRpyN7'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(external_api_url + 'produtos') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.json()

            print("Body:", html)
            return dict(chave=external_api_key, reposta=html)
