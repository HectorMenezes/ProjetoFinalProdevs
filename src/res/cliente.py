from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.models.cliente import Cliente as ModelCliente
from src.schemas.cliente import ClienteSchema, ClienteUpdate, ClienteSchemaResponse
from src.services.database import get_con, SESSION

router_cliente = APIRouter()


@router_cliente.post('/clientes', status_code=200)
def cadastra_cliente(cliente: ClienteSchema, database_session: SESSION = Depends(get_con)):
    model_cliente = ModelCliente(cpf=cliente.cpf,
                                 nome=cliente.nome,
                                 email=cliente.email,
                                 data_nasc=cliente.data_nasc,
                                 telefone=cliente.telefone)
    status_user, message = model_cliente.save(database_session=database_session)

    if not status_user:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='REQUISICAO_INVALIDA', descricao='Cliente não encontrado'))

    return dict(status='SUCESSO')


@router_cliente.get('/clientes/{cpf}', response_model=ClienteSchemaResponse)
def get_dados_cliente(cpf: str, database_session: SESSION = Depends(get_con)):
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA', descricao='Cliente não encontrado'))
    return dict(status='SUCESSO',
                cliente=ClienteSchema(cpf=cliente.cpf,
                                      nome=cliente.nome,
                                      email=cliente.email,
                                      data_nasc=cliente.data_nasc,
                                      telefone=cliente.telefone))


@router_cliente.patch('/clientes/{cpf}', response_model=ClienteSchemaResponse)
def atualiza_dados_cliente(cpf: str, cliente_update: ClienteUpdate, database_session: SESSION = Depends(get_con)):
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA', descricao='Cliente não encontrado'))

    status_cliente, message = cliente.update(database_session=database_session,
                                             nome=cliente_update.nome,
                                             email=cliente_update.email,
                                             data_nasc=cliente_update.data_nasc,
                                             telefone=cliente_update.telefone)

    if not status_cliente:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='FALHA_INTERNA', descricao='Erro no banco de dados'))

    return dict(status='SUCESSO',
                cliente=ClienteSchema(cpf=cliente.cpf,
                                      nome=cliente.nome,
                                      email=cliente.email,
                                      data_nasc=cliente.data_nasc,
                                      telefone=cliente.telefone))


@router_cliente.delete('/clientes/{cpf}')
def excluir_cliente(cpf: str, database_session: SESSION = Depends(get_con)):
    cliente = ModelCliente.get_by_cpf(database_session=database_session, cpf=cpf)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=dict(status='REQUISICAO_INVALIDA', descricao='Cliente não encontrado'))

    status_cliente, message = cliente.delete(database_session=database_session)

    if not status_cliente:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=dict(status='FALHA_INTERNA', descricao='Erro no banco de dados'))

    return dict(status='SUCESSO')
