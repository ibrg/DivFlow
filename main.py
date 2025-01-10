import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.routers.main_routers import main_app
from db.connection import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()
    print("Shutting down the app")

app = FastAPI(title="Dividents Flow", lifespan=lifespan)

app.include_router(main_app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
