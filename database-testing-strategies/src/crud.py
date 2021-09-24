"""Functions used to access the database."""

from typing import Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import database, schemas


def get(db: Session) -> Optional[List[database.Character]]:
    """Get all the characters."""
    return db.query(database.Character).all()


def create(
    db: Session,
    character: Union[schemas.Character, Dict[str, str]],
) -> database.Character:
    """Create and save a character to db."""
    data_in = jsonable_encoder(character)
    db_resource = database.Character(**data_in)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource
