from enum import Enum

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src import settings
from src.database import Base
from src.main import app, get_db

from . import testing_strategies


class TestingStrategyEnum(Enum):
    """An enumeration of the different testing strategies to reset the db."""

    drop = "drop"
    clear = "clear"
    subtransaction = "subtransaction"


@pytest.fixture
def testing_strategy(request) -> TestingStrategyEnum:
    """Get the selected testing strategy."""
    strategy: str = request.config.getoption("--strategy")

    try:
        return TestingStrategyEnum(strategy)
    except ValueError:
        raise pytest.exit(
            msg="Please provide a valid strategy",
            returncode=pytest.ExitCode.USAGE_ERROR,
        )


@pytest.fixture(scope="session", name="engine")
def get_engine():
    """Get a sqlalchemy engine connected to the db."""
    return create_engine(settings.SQLALCHEMY_TESTING_DATABASE_URL)


@pytest.fixture(scope="session")
def testing_session(engine) -> Session:
    """Get a sessionmaker connected to the db."""
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    yield testing_session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_fixture(testing_session, engine, testing_strategy):
    """Get a database session using the selected strategy."""
    if testing_strategy == TestingStrategyEnum.drop:
        yield from testing_strategies.drop_strategy(testing_session, engine)
    elif testing_strategy == TestingStrategyEnum.clear:
        yield from testing_strategies.clear_strategy(testing_session)
    elif testing_strategy == TestingStrategyEnum.subtransaction:
        yield from testing_strategies.subtransaction_factory(testing_session, engine)


@pytest.fixture()
def client(db_fixture):
    """Get an http testing client."""
    app.dependency_overrides[get_db] = lambda: db_fixture
    yield TestClient(app)
    del app.dependency_overrides[get_db]
