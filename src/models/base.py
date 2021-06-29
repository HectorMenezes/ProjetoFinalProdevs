"""
A modulo faz a implementação de uma classe base para as operações de banco de dados.
"""
from typing import Tuple, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class BasicCrud:
    """
    A classe tem as operações básicas de save, delete e update.
    """
    def save(self, database_session: Session) -> Tuple[bool, Optional[str]]:
        """
        Salva a instância no banco de dados.
        :param database_session: Sessão do banco de dados.
        :return: Verdadeiro se tudo deu certo, Falso e uma mensagem caso contrário.
        """
        try:
            database_session.add(self)
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def delete(self, database_session: Session) -> Tuple[bool, Optional[str]]:
        """
        Deleta a instância do banco de dados.
        :param database_session: Sessão do banco de dados.
        :return: Verdadeiro se tudo deu certo, Falso e uma mensagem caso contrário.
        """
        try:
            database_session.delete(self)
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def update(self, database_session: Session, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Atualiza instância do banco de dados de acordo com o passado.
        :param database_session: Sessão do banco de dados.
        :param kwargs: Atributos a serem atualizados.
        :return: Verdadeiro se tudo deu certo, Falso e uma mensagem caso contrário.
        """
        try:
            for (attr, _) in self.__dict__.items():
                if kwargs.get(attr):
                    setattr(self, attr, kwargs.get(attr))
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)
