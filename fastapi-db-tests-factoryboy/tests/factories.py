import factory
import pytest
from pytest_factoryboy import LazyFixture, register
from sqlalchemy.orm import Session
from src import database, schemas


class SQLAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def save_db_session(cls, session: Session) -> None:
        cls._meta.sqlalchemy_session = session

        for cls_attr in vars(cls).values():
            if hasattr(cls_attr, "get_factory"):
                cls_attr.get_factory().save_db_session(session=session)


class TeamModelFactory(SQLAlchemyFactory):
    class Meta:
        model = database.Team

    name = factory.Sequence(lambda n: f"Team {n}")


class TeamCreateFactory(factory.Factory):
    class Meta:
        model = schemas.TeamCreate

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Team {n}")


class DriverModelFactory(SQLAlchemyFactory):
    class Meta:
        model = database.Driver

    id = factory.Sequence(lambda n: n)
    name = factory.Iterator(["Facundo", "Joaquin"])
    team = factory.SubFactory(TeamModelFactory)
    number = factory.Sequence(lambda n: n)
    nationality = factory.Iterator(["Argentina", "France"])


@pytest.fixture(autouse=True)
def _setup_factories(db_fixture):
    TeamModelFactory.save_db_session(session=db_fixture)
    DriverModelFactory.save_db_session(session=db_fixture)

    TeamModelFactory.reset_sequence()
    TeamCreateFactory.reset_sequence()
    DriverModelFactory.reset_sequence()


register(TeamModelFactory)
register(TeamCreateFactory)
register(DriverModelFactory)

register(
    TeamModelFactory,
    "red_bull",
    name="Red Bull Racing",
)

register(
    DriverModelFactory,
    "max_verstappen",
    name="Max Verstappen",
    number=33,
    nationality="Dutch",
    team=LazyFixture("red_bull"),
)
