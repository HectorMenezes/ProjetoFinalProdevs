from typing import List, Optional

from sqlalchemy import Column, String, Integer, \
    DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import BasicCrud
from src.services.database import BaseModel, SESSION


class Item(BaseModel, BasicCrud):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_cpf = Column(String(11), ForeignKey('cliente.cpf'))
    codigo_produto = Column(String(200), nullable=False)
    nome = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)

    cliente = relationship('Cliente', back_populates="itens")
