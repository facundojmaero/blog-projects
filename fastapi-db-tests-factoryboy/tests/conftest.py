import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.main import app, get_db

pytest_plugins = [
    "tests.factories",
]


@pytest.fixture
def db_fixture():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/f1.db"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        Base.metadata.create_all(bind=engine)

        db = testing_session_local()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_fixture):
    def override_get_db():
        yield db_fixture

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
