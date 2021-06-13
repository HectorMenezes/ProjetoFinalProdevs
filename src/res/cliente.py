from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from starlette import status
from src.schemas.cliente import ClienteInput
from src.models.cliente import Cliente as ModelCliente
from src.services.database import get_con, SESSION
router_cliente = APIRouter()


@router_cliente.post('/clientes')
def cadastra_cliente(cliente: ClienteInput, data_base: SESSION = Depends(get_con)):
    try:
        model_cliente = ModelCliente(cpf=cliente.cpf,
                                     nome=cliente.nome,
                                     email=cliente.email,
                                     data_nasc=cliente.data_nasc,
                                     telefone=cliente.telefone)
        status_user, message = model_cliente.save(connection=data_base)

        if not status_user:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=dict(message='Database error', details=message))
        return 'cadastrado'
    except Exception as e:
        print(e)
        return 'deu ruim'


@router_cliente.get('/clientes/{cpf}')
def get_dados_cliente(cpf: str):
    return cpf


@router_cliente.patch('/clientes/{cpf}')
def atualiza_dados_cliente(cpf: str):
    return cpf


@router_cliente.delete('/clientes/{cpf}')
def deletar_cliente(cpf: str):
    return cpf
