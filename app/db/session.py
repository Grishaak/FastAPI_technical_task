from sqlmodel import create_engine, Session
from sqlalchemy.engine import URL

DATABASE_URL = "postgresql://user:password@db:5432/dbname"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
