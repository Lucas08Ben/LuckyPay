from api.configuration.settings import get_database_engine
from sqlmodel import Session


def get_db():
    engine = get_database_engine()
    with Session(engine) as session:
        yield session
