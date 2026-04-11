from app.api.schemas import (
    SomParaTextoRequest,
    SomParaTextoResponse,
    TextoParaMorseRequest,
    TextoParaMorseResponse,
)
from app.core.tradutor import texto_para_morse
from app.utils.utils import RECORDINGS_DIR
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

    # TODO: Salvar o código Morse gerado no banco de dados
    # TODO: Gerar o arquivo de áudio e calcular a duração total da gravação
    # TODO: Gerar o caminho para o arquivo de áudio

    return TextoParaMorseResponse(
        codigo_morse=codigo_morse_gerado,
        # TODO: Substituir o ID de teste por um ID real gerado pelo banco de dados
        id=0,
        # TODO: Gerar o arquivo de áudio e adicioná-lo ao caminho correto para o frontend acessar
        caminho_audio=str(RECORDINGS_DIR / "output.wav"),
        # TODO: Substituir a duração total de teste pelo valor real calculado durante a geração do áudio
        duracao_total=0.1,
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
        id=0,
        texto_convertido="",
    )
