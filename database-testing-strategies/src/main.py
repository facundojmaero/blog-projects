"""Main FastAPI application."""

from typing import Any, List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, database, schemas

database.Base.metadata.create_all(bind=database.engine)


app = FastAPI()


def get_db():
    """Return a new db session. Used as a FastAPI dependency."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/characters", response_model=schemas.Character)
def create_character(
    character: schemas.Character,
    db: Session = Depends(get_db),
) -> Any:
    """Endpoint to create a character.

    Args:
        character (schemas.Character): character input data
        db (Session): A database session
    """
    return crud.create(db=db, character=character)


@app.get("/characters", response_model=List[schemas.Character])
def read_characters(db: Session = Depends(get_db)) -> Any:
    """Endpoint to read characters.

    Args:
        db (Session, optional): A database session
    """
    teams = crud.get(db)
    return teams
