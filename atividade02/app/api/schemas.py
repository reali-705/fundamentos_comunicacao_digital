import re
from datetime import datetime

from app.utils.utils import RECORDINGS_DIR
from pydantic import BaseModel, Field, field_validator


# --- Modelo Base para Requisições e Respostas ---
class BaseRequest(BaseModel):
    frequencia: int = Field(
        default=800,
        ge=400,
        le=2000,
        examples=[800, 1000, 1500],
        description="Frequência em Hz para a conversão do texto em código Morse (entre 400 e 2000 Hz)",
    )


class BaseResponse(BaseModel):
    codigo_morse: str = Field(
        default=...,
        examples=["... --- ...", "- . ... - .- -. -.. ---"],
        description="Código Morse extraído do arquivo de áudio",
    )
    id: int = Field(
        default=...,
        examples=[1, 2],
        description="Identificador único para a conversão realizada, útil para rastreamento no banco de dados ou para referência futura",
    )
    tempo_referencia: datetime = Field(
        default_factory=datetime.now,
        examples=["2026-04-10T19:30:00Z", "2026-04-14T15:30:00Z"],
        description="Timestamp da conversão realizada, útil para rastreamento no banco de dados ou para referência futura",
    )


# --- Modelos Específicos de entrada de Texto ---
class TextoParaMorseRequest(BaseRequest):
    texto_original: str = Field(
        default=...,
        min_length=1,
        examples=["SOS", "Testando"],
        description="Texto alfanumérico para ser convertido em código Morse",
    )

    @field_validator("texto_original")
    @classmethod
    def validar_texto_original(cls, valor: str) -> str:
        """
        Normaliza underscores e novas linhas para espaços e valida que o texto
        resultante contém apenas caracteres alfanuméricos e espaços.
        """
        valor_normalizado = valor.replace("_", " ").replace("\n", " ").strip()
        if not re.match(r"^[a-zA-Z0-9\s]+$", valor_normalizado):
            raise ValueError(
                "O texto original deve conter apenas caracteres alfanuméricos e espaços"
            )
        return valor_normalizado


class TextoParaMorseResponse(BaseResponse):
    caminho_audio: str = Field(
        default=...,
        examples=[
            str(RECORDINGS_DIR / "output" / "sos.wav"),
            str(RECORDINGS_DIR / "output" / "testando.wav"),
        ],
        description="Caminho para o arquivo de áudio gerado com a conversão do texto em código Morse",
    )
    duracao_total: float = Field(
        default=...,
        examples=[2.5, 3.0],
        description="Duração total do áudio gerado em segundos para barra de progresso no frontend",
        ge=0.1,
    )


# --- Modelos Específicos de entrada de Áudio ---
class SomParaTextoRequest(BaseRequest):
    caminho_audio: str = Field(
        default=...,
        examples=[
            str(RECORDINGS_DIR / "input" / "sos.wav"),
            str(RECORDINGS_DIR / "input" / "testando.wav"),
        ],
        description="Caminho para o arquivo de áudio contendo o código Morse a ser convertido em texto alfanumérico",
    )


class SomParaTextoResponse(BaseResponse):
    texto_convertido: str = Field(
        default=...,
        examples=["SOS", "Testando"],
        description="Texto alfanumérico resultante da conversão do código Morse presente no arquivo de áudio",
    )
