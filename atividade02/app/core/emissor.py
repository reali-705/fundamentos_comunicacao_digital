import numpy as np
from app.core.config import (
    AMPLITUDE,
    DURACAO_PONTO,
    DURACAO_TRACO,
    FREQUENCIA_PONTO,
    FREQUENCIA_TRACO,
    PAUSA_ESPACO_DIGITO_MORSE,
    PAUSA_ESPACO_LETRA,
    PAUSA_ESPACO_PALAVRA,
    RECORDINGS_DIR,
    SAMPLE_RATE,
)
from numpy.typing import NDArray
from scipy.io import wavfile


def morse_para_audio(
    morse: str,
    freq_ponto: int = FREQUENCIA_PONTO,
    freq_traco: int = FREQUENCIA_TRACO,
    duracao_ponto: float = DURACAO_PONTO,
    duracao_traco: float = DURACAO_TRACO,
    pausa_digito: float = PAUSA_ESPACO_DIGITO_MORSE,
    pausa_letra: float = PAUSA_ESPACO_LETRA,
    pausa_palavra: float = PAUSA_ESPACO_PALAVRA,
    sample_rate: int = SAMPLE_RATE,
) -> NDArray[np.floating]:
    """
    Converte Morse em áudio usando as definições do config.py como padrão.
    """

    # 1: Construção do domínio do tempo
    t_ponto = np.linspace(
        0, duracao_ponto, int(sample_rate * duracao_ponto), endpoint=False
    )
    t_traco = np.linspace(
        0, duracao_traco, int(sample_rate * duracao_traco), endpoint=False
    )

    # 2: Geração dos sons para ponto e traço
    som_ponto = AMPLITUDE * np.sin(2 * np.pi * freq_ponto * t_ponto)
    som_traco = AMPLITUDE * np.sin(2 * np.pi * freq_traco * t_traco)

    # 3: Construção do domínio do tempo para os silêncios
    num_amostras_digito = int(pausa_digito * sample_rate)
    num_amostras_letra = int(pausa_letra * sample_rate)
    num_amostras_palavra = int(pausa_palavra * sample_rate)

    # 4: Geração de silêncios
    silencio_digito = np.zeros(num_amostras_digito, dtype=np.float32)
    silencio_letra = np.zeros(num_amostras_letra, dtype=np.float32)
    silencio_palavra = np.zeros(num_amostras_palavra, dtype=np.float32)

    # 5: Buffer e Loop
    audio_final: list[NDArray[np.floating]] = []

    for simbolo in morse:
        match simbolo:
            case ".":
                audio_final.append(som_ponto)
                audio_final.append(silencio_digito)
            case "-":
                audio_final.append(som_traco)
                audio_final.append(silencio_digito)
            case " ":
                audio_final.append(silencio_letra)
            case "/":
                audio_final.append(silencio_palavra)
            case _:
                print(f"Aviso: Símbolo inválido ignorado: '{simbolo}'")

    # Prevenção de erro: se a string for vazia, retorna array vazio
    if len(audio_final) == 0:
        return np.array([])

    return np.concatenate(audio_final)


def salvar_audio(
    audio: NDArray[np.floating], filename: str, sample_rate: int = SAMPLE_RATE
) -> str:
    """Salva o array de áudio em um arquivo WAV."""

    # Constrói o caminho completo para o arquivo de saída, garantindo que a pasta exista
    caminho_completo = RECORDINGS_DIR / filename
    caminho_completo.parent.mkdir(parents=True, exist_ok=True)

    audio32: NDArray[np.float32] = np.asarray(audio, dtype=np.float32)

    # O astype(np.float32) é essencial para o arquivo WAV entender a amplitude de 0.5
    try:
        wavfile.write(caminho_completo, sample_rate, audio32)  # type: ignore
        print(f"Sucesso! Áudio salvo como: {filename}")
    except Exception as e:
        print(f"Erro ao salvar áudio: {e}")

    return str(caminho_completo)
