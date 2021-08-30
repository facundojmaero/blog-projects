"""Functions used to access the database."""

from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import database, schemas


def get_drivers(db: Session) -> List[Optional[database.Driver]]:
    return db.query(database.Driver).all()


def create_driver(db: Session, driver: schemas.DriverCreate) -> database.Driver:
    data_in = jsonable_encoder(driver)
    db_driver = database.Driver(**data_in)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def get_teams(db: Session) -> List[Optional[database.Team]]:
    return db.query(database.Team).all()


def get_team(db: Session, team_id: int) -> database.Team:
    return db.query(database.Team).filter(database.Team.id == team_id).first()


def create_team(db: Session, team: schemas.TeamCreate) -> database.Team:
    data_in = jsonable_encoder(team)
    db_team = database.Team(**data_in)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
