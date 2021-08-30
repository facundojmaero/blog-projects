import pytest
from src import crud

from . import factories


def test_create_one_team(client):
    team_data = {"name": "Scuderia Ferrari"}

    response = client.post("/teams", json=team_data)

    received = response.json()
    expected = {"id": 1, "name": "Scuderia Ferrari"}

    assert response.status_code == 200
    assert received == expected


def test_get_team(client):
    team_data = {"name": "Scuderia Ferrari"}
    _ = client.post("/teams", json=team_data)

    response = client.get("/teams")

    expected = [{"id": 1, "name": team_data["name"]}]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_team_orm(client, db_fixture):
    team_data = {"name": "Scuderia Ferrari"}

    crud.create_team(db=db_fixture, team=team_data)

    response = client.get("/teams")

    expected = [{"id": 1, "name": team_data["name"]}]

    assert response.status_code == 200
    assert response.json() == expected


def test_create_one_team_factoryboy(client):
    team_data = factories.TeamCreateFactory()
    response = client.post("/teams", json=team_data.dict())

    expected = {"id": 1, "name": team_data.name}

    assert response.status_code == 200
    assert response.json() == expected


def test_create_one_team_factoryboy_custom_name(client):
    team_data = factories.TeamCreateFactory(name="Mercedes-AMG")
    response = client.post("/teams", json=team_data.dict())

    expected = {"id": 1, "name": "Mercedes-AMG"}

    assert response.status_code == 200
    assert response.json() == expected


def test_get_team_sqlalchemy_factory(client):
    created_team = factories.TeamModelFactory()

    response = client.get("/teams")

    expected = [{"id": 1, "name": created_team.name}]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_many_teams_sqlalchemy_factory(client):
    created_teams = factories.TeamModelFactory.create_batch(3)

    response = client.get("/teams")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_drivers(client):
    driver = factories.DriverModelFactory()

    response = client.get("/drivers")
    expected = [
        {
            "id": driver.id,
            "name": driver.name,
            "number": driver.number,
            "nationality": driver.nationality,
            "team": {
                "name": driver.team.name,
            },
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_many_teams_sqlalchemy_factory_pytest(client, team_model_factory):
    created_teams = team_model_factory.create_batch(3)

    response = client.get("/teams")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_team_sqlalchemy_factory_pytest(client, team):
    response = client.get("/teams")

    expected = [{"id": 1, "name": team.name}]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_drivers_sqlalchemy_factory_pytest(client, driver):
    response = client.get("/drivers")
    expected = [
        {
            "id": driver.id,
            "name": driver.name,
            "number": driver.number,
            "nationality": driver.nationality,
            "team": {
                "name": driver.team.name,
            },
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("team__name", ["Alpine F1 Team"])
def test_get_team_sqlalchemy_factory_pytest_custom(client, team):
    response = client.get("/teams")

    expected = [{"id": 1, "name": "Alpine F1 Team"}]

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("driver__name", ["Valtteri Bottas"])
@pytest.mark.parametrize("driver__number", [77])
def test_get_drivers_sqlalchemy_factory_pytest_custom(client, driver):
    response = client.get("/drivers")
    expected = [
        {
            "id": driver.id,
            "name": "Valtteri Bottas",
            "number": 77,
            "nationality": driver.nationality,
            "team": {
                "name": driver.team.name,
            },
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_red_bull(client, red_bull):
    response = client.get("/teams")

    expected = [{"id": 1, "name": "Red Bull Racing"}]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_verstappen(client, max_verstappen):
    response = client.get("/drivers")
    expected = [
        {
            "id": max_verstappen.id,
            "name": "Max Verstappen",
            "number": 33,
            "nationality": "Dutch",
            "team": {
                "name": "Red Bull Racing",
            },
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected
