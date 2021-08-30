# Writing FastAPI database tests with SQLAlchemy and PostgreSQL

This is the companion code of the article found [here](https://facundojmaero.github.io/blog/2021/08/fastapi-db-tests/)

## Set up

* Create a virtualenv: `python3 -m venv env`
* Activate it: `source env/bin/activate`
* Install the project dependencies: `pip install -r requirements.txt`

## How to run the project?

* Start the database: `docker-compose up -d`
* Start the API: `uvicorn src.main:app`
* Explore the API in `http://localhost:8000/docs`

## How to run the tests?

* Start the database: `docker-compose up -d`
* Run the tests: `pytest`
