import aiohttp
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.models.cliente import Cliente as ModelCliente
from src.schemas.compras import InputCompra, ItemOutput
from src.schemas.produto import Produto as SchemaProduto
from src.services.database import get_con, SESSION
from src.settings import external_api_url, external_api_key

router_compras = APIRouter()


@router_compras.get('/compras/{cpf}')
def get_lista_de_compras_do_cliente(cpf: str):
    return cpf


@router_compras.post('/compras')
async def solicita_compra_de_itens(compra: InputCompra, database_session: SESSION = Depends(get_con)):
    # Get Cliente
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=compra.cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA', descricao='Cliente não encontrado'))
    # Get array of produtos
    produtos = []
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        async with session.get(external_api_url + 'produtos') as response:
            for produto in await response.json():
                produtos.append(SchemaProduto(codigo=produto['codigo'],
                                              nome=produto['nome'],
                                              preco=produto['preco'],
                                              quantidade=produto['quantidade']))
    # Create an array of itens and add up the sum
    itens = []
    valor_total = 0
    for item_compra in compra.itens:
        produto = None
        for i in produtos:
            if i.codigo == item_compra.codigo:
                produto = i
        if produto is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=dict(status='REQUISICAO_INVALIDA',
                                             descricao=f'Produto de código {item_compra.codigo} não encontrado'))

        itens.append(ItemOutput(codigo=produto.codigo,
                                nome=produto.nome,
                                preco=produto.preco,
                                quantidade=item_compra.quantidade,
                                total=produto.preco * item_compra.quantidade))
        valor_total += produto.preco * item_compra.quantidade

    # External API
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        payload = {
            "cliente": "32694352740",
            "itens": [
                {
                    "codigo": "ABC123",
                    "quantidade": 2
                }
            ]
        }
        async with session.post(external_api_url + 'compras', data=payload) as response:
            print(await response.json())

    return dict(status='SUCESSO', total=valor_total, itens=itens)


@router_compras.delete('/compras/{cpf}/{pedido}/{item}')
def cancela_compra_de_produto(cpf: str, pedido: str, item: str):
    return cpf + pedido + item
