"""
RECEPTOR DE MORSE - Decodificador de Áudio para Texto

Módulo responsável por processar áudio contendo sinais Morse e convertê-lo
em texto legível. Implementa um pipeline de processamento de sinais que:

1. Filtra o áudio para a faixa de frequência do Morse (500-1000Hz)
2. Normaliza a amplitude do sinal com ganho automático
3. Detecta segmentos de som e silêncio através de análise de energia
4. Classifica os segmentos em pontos (.), traços (-) e espaços
5. Traduz o padrão Morse resultante em texto

Autor: Seu Nome
Data: 2026-04-12
Versão: 1.0
"""

import numpy as np
from scipy.signal import butter, filtfilt
from tradutor import morse_para_texto
from config import SAMPLE_RATE, FRAME_MS


def filtro_passa_banda_largo(audio, sr, low=500, high=1000):
    """
    Aplica filtro passa-banda para isolar a faixa de frequência do Morse.
    
    O Morse é tipicamente transmitido em frequências entre 500-1000 Hz.
    Este filtro remove ruído em frequências muito baixas (< 500Hz) e muito altas (> 1000Hz),
    mantendo o sinal de Morse e melhorando a razão sinal-ruído (SNR).
    
    Utiliza um filtro Butterworth de 4ª ordem com zero-phase filtering (filtfilt)
    para evitar distorção de fase no sinal.
    
    Args:
        audio (np.ndarray): Array de áudio com amostras de som
        sr (int): Taxa de amostragem em Hz (ex: 8000, 16000)
        low (int): Frequência baixa do filtro em Hz. Padrão: 500Hz
        high (int): Frequência alta do filtro em Hz. Padrão: 1000Hz
    
    Returns:
        np.ndarray: Array de áudio filtrado (mesmo tamanho da entrada)
    
    Processo:
        1. Calcula frequência de Nyquist (sr/2)
        2. Normaliza frequências de corte (divide por Nyquist)
        3. Projeta filtro Butterworth 4ª ordem
        4. Aplica filtro nos dois sentidos (forward-backward) para zero-phase
    
    Exemplo:
        >>> audio_filtrado = filtro_passa_banda_largo(audio, sr=8000, low=400, high=1200)
    """
    # Frequência de Nyquist é metade da taxa de amostragem
    nyq = 0.5 * sr
    
    # Normalizar frequências de corte dividindo pela frequência de Nyquist
    # Resultado: valores entre 0 e 1
    b, a = butter(4, [low/nyq, high/nyq], btype='band')
    
    # filtfilt: aplica o filtro duas vezes (forward e backward)
    # Benefício: cancela distorção de fase, mantém magnitude do sinal
    return filtfilt(b, a, audio)


def detectar_energia_melhorada(audio, sr=SAMPLE_RATE, frame_ms=FRAME_MS, sensibilidade=0.3):
    """
    Detecta presença de som através da análise de energia (RMS) do áudio.
    
    Divide o áudio em frames (janelas) de tempo fixo, calcula a energia RMS
    (Root Mean Square) de cada frame, e cria uma máscara booleana indicando
    quais frames contêm som (energia acima do limiar).
    
    O limiar é adaptativo: varia entre o mínimo e máximo de energia detectado,
    permitindo adaptação a diferentes níveis de ruído de fundo.
    
    Args:
        audio (np.ndarray): Array de áudio
        sr (int): Taxa de amostragem em Hz. Padrão: SAMPLE_RATE
        frame_ms (int): Duração de cada frame em milissegundos. Padrão: FRAME_MS
        sensibilidade (float): Fator de sensibilidade (0.0 a 1.0).
                              - 0.0: extremamente sensível (detecta tudo)
                              - 1.0: insensível (detecta apenas picos altos)
                              - 0.3: bom equilíbrio (recomendado)
    
    Returns:
        np.ndarray: Array booleano onde True = presença de som, False = silêncio
    
    Processo:
        1. Converte duração do frame de ms para número de amostras
        2. Divide áudio em frames consecutivos
        3. Calcula RMS (energia) para cada frame
        4. Encontra mínimo e máximo de energia
        5. Calcula limiar adaptativo: limiar = min + sensibilidade * (max - min)
        6. Cria máscara comparando energia com limiar
        7. Aplica filtro mediana para remover picos isolados
    
    Exemplo:
        >>> mascara = detectar_energia_melhorada(audio, sensibilidade=0.3)
        >>> num_frames_com_som = np.sum(mascara)
    
    Nota:
        O filtro mediana remove ruído impulsivo (clicks, pops) que poderia
        ser incorretamente detectado como segmentos de Morse.
    """
    # Converter milissegundos para número de amostras
    # Fórmula: (milissegundos / 1000) * taxa_amostragem
    frame_len = int(sr * frame_ms / 1000)
    hop = frame_len  # Avanço entre frames (sem sobreposição)
    
    # Lista para armazenar energia de cada frame
    energia = []
    
    # Iterar sobre o áudio em passos de frame_len
    for i in range(0, len(audio) - frame_len, hop):
        # Extrair frame (janela de áudio)
        frame = audio[i:i+frame_len]
        
        # Calcular RMS (Root Mean Square) - representa energia do frame
        # RMS = sqrt(média(amostra^2))
        rms = np.sqrt(np.mean(frame**2))
        energia.append(rms)
    
    # Converter lista para array numpy para operações eficientes
    energia = np.array(energia)
    
    # Calcular limiar adaptativo
    # Permite adaptação a diferentes níveis de ruído
    min_e = np.min(energia)  # Energia mínima (ruído de fundo)
    max_e = np.max(energia)  # Energia máxima (picos do sinal)
    
    # Limiar = mínimo + sensibilidade * (faixa de energia)
    # Com sensibilidade=0.3: limiar está a 30% do caminho entre mín e máx
    limiar = min_e + sensibilidade * (max_e - min_e)
    
    # Criar máscara: True onde energia > limiar (som), False onde < limiar (silêncio)
    mascara = energia > limiar
    
    # Aplicar filtro de mediana para remover picos isolados
    # kernel_size=5: verifica 5 valores consecutivos
    # Remove ruído impulsivo (spikes únicos que não representam som real)
    from scipy.signal import medfilt
    mascara = medfilt(mascara.astype(int), kernel_size=5).astype(bool)
    
    return mascara


def segmentar_morse_simples(audio, sr=SAMPLE_RATE, frame_ms=FRAME_MS, sensibilidade=0.3, duracao_min=30):
    """
    Agrupa frames consecutivos em segmentos de som e silêncio.
    
    Usa a máscara de detecção de energia para identificar mudanças entre
    som e silêncio, criando segmentos contínuos. Filtra segmentos muito
    curtos para eliminar ruído.
    
    Args:
        audio (np.ndarray): Array de áudio
        sr (int): Taxa de amostragem em Hz. Padrão: SAMPLE_RATE
        frame_ms (int): Duração de cada frame em ms. Padrão: FRAME_MS
        sensibilidade (float): Sensibilidade do detector (0.0-1.0). Padrão: 0.3
        duracao_min (int): Duração mínima de um segmento em ms.
                          Segmentos mais curtos são filtrados. Padrão: 30ms
    
    Returns:
        list: Lista de tuplas (estado, duração_ms) onde:
              - estado (bool): True = som, False = silêncio
              - duração_ms (int): Duração em milissegundos
    
    Processo:
        1. Detecta energia do áudio gerando máscara booleana
        2. Itera sobre a máscara, agrupando frames consecutivos com mesmo estado
        3. Quando muda o estado, cria um segmento com a duração acumulada
        4. Filtra segmentos com duração < duracao_min (remove ruído)
    
    Exemplo:
        >>> segmentos = segmentar_morse_simples(audio)
        >>> for eh_som, duracao in segmentos:
        >>>     tipo = "Som" if eh_som else "Silêncio"
        >>>     print(f"{tipo}: {duracao}ms")
    
    Nota:
        O parâmetro duracao_min é crítico para filtrar ruído:
        - duracao_min=20: detecta mais segmentos, mas pode ter falsos positivos
        - duracao_min=30: bom equilíbrio (padrão)
        - duracao_min=50: ignora mais ruído, mas pode perder segmentos válidos
    """
    # Detectar energia do áudio
    mascara = detectar_energia_melhorada(audio, sr, frame_ms, sensibilidade)
    
    # Validar se máscara não está vazia
    if len(mascara) == 0:
        return []
    
    # Lista para armazenar segmentos (estado, duração)
    segmentos = []
    
    # Estado inicial (primeiro frame)
    estado = mascara[0]  # True (som) ou False (silêncio)
    
    # Tempo acumulado para o segmento atual (em ms)
    tempo = frame_ms
    
    # Iterar sobre os frames a partir do segundo
    for i in range(1, len(mascara)):
        if mascara[i] == estado:
            # Mesmo estado: acumular tempo
            tempo += frame_ms
        else:
            # Mudança de estado: criar segmento
            # Mas apenas se duração >= duração mínima (filtro de ruído)
            if tempo >= duracao_min:
                segmentos.append((estado, tempo))
            
            # Iniciar novo segmento com novo estado
            estado = mascara[i]
            tempo = frame_ms
    
    # Não esquecer do último segmento
    if tempo >= duracao_min:
        segmentos.append((estado, tempo))
    
    return segmentos


def classificar_morse_robusto(segmentos, duracao_ponto=0.1):
    """
    Classifica segmentos em símbolos Morse (pontos, traços, espaços).
    
    Em Morse, os diferentes símbolos e espaços têm durações padronizadas:
    - Ponto (.): 1 unidade de tempo
    - Traço (-): 3 unidades de tempo
    - Espaço entre elementos (ignorado): 1 unidade
    - Espaço entre letras: 3 unidades
    - Espaço entre palavras (/): 7 unidades
    
    Esta função compara a duração de cada segmento com estes valores relativos
    para classificá-lo corretamente.
    
    Args:
        segmentos (list): Lista de tuplas (estado, duração_ms)
                         Obtido de segmentar_morse_simples()
        duracao_ponto (float): Duração do ponto em segundos.
                              Padrão: 0.1s (100ms)
                              Todos os outros valores são múltiplos deste.
    
    Returns:
        str: String com o padrão Morse detectado.
             Exemplo: ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
    
    Classificação:
        SOM (estado=True):
            - tempo_s <= 0.1 * 1.5 (150ms): Ponto (.)
            - tempo_s > 0.1 * 1.5: Traço (-)
        
        SILÊNCIO (estado=False):
            - tempo_s <= 0.1 * 2.0 (200ms): Ignorado (espaço dentro de letra)
            - tempo_s <= 0.1 * 5.0 (500ms): Espaço entre letras ( )
            - tempo_s > 0.1 * 5.0: Espaço entre palavras (/)
    
    Exemplo:
        >>> segmentos = [
        >>>     (True, 100),   # Som 100ms -> Ponto
        >>>     (False, 100),  # Silêncio 100ms -> Ignorado
        >>>     (True, 300),   # Som 300ms -> Traço
        >>>     (False, 400),  # Silêncio 400ms -> Espaço letra
        >>> ]
        >>> morse = classificar_morse_robusto(segmentos)
        >>> # Resultado: ".-"
    
    Nota:
        Os fatores multiplicadores (1.5, 2.0, 5.0) são baseados na
        padronização internacional de Morse e representam razões
        de duração entre diferentes símbolos.
    """
    # Lista para construir a string Morse
    resultado = []
    
    # Processar cada segmento
    for status, tempo_ms in segmentos:
        # Converter tempo de ms para segundos para comparação
        tempo_s = tempo_ms / 1000.0
        
        if status:  # SOM: classificar como ponto ou traço
            # Comparar duração com o limiar de 1.5x o ponto
            # Se <= 1.5x ponto -> ponto (.)
            # Se > 1.5x ponto -> traço (-)
            if tempo_s <= duracao_ponto * 1.5:
                resultado.append('.')
            else:
                resultado.append('-')
        
        else:  # SILÊNCIO: classificar tipo de espaço
            # Espaço muito curto (<=2x ponto): ignorar
            # (representa espaço entre elementos da mesma letra)
            if tempo_s <= duracao_ponto * 2.0:
                continue
            
            # Espaço médio (entre 2x e 5x ponto): espaço entre letras
            elif tempo_s <= duracao_ponto * 5.0:
                resultado.append(' ')
            
            # Espaço longo (>5x ponto): espaço entre palavras
            else:
                resultado.append('/')
    
    # Juntar lista em string única
    return ''.join(resultado)


def processar_audio_para_texto(audio, sensibilidade=0.35, duracao_ponto=0.1):
    """
    Pipeline completo: transforma áudio em Morse, depois em texto.
    
    Orquestra todo o processo de decodificação:
    1. Filtra áudio para faixa Morse (500-1000Hz)
    2. Aplica ganho automático se sinal está fraco
    3. Segmenta em blocos de som/silêncio
    4. Classifica blocos em símbolos Morse
    5. Traduz padrão Morse em texto legível
    
    Args:
        audio (np.ndarray): Array de áudio a processar
        sensibilidade (float): Sensibilidade do detector (0.0-1.0).
                              Padrão: 0.35 (bom equilíbrio)
        duracao_ponto (float): Duração esperada do ponto em segundos.
                              Padrão: 0.1s (100ms)
    
    Returns:
        str: Texto decodificado (ex: "HELLO WORLD")
    
    Etapas:
    
    1. FILTRAGEM (linha ~85)
       - Remove ruído fora da faixa 500-1000Hz
       - Melhora razão sinal-ruído (SNR)
    
    2. GANHO AUTOMÁTICO (linha ~88-92)
       - Verifica amplitude do sinal
       - Se muito fraco (pico < 0.05), aplica ganho
       - Normaliza para amplitude ~0.5
    
    3. SEGMENTAÇÃO (linha ~95)
       - Divide áudio em blocos de som/silêncio
       - Filtra ruído (segmentos muito curtos)
    
    4. CLASSIFICAÇÃO (linha ~98)
       - Compara duração de cada bloco
       - Classifica em pontos, traços, espaços
    
    5. TRADUÇÃO (linha ~102)
       - Converte padrão Morse em letras/palavras
       - Usa tabela de conversão de morse_para_texto()
    
    Exemplo:
        >>> import librosa
        >>> audio, sr = librosa.load("morse.wav", sr=8000)
        >>> texto = processar_audio_para_texto(audio)
        >>> print(f"Decodificado: {texto}")
        Decodificado: HELLO WORLD
    
    Prints de Debug:
        - Mostra fator de ganho aplicado (se necessário)
        - Mostra padrão Morse detectado antes da tradução
    """
    
    # ========== ETAPA 1: FILTRAGEM ==========
    # Aplica filtro passa-banda para isolar faixa de frequência do Morse
    # Remove ruído em frequências muito baixas (< 500Hz) e muito altas (> 1000Hz)
    audio_filtrado = filtro_passa_banda_largo(audio, SAMPLE_RATE)
    
    # ========== ETAPA 2: GANHO AUTOMÁTICO ==========
    # Normaliza sinal fraco para amplitude adequada
    pico = np.max(np.abs(audio_filtrado))
    
    # Se amplitude máxima está abaixo do limiar (0.05):
    # - Calcular fator de ganho necessário para atingir amplitude alvo (0.5)
    # - Aplicar ganho ao áudio
    # - Imprimir informação de debug
    if pico < 0.05:
        ganho = 0.5 / (pico + 1e-6)  # +1e-6 evita divisão por zero
        audio_filtrado *= ganho
        print(f"Ganho aplicado: {ganho:.2f}")
    
    # ========== ETAPA 3: SEGMENTAÇÃO ==========
    # Divide áudio em segmentos de som e silêncio
    # Remove ruído muito curto (< 30ms)
    segmentos = segmentar_morse_simples(audio_filtrado, sensibilidade=sensibilidade)
    
    # ========== ETAPA 4: CLASSIFICAÇÃO ==========
    # Classifica cada segmento em símbolo Morse
    # Compara duração com valores esperados de ponto/traço
    morse = classificar_morse_robusto(segmentos, duracao_ponto)
    print(f"Morse detectado: {morse}")
    
    # ========== ETAPA 5: TRADUÇÃO ==========
    # Converte padrão Morse em texto legível
    # Usa tabela de conversão internacional de Morse
    return morse_para_texto(morse)