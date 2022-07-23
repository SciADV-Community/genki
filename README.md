# genki

![Build Status](https://github.com/SciADV-Community/genki/workflows/CI%20%26%20CD/badge.svg)

Genki is the web service component of [rosetta](https://github.com/SciADV-Community/rosetta), a Discord bot for visual novels playthrough servers. It is built with [Django](https://www.djangoproject.com/) and [tailwindcss](https://tailwindcss.com/).

## Development setup

You need Python 3.8 installed.

1. Install [poetry](https://python-poetry.org/).
2. Run `poetry install`.
3. Run `poetry run python manage.py migrate`
4. Run `export $(cat .env | xargs) && poetry run python manage.py runserver`

## Building the CSS

Run `poetry run python manage.py tailwind build`.

## Production setup

1. Create an `.env` file with:

-   `GENKI_SECRET`: The secret key.
-   `GENKI_ALLOWED_HOSTS`: The allowed hosts (comma separated).
-   `DISCORD_CLIENT_ID`: The Discord app ID.
-   `DISCORD_CLIENT_SECRET`: The Discord app Secret.
-   `GENKI_DB_USER`: The database username for genki.
-   `GENKI_DB_PASSWORD`: The database password for genki.
-   `GENKI_DB_HOST`: The hostname of the PostgreSQL instance (for pointing to localhost outside of docker, use `host.docker.internal` if you're using Docker Desktop, or (probably, check with `ifconfig`) `172.17.0.1` on Linux).
-   `GENKI_DB_PORT`: The port the PostgreSQL instance is running on (5432 by default).
-   (Optional) `GENKI_HTTPS`: If serving over HTTPS.

2. Build the images with `docker-compose build`.
3. Create the `genki_media` volume with `docker volume create genki_media`.
4. Run the images.

-   If you want to also run a database instance, run:
    ```sh
    docker-compose -f docker-compose.yml -f docker-compose.db.yml up
    ```
    And add the following to your .env file:
    -   `POSTGRES_USER`: Same as `GENKI_DB_USER`.
    -   `POSTGRES_PASSWORD`: Same as `GENKI_DBPASSWORD`.
    -   `POSTGRESS_DB`: `genki`.
-   If you are using another PostgreSQL instance, then just run:
    ```sh
    docker-compose up
    ```
