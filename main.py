import uvicorn
from fastapi import FastAPI

from app.routers.main_routers import main_app
from db.database import lifespan


app = FastAPI(title="Dividents Flow", lifespan=lifespan)

app.include_router(main_app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
