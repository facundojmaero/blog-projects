import os

import pytest
from fastapi import status
from src import crud


def test_create_character(client):
    """Can create a character using a POST request."""
    data = {"name": "Rick Sanchez", "origin": "Earth (C-137)"}

    response = client.post("/characters", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data


def test_get_character(client, db_fixture):
    """Can retrieve many created characters."""
    characters = [
        {"name": "Rick Sanchez", "origin": "Earth (C-137)"},
        {"name": "Morty Smith", "origin": "Earth (C-137)"},
        {"name": "Beth Smith", "origin": "Earth (C-137)"},
        {"name": "Jerry Smith", "origin": "Earth (C-137)"},
    ]

    for character in characters:
        crud.create(db=db_fixture, character=character)

    response = client.get("/characters")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == characters


@pytest.mark.parametrize("meeseks_number", range(int(os.getenv("meeseks"))))
def test_hog(client, meeseks_number):
    """Can create a character many times."""
    data = {
        "name": f"Mr. Meeseks number {meeseks_number}",
        "origin": "Mr. Meeseks Box",
    }
    response = client.post("/characters", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data


def test_using_ids(db_fixture):
    character = {"name": "Birdperson", "origin": "Earth (C-137)"}

    created_character = crud.create(db=db_fixture, character=character)

    assert created_character.id == 1
