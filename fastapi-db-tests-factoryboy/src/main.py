"""Main FastAPI application."""

from typing import Any, List

from fastapi import Depends, FastAPI, HTTPException
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


@app.post("/teams", response_model=schemas.Team)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
) -> Any:
    """Endpoint to create a Team.

    Args:
        team (schemas.TeamCreate): Team input data
        db (Session): A database session
    """
    return crud.create_team(db=db, team=team)


@app.get("/teams", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)) -> Any:
    teams = crud.get_teams(db)
    return teams


@app.post("/drivers", response_model=schemas.Driver)
def create_driver(
    driver: schemas.DriverCreate,
    db: Session = Depends(get_db),
) -> Any:
    team_db = crud.get_team(db=db, team_id=driver.team_id)
    if team_db is None:
        raise HTTPException(status_code=404, detail="Team not found")

    return crud.create_driver(db=db, driver=driver)


@app.get("/drivers", response_model=List[schemas.Driver])
def read_drivers(db: Session = Depends(get_db)) -> Any:
    return crud.get_drivers(db)
