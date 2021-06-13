from fastapi import FastAPI

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
    try:
        run_migration(MigrationType.UPGRADE, 'head')
    except Exception as error:
        print(error)
