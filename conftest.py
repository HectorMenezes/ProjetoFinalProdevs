import pytest
from fastapi.testclient import TestClient
from src.main import APP
from src.services.database import run_migration, MigrationType, SESSION


@pytest.fixture
def web_client():
    cliente = TestClient(APP)
    yield cliente


@pytest.fixture
def database_client():
    run_migration(migration_type=MigrationType.DOWNGRADE, revision='base')
    run_migration(migration_type=MigrationType.DOWNGRADE, revision='base')
    session = SESSION()
    yield session
    session.close()
