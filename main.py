import uvicorn
from fastapi import FastAPI

from routers.main_routers import main_app

from db.database import create_db_and_tables

app = FastAPI(title="Dividents Flow")

app.include_router(main_app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
