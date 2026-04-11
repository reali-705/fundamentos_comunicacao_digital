"""Este arquivo é responsável por conter as funções de tradução entre texto e código Morse.
Ele utiliza o dicionário de mapeamento definido em config.py para realizar as conversões."""

import config as config


def texto_para_morse(text: str) -> str:
    """Converte texto simples para uma string em Morse."""

    # Converte cada caractere para Morse, usando '?' para caracteres desconhecidos
    return " ".join(config.MORSE_MAP.get(char, "?") for char in text.upper())


def morse_para_texto(morse: str) -> str:
    """Converte uma string em Morse para texto simples."""

    return "".join(
        config.REVERSE_MORSE_MAP.get(letra_morse, "?")
        for letra_morse in morse.split(" ")
    )
