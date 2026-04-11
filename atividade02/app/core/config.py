'''Este arquivo é responsável por configurar as variáveis de ambiente e outras configurações do projeto. '''
from pathlib import Path

ATIVIDADE02_DIR = Path(__file__).resolve().parent.parent
RECORDINGS_DIR = ATIVIDADE02_DIR / "data" / "recordings"

MORSE_MAP = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",
    "E": ".",     "F": "..-.",  "G": "--.",   "H": "....",
    "I": "..",    "J": ".---",  "K": "-.-",   "L": ".-..",
    "M": "--",    "N": "-.",    "O": "---",   "P": ".--.",
    "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",
    "Y": "-.--",  "Z": "--..",
    
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",
    
    " ": "/"  # Espaço no texto é representado por "/" no código Morse
}

# Dicionário reverso 
REVERSE_MORSE_MAP = {v: k for k, v in MORSE_MAP.items()}
"""
Configurações Globais do Tradutor Morse
---------------------------------------
Este arquivo concentra todos os parâmetros físicos (som) e rítmicos (tempo) 
usados na geração de áudio do Código Morse. As proporções de tempo seguem 
o padrão internacional da ITU (International Telecommunication Union).
"""

# ==========================================
# 1. FREQUÊNCIAS TONAIS (O "Tom" do bipe)
# ==========================================
# Medidas em Hertz (Hz). Valores entre 600Hz e 800Hz são os mais confortáveis 
# e tradicionais para radiotelegrafia.
FREQUENCIA_PONTO = 700  # Frequência ligeiramente mais aguda para o ponto.
FREQUENCIA_TRACO = 600  # Frequência ligeiramente mais grave para o traço, ajudando na distinção.

# ==========================================
# 2. TEMPO E RITMO (Padrão Internacional)
# ==========================================
# A unidade básica de tempo do Código Morse é a duração de um "Ponto".
# Todos os outros sinais e silêncios são múltiplos matemáticos desse valor.
DURACAO_PONTO = 0.1  # Duração base (em segundos). Determina a velocidade geral (WPM).

# Durações de som:
DURACAO_TRACO = DURACAO_PONTO * 3  # Regra: Um traço tem a duração de 3 pontos.

# Durações de silêncio (Pausas):
PAUSA_ESPACO_DIGITO_MORSE = DURACAO_PONTO      # Regra: Silêncio entre bipes da mesma letra (1 ponto).
PAUSA_ESPACO_LETRA        = DURACAO_PONTO * 3  # Regra: Silêncio entre letras de uma palavra (3 pontos).
PAUSA_ESPACO_PALAVRA      = DURACAO_PONTO * 7  # Regra: Silêncio entre palavras diferentes (7 pontos).

# ==========================================
# 3. PROPRIEDADES DO ÁUDIO DIGITAL
# ==========================================
# Limite máximo de volume. Vai de 0.0 a 1.0. 
# Usamos 0.5 (50%) para deixar uma margem de segurança (headroom) 
# e evitar distorção (clipping) nos fones de ouvido.
AMPLITUDE = 0.5      

# Taxa de Amostragem (Sample Rate). Quantos "pontos" o computador desenha por segundo.
# 44100 Hz é o padrão comercial de CDs, garantindo alta fidelidade sem arquivos gigantes.
SAMPLE_RATE = 44100