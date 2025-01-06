import logging
from typing import Annotated

from sqlmodel import create_engine, SQLModel, Session

from fastapi import Depends

from models import Stock, StockDividend # Importing the models to be created in the database


sqlite_file_name = "database.db"

DATABASE_URL =  f"sqlite:///{sqlite_file_name}"
engine = create_engine(DATABASE_URL, echo=True)


def drop_tables():
    SQLModel.metadata.drop_all(engine)

def create_db_and_tables():
    drop_tables()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]