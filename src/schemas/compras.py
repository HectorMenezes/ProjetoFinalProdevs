"""
Schemas de compras, com todas as validações relacionadas à entrada/saídas.
"""
from typing import List
from pydantic import BaseModel, Field, constr, conint
from src.schemas.produto import Produto


class ItemInput(BaseModel):
    """
    Input do item com:
    - codigo (max de 200 carateres)
    - quantidade (int maior que 0)
    """
    codigo: constr(max_length=200)
    quantidade: conint(gt=0)


class InputCompra(BaseModel):
    """
    Input da compra com:
    - cpf (11 caracteres)
    - itens (itens definidos no ItemInput)
    """
    cpf: constr(max_length=11, min_length=11)
    itens: List[ItemInput] = Field(...)


class ItemOutput(Produto):
    """
    Output de itens, é o mesmo que o produto, mas com:
    - total (float)
    """
    total: float = Field(...)
