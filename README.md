# LuckyPay
This is a FastApi project that reproduces a very popular system of raffle in brazil

## Techs:
Here we are using some technologies: 
 - FastApi
 - SqlModel (SQLAlchemy)
 - Alembic
 - Postgres
 - Astral Uv
 - Keycloak

## Prerequesites
Make sure you have: 
 - Docker
 - Astral Uv

## Instalation

Fist of all you have to execute all containers in docker compose: to make available the needed services:
 - Keycloak
 - Postgres

to this just run the following command on root path of the project: 

```bash
docker compose up -d
```

after this install all dependencies with uv executing the following command:

```bash
uv sync --extra dev
```

The `--extra dev` causes development dependencies to be installed as well

After that, to execute the application just execute the following command: 

```bash
uvicorn api.app:get_app --host 0.0.0.0 --port 8000 --factory
```

or, if you have configured the vscode to execute automatically, just press `F5`

> make sure you have an .env file with all environment variables