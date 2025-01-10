from typing import Annotated

from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends

from env import SQLITE_DB

if not SQLITE_DB:
    raise ValueError("SQLITE_DB is not set in the environment variables.")
engine = create_engine(SQLITE_DB, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
    print(SQLModel.metadata.tables.keys())


def close_db():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
