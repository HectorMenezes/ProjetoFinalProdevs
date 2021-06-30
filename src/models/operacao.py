"""
O modulo faz o modelo de operação da base de dados.
"""
from typing import Optional, List

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.models.base import BasicCrud
from src.services.database import BaseModel, SESSION


class Operacao(BaseModel, BasicCrud):
    """
    A classe tem os elementos base de uma operação. Vale ressaltar que caso Tipo = False -> Compra
    """
    __tablename__ = 'operacao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), ForeignKey('cliente.cpf'))
    pedido = Column(String(100), nullable=False)
    codigo_produto = Column(String(200), nullable=False)
    quantidade = Column(Integer, nullable=False)
    tipo = Column(Boolean, nullable=False)
    cliente = relationship('Cliente', back_populates="operacoes")

    @classmethod
    def get_by_cliente_e_pedido(cls, database_session: SESSION, cpf: str,
                                pedido: str) -> Optional['Operacao']:
        """
        Retorna um pedido específico de um cliente.
        :param database_session: Sessão do banco de dados.
        :param cpf: CPF do cliente.
        :param pedido: Pedido a ser pesquisado.
        :return: primeiro pedido encontrado.
        """
        return database_session.query(cls).filter_by(cpf=cpf, pedido=pedido).first()

    @classmethod
    def get_by_cliente_pedido_e_item(cls, database_session: SESSION, cpf: str,
                                     pedido: str, item: str) -> Optional['Operacao']:
        """
        Retorna um pedido específico de um cliente.
        :param database_session: Sessão do banco de dados.
        :param cpf: CPF do cliente.
        :param pedido: Pedido a ser pesquisado.
        :param item: Item a ser pesquisado
        :return: primeiro pedido encontrado.
        """
        return database_session.query(cls).filter_by(cpf=cpf, pedido=pedido, codigo_produto=item).first()

    @classmethod
    def get_all_compras_cliente(cls, database_session: SESSION, cpf: str) -> List['Operacao']:
        """
        Retorna as compras de um cliente
        :param database_session: Sessão do banco de dados.
        :param cpf: CPF do cliente.
        :return: Todas as compras do cliente.
        """
        return database_session.query(cls).filter_by(cpf=cpf).all()
