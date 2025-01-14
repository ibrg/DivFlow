import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

from main import app
from db.connection import get_session

# Создание тестовой базы данных
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)


# Переопределение зависимости `get_session` для использования тестовой базы
def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


# Фикстура для подготовки тестовой базы данных
@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    SQLModel.metadata.create_all(engine)  # Создаём таблицы перед тестом
    yield
    SQLModel.metadata.drop_all(engine)  # Удаляем таблицы после теста


# Фикстура для клиента тестового приложения
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
