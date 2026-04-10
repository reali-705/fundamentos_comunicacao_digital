from app.api.schemas import (
    SomParaTextoRequest,
    SomParaTextoResponse,
    TextoParaMorseRequest,
    TextoParaMorseResponse,
)
from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    path="/texto-para-som",
    status_code=status.HTTP_201_CREATED,
    response_model=TextoParaMorseResponse,
    summary="Converter texto alfanumérico em código Morse e gerar áudio",
)
async def texto_para_som(request: TextoParaMorseRequest) -> TextoParaMorseResponse:
    """
    Endpoint para converter um texto alfanumérico em código Morse e gerar um arquivo de áudio correspondente.
    O usuário deve fornecer o texto a ser convertido e a frequência desejada para a conversão.
    """

    # TODO: Lógica de conversão do texto para código Morse e geração do áudio

    return TextoParaMorseResponse(
        codigo_morse="",
        id=0,
        caminho_audio="./data/recordings/output/*.wav",
        duracao_total=0.0,
    )


@router.post(
    path="/som-para-texto",
    status_code=status.HTTP_201_CREATED,
    response_model=SomParaTextoResponse,
    summary="Converter áudio contendo código Morse em texto alfanumérico",
)
async def som_para_texto(request: SomParaTextoRequest) -> SomParaTextoResponse:
    """'
    Endpoint para converter um arquivo de áudio contendo código Morse em texto alfanumérico.
    O usuário deve fornecer o caminho para o arquivo de áudio a ser convertido e a frequência utilizada na gravação.
    """

    # TODO: Lógica de conversão do áudio para texto alfanumérico

    return SomParaTextoResponse(
        codigo_morse="",
        id=0,
        texto_convertido="",
    )
