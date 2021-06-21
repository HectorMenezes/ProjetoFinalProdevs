from typing import List
from pydantic import BaseModel, Field, constr, conint
from src.schemas.produto import Produto


class ItemInput(BaseModel):
    codigo: constr(max_length=200)
    quantidade: conint(gt=0)


class InputCompra(BaseModel):
    cpf: constr(max_length=11, min_length=11)
    itens: List[ItemInput] = Field(...)


class ItemOutput(Produto):
    total: float = Field(...)