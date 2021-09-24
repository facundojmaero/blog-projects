"""Strategies for getting a testing db session."""

import sqlalchemy as sa
from src.database import Base


def drop_strategy(testing_session, engine):
    """Get a db session.

    The database is dropped and recreated on every call
    """
    try:
        Base.metadata.create_all(bind=engine)

        db = testing_session()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def clear_strategy(testing_session):
    """Get a db session.

    Every db table is deleted on every call
    """
    try:
        db = testing_session()
        yield db
    finally:
        db.close()

        # Empty all tables after each test
        session = testing_session()
        session.execute(
            "TRUNCATE {} RESTART IDENTITY;".format(
                ",".join(table.name for table in reversed(Base.metadata.sorted_tables))
            )
        )
        session.commit()
        session.close()


def subtransaction_factory(testing_session, engine):
    """Get a db session.

    The transaction is rolled back on every savepoint
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = testing_session(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()
