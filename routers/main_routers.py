from fastapi.routing import APIRouter

main_app = APIRouter()


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


@main_app.get("/status")
def status_check():
    return {"status": "ok"}
