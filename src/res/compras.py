"""
O modulo implementa a rota de compras.
"""
import aiohttp
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.models.cliente import Cliente as ModelCliente
from src.models.operacao import Operacao as ModelOperacao
from src.schemas.compras import InputCompra
from src.schemas.operacao import Operacao as SchemaOperacao
from src.schemas.produto import Produto as SchemaProduto
from src.services.database import get_con, SESSION
from src.settings import EXTERNAL_API_URL, external_api_key

router_compras = APIRouter()


@router_compras.get('/compras/{cpf}')
def get_lista_de_compras_do_cliente(cpf: str, database_session: SESSION = Depends(get_con)):
    """
    Rota para listar todas as compras do cliente de acordo com o registro no banco de dados.
    :param cpf: CPF do cliente.
    :param database_session: Sessão do banco de dados.
    :return: todas as operações no banco.
    """
    compras = ModelOperacao.get_all_compras_cliente(database_session=database_session, cpf=cpf)
    if not compras:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='SUCESSO', cpf_cliente=cpf,
                                         itens='O cliente não fez nenhuma compra'))
    itens = []

    for i in compras:
        tipo = 'COMPRA' if i.tipo else 'CANCELAMENTO DE COMPRA'
        itens.append(SchemaOperacao(id=i.id,
                                    cpf=i.cpf,
                                    pedido=i.pedido,
                                    codigo_produto=i.codigo_produto,
                                    quantidade=i.quantidade,
                                    tipo=tipo))
    retorno = {
        'status': 'SUCESSO',
        'cpf_cliente': f'{cpf}',
        'itens': itens
    }
    return retorno


@router_compras.post('/compras')
async def solicita_compra_de_itens(compra: InputCompra,
                                   database_session: SESSION = Depends(get_con)):
    """
    Faz compra de acordo com os itens requisitados.
    :param compra: Padrão de payload de acordo com o Schema.
    :param database_session: Sessão do banco de dados.
    :return: Falha na requisição caso a compra não seja possível. Falha no parceiro caso
    exista erro no parceiro. Sucesso caso não exista nenhum problema.
    """
    # Get Cliente
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=compra.cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA',
                                         descricao='Cliente não encontrado'))
    # Get array of produtos
    produtos = []
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        async with session.get(EXTERNAL_API_URL + 'produtos') as response:
            for produto in await response.json():
                produtos.append(SchemaProduto(codigo=produto['codigo'],
                                              nome=produto['nome'],
                                              preco=produto['preco'],
                                              quantidade=produto['quantidade']))
    # Create an array of itens and checks if they are available
    itens_requisicao = []
    for item_compra in compra.itens:
        produto = None
        for i in produtos:
            if i.codigo == item_compra.codigo and i.quantidade > item_compra.quantidade:
                produto = i
        if produto is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=dict(
                                    status='REQUISICAO_INVALIDA',
                                    descricao=f'Produto de código {item_compra.codigo} '
                                              f'não encontrado ou com estoque insuficiente'
                                ))

        itens_requisicao.append({'codigo': produto.codigo,
                                 'quantidade': item_compra.quantidade})

    # External API
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        payload = {
            "cliente": compra.cpf,
            "itens": itens_requisicao
        }
        async with session.post(EXTERNAL_API_URL + 'compras', json=payload) as response:
            retorno = await response.json()
            if retorno['status']:
                retorno['status'] = 'SUCESSO'

                return retorno
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=dict(status='FALHA_NO_PARCEIRO'))


@router_compras.delete('/compras/{cpf}/{pedido}/{item}')
async def cancela_compra_de_produto(cpf: str, pedido: str, item: str):
    """
    Cancela a compra de um item no pedido de acordo com o pedido e o item.
    :param cpf: CPF do cliente.
    :param pedido: id do pedido.
    :param item: id do item.
    :return: Requisição inválida caso não ache algum dos parâmetros. Falha no
    parceiro caso API externa retorne erro. Sucesso caso tudo de certo.
    """
    # NEIEUPMKYN
    # 32694352740
    # ABC123

    # Segundo

    # NGDJYKAWEQ
    # 32694352740
    # ABC123
    # ABC871

    #
    # 32694352740
    #
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        url = EXTERNAL_API_URL + f'{cpf}/{pedido}/{item}'
        print(url)
        async with session.delete(url) as response:
            j = await response.json()
            print(j)
            return j
