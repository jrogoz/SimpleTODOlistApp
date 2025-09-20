import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from fastapi.testclient import TestClient

from app.models import Base, Task
from app.main import app
from app.database import get_db

# Baza w pamięci dla testów
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))

@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    try:
        session.query(Task).delete()
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

@pytest.fixture(scope='function')
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    return _override_get_db


@pytest.fixture(scope='function')
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}