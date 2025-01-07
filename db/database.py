from typing import Annotated

from contextlib import asynccontextmanager

from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends, FastAPI


sqlite_file_name = "database.db"

DATABASE_URL = f"sqlite:///{sqlite_file_name}"
engine = create_engine(DATABASE_URL, echo=True)


def drop_tables():
    SQLModel.metadata.drop_all(engine)


def create_db_and_tables():
    drop_tables()
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Логика при старте
    create_db_and_tables()
    print("Database initialized")

    yield  # Приложение работает
    drop_tables()
    print("Database dropped")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
