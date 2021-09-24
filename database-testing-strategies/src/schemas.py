"""Pydantic schemas used to model data coming in and going to a client."""
from pydantic import BaseModel


class Character(BaseModel):
    """Schema that holds the common fields of a Character."""

    name: str
    origin: str

    class Config:
        orm_mode = True
