from app.api.routers import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import RECORDINGS_DIR

app = FastAPI()

# Isso permite acessar os arquivos via http://127.0.0.1:8000/audios/nome_do_arquivo.wav
app.mount("/audios", StaticFiles(directory=str(RECORDINGS_DIR)), name="audios")

app.include_router(
    router=router,
    prefix="/api",
    tags=["Tradutor Morse"],
)
