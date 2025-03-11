from pydantic_settings import BaseSettings as PydanticBaseSettings
from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy import Engine


import os


class BaseSettings(PydanticBaseSettings):
    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)
        if attr is None:
            raise NotImplementedError(f"Env var {item} not implemented")
        return attr


class EnvironmentVariables(BaseSettings):
    load_dotenv()

    FAPI_ROOT_PATH: str = (
        os.getenv("FAPI_ROOT_PATH")
        if os.environ["FAPI_ROOT_PATH"] is None
        else os.environ["FAPI_ROOT_PATH"]
    )

    SQLALCHEMY_DATABASE_URL: str = (
        os.getenv("SQLALCHEMY_DATABASE_URL")
        if os.environ["SQLALCHEMY_DATABASE_URL"] is None
        else os.environ["SQLALCHEMY_DATABASE_URL"]
    )

    SERVER_URL: str = (
        os.getenv("SERVER_URL")
        if os.environ["SERVER_URL"] is None
        else os.environ["SERVER_URL"]
    )

    CLIENT_ID: str = (
        os.getenv("CLIENT_ID")
        if os.environ["CLIENT_ID"] is None
        else os.environ["CLIENT_ID"]
    )

    REALM_NAME: str = (
        os.getenv("REALM_NAME")
        if os.environ["REALM_NAME"] is None
        else os.environ["REALM_NAME"]
    )

    CLIENT_SECRET_KEY: str = (
        os.getenv("CLIENT_SECRET_KEY")
        if os.environ["CLIENT_SECRET_KEY"] is None
        else os.environ["CLIENT_SECRET_KEY"]
    )

    # FastAPI
    FASTAPI_HOST: str = "http://127.0.0.1"
    FASTAPI_PORT: int = 8000
    FASTAPI_RELOAD: bool = False
    FASTAPI_ACCESS_LOG: bool = False
    FASTAPI_ROOT_PATH: str = FAPI_ROOT_PATH


envs = EnvironmentVariables()

pool = create_engine(
    envs.SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_size=10, max_overflow=5
)


def get_database_engine() -> Engine | None:
    return pool
