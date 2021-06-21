from pydantic import BaseModel, constr, conint, confloat


class Produto(BaseModel):
    codigo: constr(max_length=200)
    nome: constr(max_length=100)
    preco: confloat(gt=0)
    quantidade: conint(gt=0)
