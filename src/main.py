"""
Esse modulo incluí todas as rotas do sistema e faz as migrações.
"""
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from src.res.cliente import router_cliente
from src.res.compras import router_compras
from src.res.produto import router_produto
from src.services.database import run_migration, MigrationType


APP = FastAPI(title="ProjetoFinalProdevs", version="0.0.1")

APP.include_router(router=router_compras, tags=['Compras'])
APP.include_router(router=router_cliente, tags=['Clientes'])
APP.include_router(router=router_produto, tags=['Produtos'])


@APP.on_event('startup')
def start_up():
    """
    Faz as migrações ao iniciar o APP.
    :return: Nada
    """
    try:
        run_migration(MigrationType.UPGRADE, 'head')
    except SQLAlchemyError as error:
        print(error)
