from app.api.routers import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(
    router=router,
    prefix="/api",
    tags=["Tradutor Morse"],
)
