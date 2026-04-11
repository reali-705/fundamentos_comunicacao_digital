import re

from app.core.config import FREQUENCIA_PONTO, FREQUENCIA_TRACO, RECORDINGS_DIR
from pydantic import BaseModel, Field, field_validator


# --- Modelo Base para Requisições e Respostas ---
class BaseRequest(BaseModel):
    frequencia_ponto: int = Field(
        default=FREQUENCIA_PONTO,
        ge=400,
        le=2000,
        examples=[FREQUENCIA_PONTO],
        description="Frequência do ponto em Hz para a conversão do texto em código Morse (entre 400 e 2000 Hz)",
    )
    frequencia_traco: int = Field(
        default=FREQUENCIA_TRACO,
        ge=400,
        le=2000,
        examples=[FREQUENCIA_TRACO],
        description="Frequência do traco em Hz para a conversão do texto em código Morse (entre 400 e 2000 Hz)",
    )


class BaseResponse(BaseModel):
    codigo_morse: str = Field(
        default=...,
        examples=["... --- ...", "- . ... - .- -. -.. ---"],
        description="Código Morse extraído do arquivo de áudio",
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
