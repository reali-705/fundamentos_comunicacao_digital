"""
RECEPTOR DE MORSE - Decodificador de Áudio para Texto

Módulo responsável pela decodificação de sinais Morse a partir de áudio
pré-processado. Implementa o pipeline de decodificação em 4 etapas:

    1. Detecção de energia  → máscara booleana (som/silêncio)
    2. Segmentação          → lista de segmentos (tipo, duração)
    3. Classificação        → string Morse (".-. ...")
    4. Tradução             → texto legível ("RS")

Para pré-processamento do áudio (filtro e ganho), use audio_services.py.
"""

import numpy as np
from scipy.signal import medfilt
from numpy.typing import NDArray
from tradutor import morse_para_texto
from audio_services import GravadorAudio
from config import SAMPLE_RATE, FRAME_MS, DURACAO_PONTO

# Alias de tipo para legibilidade
Segmentos = list[tuple[bool, int]]  # [(eh_som, duracao_ms), ...]


# ── ETAPA 1: DETECÇÃO DE ENERGIA ──────────────────────────────────────────────
def detectar_energia(
    audio: NDArray[np.floating],
    sample_rate: int = SAMPLE_RATE,
    frame_ms: int = FRAME_MS,
    sensibilidade: float = 0.3,
) -> NDArray[np.bool_]:
    """
    Divide o áudio em janelas e retorna máscara booleana de som/silêncio.

    Calcula o RMS de cada janela e compara com threshold adaptativo:
        threshold = min_rms + sensibilidade × (max_rms - min_rms)

    Aplica filtro de mediana (kernel=5) para remover spikes isolados
    que representam ruído impulsivo, não Morse real.

    Args:
        audio: Array de áudio pré-processado
        sample_rate: Taxa de amostragem em Hz
        frame_ms: Duração de cada janela em ms
        sensibilidade: Fator do threshold adaptativo (0.0 a 1.0)
                       - 0.0 → detecta tudo, inclusive ruído
                       - 1.0 → só detecta picos muito altos
                       - 0.3 → bom equilíbrio (recomendado)

    Returns:
        Array booleano — True = som, False = silêncio
    """
    frame_size = int(sample_rate * frame_ms / 1000)
    frames = [
        audio[i : i + frame_size]
        for i in range(0, len(audio) - frame_size, frame_size)
    ]

    if not frames:
        return np.array([], dtype=bool)

    rms = np.array([np.sqrt(np.mean(f ** 2)) for f in frames])
    threshold = rms.min() + sensibilidade * (rms.max() - rms.min())
    mascara = rms > threshold

    # Remove ruído impulsivo: spikes de 1-2 frames isolados
    mascara = medfilt(mascara.astype(int), kernel_size=5).astype(bool)

    return mascara


# ── ETAPA 2: SEGMENTAÇÃO ──────────────────────────────────────────────────────
'''
Agrupa frames consecutivos do mesmo tipo (som ou silêncio) em segmentos. Cada segmento é representado por uma tupla (eh_som, duracao_ms).
Filtra segmentos com duração menor que duracao_min_ms para eliminar fragmentos de ruído que passaram pela detecção de energia. O valor recomendado para duracao_min_ms é 30ms, mas pode ser ajustado conforme a qualidade do áudio e a sensibilidade desejada.
Args:
    mascara: Array booleano da detecção de energia (True = som, False = silêncio)
    frame_ms: Duração de cada frame em milissegundos
    duracao_min_ms: Duração mínima para um segmento ser considerado válido. 
                    - 20ms: mais sensível, pode incluir mais ruído
                    - 30ms: bom equilíbrio (recomendado)
                    - 50ms: mais conservador, pode perder pontos curtos'''
def segmentar_morse(
    mascara: NDArray[np.bool_],
    frame_ms: int = FRAME_MS,
    duracao_min_ms: int = 30,
) -> Segmentos:
    """
    Agrupa frames consecutivos do mesmo tipo em segmentos.

    Filtra segmentos com duração < duracao_min_ms para eliminar
    fragmentos de ruído que passaram pela detecção de energia.

    Args:
        mascara: Array booleano da detecção de energia
        frame_ms: Duração de cada frame em ms
        duracao_min_ms: Duração mínima para um segmento ser válido.
                        - 20ms: mais sensível, mais falsos positivos
                        - 30ms: bom equilíbrio (padrão)
                        - 50ms: mais conservador, pode perder pontos

    Returns:
        Lista de tuplas (eh_som, duracao_ms)
    """
    if len(mascara) == 0:
        return []

    segmentos: Segmentos = []
    status_atual = mascara[0]
    tempo_ms = frame_ms

    for i in range(1, len(mascara)):
        if mascara[i] == status_atual:
            tempo_ms += frame_ms
        else:
            if tempo_ms >= duracao_min_ms:
                segmentos.append((bool(status_atual), tempo_ms))
            status_atual = mascara[i]
            tempo_ms = frame_ms

    # Último segmento
    if tempo_ms >= duracao_min_ms:
        segmentos.append((bool(status_atual), tempo_ms))

    return segmentos


# ── ETAPA 3: CLASSIFICAÇÃO ────────────────────────────────────────────────────
def classificar_morse(
    segmentos: Segmentos,
    duracao_ponto: float = DURACAO_PONTO,
) -> str:
    resultado = []

    for status, tempo_ms in segmentos:
        tempo_s = tempo_ms / 1000.0

        if status:  # SOM
            # Aumentamos para 2.0x. Se o ponto "esticar" por causa do eco, 
            # ele ainda será lido como ponto.
            resultado.append('.' if tempo_s <= duracao_ponto * 2.0 else '-')
        else:       # SILÊNCIO
            # Se o silêncio for curto (até 2.5x o ponto), é apenas a pausa entre bipes
            if tempo_s <= duracao_ponto * 2.5:
                pass
            # Se for médio (até 6.0x), é o espaço entre letras
            elif tempo_s <= duracao_ponto * 6.0:
                resultado.append(' ')
            # Acima disso, é espaço entre palavras
            else:
                resultado.append('/')

    return ''.join(resultado)


# ── PIPELINE PRINCIPAL ────────────────────────────────────────────────────────
def processar_audio_para_texto(
    audio: NDArray[np.floating],
    sensibilidade: float = 0.35,
    duracao_ponto: float = DURACAO_PONTO,
) -> str:
    """
    Pipeline completo: áudio bruto → texto legível.

        1. Pré-processamento  (GravadorAudio) → filtra + normaliza
        2. Detecção de energia              → máscara booleana
        3. Segmentação                      → lista de segmentos
        4. Classificação                    → string Morse
        5. Tradução                         → texto

    Args:
        audio: Array de áudio bruto do microfone
        sensibilidade: Sensibilidade do detector de energia (0.0-1.0)
        duracao_ponto: Duração esperada do ponto em segundos

    Returns:
        Texto decodificado — ex: "SOS"
    """
    gravador = GravadorAudio()
    audio_limpo = gravador.pre_processar(audio)
    
    mascara     = detectar_energia(audio_limpo, sensibilidade=sensibilidade)
    segmentos   = segmentar_morse(mascara)
    morse       = classificar_morse(segmentos, duracao_ponto)

    print(f"[morse detectado] {morse}")
    return morse_para_texto(morse)