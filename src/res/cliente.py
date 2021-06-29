from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.models.cliente import Cliente as ModelCliente
from src.schemas.cliente import ClienteSchema, ClienteUpdate, ClienteSchemaResponse
from src.services.database import get_con, SESSION

router_cliente = APIRouter()


@router_cliente.post('/clientes', status_code=200)
def cadastra_cliente(cliente: ClienteSchema, database_session: SESSION = Depends(get_con)):
    """
    A rota cadastra o cliente de acordo com CPF, nome, email, data de nascimento e telefone.
    :param cliente: Dados cadastrais do cliente.
    :param database_session: Sessão do banco de dados.
    :return: Falha interna caso erro do banco de dados.
    Sucesso caso o cadastro seja feito com sucesso.
    """
    model_cliente = ModelCliente(cpf=cliente.cpf,
                                 nome=cliente.nome,
                                 email=cliente.email,
                                 data_nasc=cliente.data_nasc,
                                 telefone=cliente.telefone)
    status_cliente = model_cliente.save(database_session=database_session)

    if not status_cliente:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='FALHA_INTERNA',
                                         descricao='Erro no banco de dados'))

    return dict(status='SUCESSO')


@router_cliente.get('/clientes/{cpf}', response_model=ClienteSchemaResponse)
def get_dados_cliente(cpf: str, database_session: SESSION = Depends(get_con)):
    """
    A rota retorna os dados de um cliente cadastrado.
    :param cpf: CPF do cliente.
    :param database_session: Sessão do banco de dados.
    :return: Requisição inválida caso o cliente não exista.
    Caso exista, retorna os dados.
    """
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA',
                                         descricao='Cliente não encontrado'))
    return dict(status='SUCESSO',
                cliente=ClienteSchema(cpf=cliente.cpf,
                                      nome=cliente.nome,
                                      email=cliente.email,
                                      data_nasc=cliente.data_nasc,
                                      telefone=cliente.telefone))


@router_cliente.patch('/clientes/{cpf}', response_model=ClienteSchemaResponse)
def atualiza_dados_cliente(cpf: str, cliente_update: ClienteUpdate,
                           database_session: SESSION = Depends(get_con)):
    """
    A rota atualiza os dados cliente, menos o CPF.
    :param cpf: CPF do cliente a ser atualizado.
    :param cliente_update: dados do cliente a ser atualizado de acordo com o Schema.
    :param database_session: Sessão do banco de dados
    :return: Requisição inválida caso o cliente não exista.
    Falha interna caso exista um problema no banco de dados.
    Sucesso caso a atualização aconteça.
    """
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA',
                                         descricao='Cliente não encontrado'))

    status_cliente = cliente.update(database_session=database_session,
                                    nome=cliente_update.nome,
                                    email=cliente_update.email,
                                    data_nasc=cliente_update.data_nasc,
                                    telefone=cliente_update.telefone)

    if not status_cliente:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='FALHA_INTERNA',
                                         descricao='Erro no banco de dados'))

    return dict(status='SUCESSO',
                cliente=ClienteSchema(cpf=cliente.cpf,
                                      nome=cliente.nome,
                                      email=cliente.email,
                                      data_nasc=cliente.data_nasc,
                                      telefone=cliente.telefone))


@router_cliente.delete('/clientes/{cpf}')
def excluir_cliente(cpf: str, database_session: SESSION = Depends(get_con)):
    """
    A rota excluí um cliente cadastrado no sistema por meio de CPF.
    :param cpf: CPF do cliente a ser excluído.
    :param database_session: sessão do banco de dados
    :return: Requisição inválida caso o cliente não exista.
    Erro interno caso problema no banco de dados. Sucesso caso
    tudo de certo.
    """
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA',
                                         descricao='Cliente não encontrado'))

    status_cliente = cliente.delete(database_session=database_session)

    if not status_cliente:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='FALHA_INTERNA',
                                         descricao='Erro no banco de dados'))

    return dict(status='SUCESSO')
