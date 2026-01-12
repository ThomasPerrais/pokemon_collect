# poke_collect

Flutter project to handle cards and sealed items pokemon collection

## Stack

database: MySQL
    - user: pikachu
    - pwd: dracaufeu2025

backend: SQLAlchemy + DTO + GraphQL FastAPI

frontend: Flutter


## Databases migration

*Alembic* is used to handle migrations of the models and apply them to the MySQL tables.
In order to run a migration after a change in the models.py the following line should be executed from
within the backend folder:

'''
poetry run alembic revision --autogenerate -m "<migration message>"
'''

then to aply the migration to actual data in the MySQL database

'''
poetry run alembic upgrade head
'''
