from app.api.schemas import (
    SomParaTextoResponse,
    TextoParaMorseRequest,
    TextoParaMorseResponse,
)
from app.core.config import SAMPLE_RATE
from app.core.emissor import morse_para_audio, salvar_audio
from app.core.recorder import RecorderManager
from app.core.tradutor import texto_para_morse
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
recorder = RecorderManager()


@router.post(
    path="/tradutor/texto-para-som",
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


@router.post(path="/iniciar-gravacao", status_code=status.HTTP_202_ACCEPTED)
async def iniciar_gravacao() -> dict[str, str]:
    """
    Endpoint para iniciar a gravação de áudio do microfone.
    O áudio será salvo em um arquivo WAV no diretório de gravações.
    """
    sucesso = recorder.start()
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A gravação já está em andamento.",
        )
    return {"message": "Gravação iniciada com sucesso."}


@router.post(
    path="/parar-gravacao",
    status_code=status.HTTP_200_OK,
    response_model=SomParaTextoResponse,
)
async def parar_gravacao() -> SomParaTextoResponse:
    """
    Endpoint para parar a gravação de áudio do microfone.
    O áudio gravado será processado para extrair o código Morse e convertê-lo em texto alfanumérico.
    """
    recorder.stop()

    # TODO: Lógica de tratamento do áudio

    return SomParaTextoResponse(
        codigo_morse="",
        texto_convertido="",
    )
