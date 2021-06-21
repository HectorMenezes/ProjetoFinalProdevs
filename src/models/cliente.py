from typing import Optional

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from src.models.base import BasicCrud
from src.services.database import BaseModel, SESSION


class Cliente(BaseModel, BasicCrud):
    __tablename__ = 'cliente'
    cpf = Column(String(11), primary_key=True, autoincrement=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(200), nullable=True)
    data_nasc = Column(DateTime, nullable=True)
    telefone = Column(String(13), nullable=False)

    itens = relationship('Item', back_populates="cliente")

    @classmethod
    def get_by_cpf(cls, database_session: SESSION, cpf: str) -> Optional['Cliente']:
        return database_session.query(cls).filter_by(cpf=cpf).first()
