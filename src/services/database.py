"""
O modulo configura as migrações do banco de dados.
"""

from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config


from src.settings import database_dsn

alembic_configuration = Config("alembic.ini")


class MigrationType(Enum):
    """
    Enum com o upgrade e downgrade.
    """
    UPGRADE = 'upgrade'
    DOWNGRADE = 'downgrade'


def run_migration(migration_type: MigrationType, revision: str):
    """
    Executa a migração.
    :param migration_type: tipo da migração de acordo com o enum.
    :param revision: número da revisão
    :return: não tem.
    """
    getattr(command, migration_type.value)(alembic_configuration, revision)


connection_pool = create_engine(database_dsn, pool_size=10)
SESSION = sessionmaker(bind=connection_pool)
BaseModel = declarative_base()


def get_con():
    """
    Faz o yield da sessão.
    :return:
    """
    session = SESSION()
    try:
        yield session
    finally:
        session.close()
