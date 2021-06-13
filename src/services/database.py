from enum import Enum

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import database_dsn

alembic_configuration = Config("alembic.ini")


class MigrationType(Enum):
    UPGRADE = 'upgrade'
    DOWNGRADE = 'downgrade'


def run_migration(migration_type: MigrationType, revision: str):
    getattr(command, migration_type.value)(alembic_configuration, revision)


connection_pool = create_engine(database_dsn, pool_size=10)
SESSION = sessionmaker(bind=connection_pool)
BaseModel = declarative_base()


def get_con():
    session = SESSION()
    try:
        yield session
    finally:
        session.close()
