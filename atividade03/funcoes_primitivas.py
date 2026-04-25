# ============================================================================
# FUNÇÕES BÁSICAS (primitivas)
# ============================================================================
import numpy as np

def seno(
    x: np.ndarray,
    amplitude: float = 1.0,
    frequencia: float = 1.0,
    fase: float = 0.0
) -> np.ndarray:
    """
    Calcula a função seno com parâmetros customizáveis.

    Args:
        x: Array de valores de entrada
        amplitude: Amplitude da onda (padrão: 1.0)
        frequencia: Frequência da onda (padrão: 1.0)
        fase: Fase inicial da onda em radianos (padrão: 0.0)

    Returns:
        Array contendo os valores da função seno
    """
    return amplitude * np.sin(frequencia * x + fase)


def cosseno(
    x: np.ndarray,
    amplitude: float = 1.0,
    frequencia: float = 1.0,
    fase: float = 0.0
) -> np.ndarray:
    """
    Calcula a função cosseno com parâmetros customizáveis.

    Args:
        x: Array de valores de entrada
        amplitude: Amplitude da onda (padrão: 1.0)
        frequencia: Frequência da onda (padrão: 1.0)
        fase: Fase inicial da onda em radianos (padrão: 0.0)

    Returns:
        Array contendo os valores da função cosseno
    """
    return amplitude * np.cos(frequencia * x + fase)


def linear(
    x: np.ndarray,
    a: float = 1.0,
    b: float = 0.0
) -> np.ndarray:
    """
    Calcula a função linear (reta).

    Args:
        x: Array de valores de entrada
        a: Coeficiente angular (padrão: 1.0)
        b: Coeficiente linear (padrão: 0.0)

    Returns:
        Array contendo os valores da função linear (a*x + b)
    """
    return a * x + b


def quadratica(
    x: np.ndarray,
    a: float = 1.0,
    b: float = 0.0,
    c: float = 0.0
) -> np.ndarray:
    """
    Calcula a função quadrática (parábola).

    Args:
        x: Array de valores de entrada
        a: Coeficiente do termo quadrático (padrão: 1.0)
        b: Coeficiente do termo linear (padrão: 0.0)
        c: Termo constante (padrão: 0.0)

    Returns:
        Array contendo os valores da função quadrática (a*x² + b*x + c)
    """
    return a * x**2 + b * x + c


def exponencial(
    x: np.ndarray,
    a: float = 1.0,
    b: float = 1.0
) -> np.ndarray:
    """
    Calcula a função exponencial.

    Args:
        x: Array de valores de entrada
        a: Coeficiente multiplicador (padrão: 1.0)
        b: Expoente multiplicador (padrão: 1.0)

    Returns:
        Array contendo os valores da função exponencial (a * e^(b*x))
    """
    return a * np.exp(b * x)


def logaritma(
    x: np.ndarray,
    a: float = 1.0,
    b: float = np.e
) -> np.ndarray:
    """
    Calcula a função logarítmica.

    Args:
        x: Array de valores de entrada (deve ser positivo)
        a: Coeficiente multiplicador (padrão: 1.0)
        b: Base do logaritmo (padrão: e para logaritmo natural)

    Returns:
        Array contendo os valores da função logarítmica (a * log_b(x))

    Raises:
        ValueError: Se a base é <= 0 ou igual a 1
    """
    if b <= 0 or b == 1:
        raise ValueError("A base do logaritmo deve ser maior que 0 e diferente de 1.")
    return a * np.log(x) / np.log(b)
