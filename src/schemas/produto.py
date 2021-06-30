"""
O modulo contém os Schemas do produto
"""

from pydantic import BaseModel, constr, conint, confloat


class Produto(BaseModel):
    """
    Classe do Produto com:
     - codigo (max de 200 caracteres)
     - nome (max de 100 caracteres)
     - preco (float maior que 0)
     - quantidade (int maior que 0)
    """
    codigo: constr(max_length=200)
    nome: constr(max_length=100)
    preco: confloat(gt=0)
    quantidade: conint(gt=0)
