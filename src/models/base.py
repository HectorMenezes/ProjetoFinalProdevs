from typing import Tuple, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class BasicCrud:

    def save(self, database_session: Session) -> Tuple[bool, Optional[str]]:
        try:
            database_session.add(self)
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def delete(self, database_session: Session) -> Tuple[bool, Optional[str]]:
        try:
            database_session.delete(self)
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)

    def update(self, database_session: Session, **kwargs) -> Tuple[bool, Optional[str]]:
        try:
            for (attr, _) in self.__dict__.items():
                if kwargs.get(attr):
                    setattr(self, attr, kwargs.get(attr))
            database_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ' '.join(error.args)
