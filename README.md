# genki

## Development setup

1. Install [poetry](https://python-poetry.org/).
2. Run `poetry install`.
3. Run `poetry run python manage.py migrate` 
4. Run `export $(cat .env | xargs) && poetry run python manage.py runserver`
