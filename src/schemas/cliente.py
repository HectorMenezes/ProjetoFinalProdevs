from datetime import datetime

from pydantic import BaseModel, Field, constr, EmailStr, validator


class ClienteSchema(BaseModel):
    cpf: constr(max_length=11, min_length=11)
    nome: constr(max_length=100)
    email: EmailStr = Field(...)
    data_nasc: datetime = Field(...)
    telefone: constr(max_length=13, min_length=13)

    # 32694352740
    # 11087773768
    # 41597255971
    @validator('cpf')
    def cpf_valido(cls, v):
        digitos = []
        try:
            for i in v:
                digitos.append(int(i))
        except ValueError:
            raise ValueError('CPF precisa conter somente números')
        # Valida 1o digito
        add = 0
        for i in range(9):
            add += digitos[i] * (10 - i)
        rev = 11 - (add % 11)
        if rev == 10 or rev == 11:
            rev = 0
        if rev != digitos[9]:
            raise ValueError('CPF inválido1')

        add = 0
        for i in range(10):
            add += digitos[i] * (11 - i)
        rev = 11 - add % 11
        if rev == 10 or rev == 11:
            rev = 0
        if rev != digitos[10]:
            raise ValueError('CPF inválido2')
        return v


class ClienteUpdate(BaseModel):
    nome: constr(max_length=100)
    email: EmailStr = Field(...)
    data_nasc: datetime = Field(...)
    telefone: constr(max_length=13, min_length=13)


class ClienteSchemaResponse(BaseModel):
    status: str = Field(...)
    cliente: ClienteSchema = Field(...)
