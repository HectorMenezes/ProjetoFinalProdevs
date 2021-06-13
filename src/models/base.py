from typing import Tuple, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class BasicCrud:

    def save(self, connection: Session) -> Tuple[bool, Optional[str]]:
        try:
            connection.add(self)
            connection.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def delete(self, connection: Session) -> Tuple[bool, Optional[str]]:
        try:
            connection.delete(self)
            connection.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def update(self, connection: Session, **kwargs) -> Tuple[bool, Optional[str]]:
        try:
            for (attr, _) in self.__dict__.items():
                if kwargs.get(attr):
                    setattr(self, attr, kwargs.get(attr))
            connection.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)
