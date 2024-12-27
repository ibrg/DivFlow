import uvicorn

from fastapi import FastAPI

from routers.main_routers import main_app


app = FastAPI(name="DivFlow")
app.include_router(main_app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
