from pydantic import BaseModel, constr, conint, confloat, Field


class Operacao(BaseModel):
    id: int = Field(...)
    cpf: str = Field(...)
    pedido: str = Field(...)
    codigo_produto: str = Field(...)
    quantidade: int = Field(...)
    tipo: str = Field(...)