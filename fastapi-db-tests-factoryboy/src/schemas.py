"""Pydantic schemas used to model data coming in and going to a client."""
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Schema used as a base."""

    class Config:
        orm_mode = True


class TeamBase(BaseSchema):
    """Schema that holds the common fields of a Team."""

    name: str


class TeamCreate(TeamBase):
    """Schema that holds the data needed to create a Team."""

    pass


class Team(TeamBase):
    """Schema that holds the data returned when requesting a Team."""

    id: int


class DriverBase(BaseSchema):
    """Schema that holds the common fields of a Driver."""

    name: str
    number: int
    nationality: str


class DriverCreate(DriverBase):
    """Schema that holds the data needed to create a Driver."""

    team_id: int


class Driver(DriverBase):
    """Schema that holds the data returned when requesting a Driver."""

    id: int
    team: TeamBase
