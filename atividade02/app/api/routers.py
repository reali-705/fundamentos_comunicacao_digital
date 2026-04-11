from app.api.schemas import (
    SomParaTextoRequest,
    SomParaTextoResponse,
    TextoParaMorseRequest,
    TextoParaMorseResponse,
)
from app.core.config import SAMPLE_RATE
from app.core.emissor import morse_para_audio, salvar_audio
from app.core.tradutor import texto_para_morse
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

    # Teste de integração com o Frontend(Flet)
    texto_recebido = request.texto_original
    print(f"[DEBUG] Texto recebido para conversão: '{texto_recebido}'")

    codigo_morse_gerado = texto_para_morse(texto_recebido)

    audio = morse_para_audio(
        morse=codigo_morse_gerado,
        freq_ponto=request.frequencia_ponto,
        freq_traco=request.frequencia_traco,
    )

    caminho_audio = salvar_audio(audio, filename="output.wav")

    duracao_total = len(audio) / SAMPLE_RATE

    return TextoParaMorseResponse(
        codigo_morse=codigo_morse_gerado,
        caminho_audio=caminho_audio,
        duracao_total=duracao_total,
    )


@router.post(
    path="/som-para-texto",
    status_code=status.HTTP_201_CREATED,
    response_model=SomParaTextoResponse,
    summary="Converter áudio contendo código Morse em texto alfanumérico",
)
async def som_para_texto(request: SomParaTextoRequest) -> SomParaTextoResponse:
    """
    Endpoint para converter um arquivo de áudio contendo código Morse em texto alfanumérico.
    O usuário deve fornecer o caminho para o arquivo de áudio a ser convertido e a frequência utilizada na gravação.
    """

    # TODO: Lógica de conversão do áudio para texto alfanumérico

    return SomParaTextoResponse(
        codigo_morse="",
        texto_convertido="",
    )
