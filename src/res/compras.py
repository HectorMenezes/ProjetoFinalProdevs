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
        tipo = 'COMPRA' if not i.tipo else 'CANCELAMENTO DE COMPRA'
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
    # Add valid produtos to request
    request_produtos = []
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        async with session.get(EXTERNAL_API_URL + 'produtos') as response:
            resposta_json = await response.json()

            for item in compra.itens:
                for produto in resposta_json:
                    if item.codigo == produto['codigo'] and item.quantidade <= produto['quantidade']:
                        request_produtos.append({'codigo': item.codigo,
                                                 'quantidade': item.quantidade})
                    elif item.codigo == produto['codigo']:
                        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                            content=dict(
                                                status='REQUISICAO_INVALIDA',
                                                descricao=f'Produto de código {item.codigo} '
                                                          f'não encontrado ou com estoque insuficiente'
                                            ))
    # External API
    async with aiohttp.ClientSession(headers={'x-api-key': external_api_key}) as session:
        payload = {
            "cliente": compra.cpf,
            "itens": request_produtos
        }
        async with session.post(EXTERNAL_API_URL + 'compras', json=payload) as response:
            retorno = await response.json()
            if retorno['status']:
                retorno['status'] = 'SUCESSO'
                # Local database
                for item in compra.itens:
                    model_operacao = ModelOperacao(cpf=compra.cpf,
                                                   pedido=retorno['pedido'],
                                                   codigo_produto=item.codigo,
                                                   quantidade=item.quantidade,
                                                   tipo=False)
                    status_operacao = model_operacao.save(database_session=database_session)
                    if not status_operacao:
                        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                            content=dict(status='FALHA_INTERNA',
                                                         descricao='Erro no banco de dados'))
                return retorno
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=dict(status='FALHA_NO_PARCEIRO'))


@router_compras.delete('/compras/{cpf}/{pedido}/{item}')
async def cancela_compra_de_produto(cpf: str, pedido: str, item: str,
                                    database_session: SESSION = Depends(get_con)):
    """
    Cancela a compra de um item no pedido de acordo com o pedido e o item.
    :param cpf: CPF do cliente.
    :param pedido: id do pedido.
    :param item: id do item.
    :param database_session: Sessão do banco de dados.
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
        async with session.delete(EXTERNAL_API_URL + f'{cpf}/{pedido}/{item}') as response:
            retorno = await response.json()
            print(retorno)
            if not retorno['status']:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content=dict(status='FALHA_NO_PARCEIRO',
                                                 mensagem=retorno['mensagem']))

            model_compra = ModelOperacao.get_by_cliente_pedido_e_item(
                database_session=database_session,
                cpf=cpf,
                pedido=pedido,
                item=item
            )
            if not model_compra:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content=dict(
                                        status='REQUISICAO_INVALIDA',
                                        descricao='Item do pedido não encontrado localmente'
                                    ))
            model_exclusao = ModelOperacao(cpf=cpf,
                                           pedido=pedido,
                                           codigo_produto=item,
                                           quantidade=model_compra.quantidade,
                                           tipo=True)
            status_exclusao = model_exclusao.save(database_session=database_session)
            if not status_exclusao:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content=dict(status='FALHA_INTERNA',
                                                 descricao='Erro no banco de dados'))
            return retorno
