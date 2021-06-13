from fastapi import APIRouter

router_compras = APIRouter()


@router_compras.get('/compras/{cpf}')
def get_lista_de_compras_do_cliente(cpf: str):
    return cpf


@router_compras.post('/compras')
def solicita_compra_de_itens():
    return 'hey'


@router_compras.delete('/compras/{cpf}/{pedido}/{item}')
def cancela_compra_de_produto(cpf: str, pedido: str, item: str):
    return cpf + pedido + item
