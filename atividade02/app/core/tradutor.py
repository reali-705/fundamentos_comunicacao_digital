"""Este arquivo é responsável por conter as funções de tradução entre texto e código Morse.
Ele utiliza o dicionário de mapeamento definido em config.py para realizar as conversões."""

from config import MORSE_MAP, REVERSE_MORSE_MAP


def texto_para_morse(text: str) -> str:
    """
    Converte texto simples para uma string em Morse.
    Usa espaço simples entre letras e '/' entre palavras.
    """
    palavras = text.upper().split(" ")
    resultado_morse = []

    for palavra in palavras:
        # Traduz cada letra da palavra
        letras_morse = [MORSE_MAP.get(char, "?") for char in palavra]
        # Junta as letras com espaço e adiciona à lista de palavras
        resultado_morse.append(" ".join(letras_morse))

    # Junta as palavras com a barra de separação
    return " / ".join(resultado_morse)


def morse_para_texto(morse: str) -> str:
    """
    Converte uma string em Morse para texto simples.
    Lida corretamente com '/' para espaços e múltiplos espaços entre letras.
    """
    if not morse or morse.strip() == "":
        return ""

    palavras_texto = []
    
    # 1. Divide a string em palavras usando a barra '/'
    palavras_morse = morse.split('/')

    for palavra_morse in palavras_morse:
        # 2. Divide cada palavra em letras usando o espaço
        # .strip() remove espaços extras nas extremidades
        # .split() sem argumentos lida com qualquer quantidade de espaços brancos
        letras_morse = palavra_morse.strip().split()
        
        letras_texto = [
            REVERSE_MORSE_MAP.get(letra, "?") for letra in letras_morse
        ]
        
        # Junta as letras para formar a palavra
        palavras_texto.append("".join(letras_texto))

    # 3. Junta as palavras com um espaço real entre elas
    return " ".join(palavras_texto).strip()