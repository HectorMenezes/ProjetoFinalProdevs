import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.cliente import ClienteSchema
from unittest import mock


@pytest.mark.parametrize('cpf,nome,email,data_nasc,telefone', [
    ('32694352740', 'Ralph', 'ralph@detona.com', '2001-06-30T11:23:31.455Z', '1234567890123'),
    ('11087773768', 'Lilo', 'lilo@stich.com', '1992-06-30T11:23:31.455Z', '1234567890157')
])
def test_cadastro_clientes_validos(web_client, database_client, cpf, nome, email, data_nasc, telefone):
    data = {
      "cpf": cpf,
      "nome": nome,
      "email": email,
      "data_nasc": data_nasc,
      "telefone": telefone
    }
    result = web_client.post(f'/clientes',
                             json=data)
    response = result.json()
    assert result.status_code == 200
    assert response['status'] == 'SUCESSO'


@pytest.mark.parametrize('cpf,nome,email,data_nasc,telefone', [
    ('32694352740', 'Ralph', 'ralph@detona.com', '2001-06-30T11:23:31.455Z', '1234567890123'),
    ('11087773768', 'Lilo', 'lilo@stich.com', '1992-06-30T11:23:31.455Z', '1234567890157')
])
# Mock does not work
def test_cadastro_cliente_erro_no_banco(web_client, database_client, cpf, nome, email, data_nasc, telefone):
    with mock.patch.object(Session, 'commit', side_effect=SQLAlchemyError):
        data = {
            "cpf": cpf,
            "nome": nome,
            "email": email,
            "data_nasc": data_nasc,
            "telefone": telefone
        }
        result = web_client.post(f'/clientes',
                                 json=data)
        response = result.json()
        assert result.status_code == 500
        assert response['status'] == 'FALHA_INTERNA'
