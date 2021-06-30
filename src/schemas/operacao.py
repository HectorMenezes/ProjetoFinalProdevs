"""
Schemas das operações para registrar as atividades do usuário
"""
from pydantic import BaseModel, Field


class Operacao(BaseModel):
    """
    Operação básica de acordo com o modelo, com:
    - id
    - cpf
    - pedido
    - codigo do produto
    - quantidade
    - tipo
    """
    id: int = Field(...)
    cpf: str = Field(...)
    pedido: str = Field(...)
    codigo_produto: str = Field(...)
    quantidade: int = Field(...)
    tipo: str = Field(...)
