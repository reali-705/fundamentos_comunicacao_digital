import numpy as np
from .funcoes_primitivas import seno, cosseno, linear, quadratica, exponencial

# ============================================================================
# CLASSE GERENCIADORA DE FUNÇÕES COMPOSTAS
# ============================================================================

class GerenciadorFuncoes:
    """
    Gerencia e calcula funções compostas para visualização.

    Mantém metadados sobre cada função (nome, descrição) e facilita
    a geração de gráficos HTML individuais via Plotly.
    """

    def __init__(self, x_min: float = -2 * np.pi, x_max: float = 2 * np.pi, pontos: int = 500):
        """
        Inicializa o gerenciador de funções.

        Args:
            x_min: Valor mínimo do intervalo (padrão: -2π)
            x_max: Valor máximo do intervalo (padrão: 2π)
            pontos: Número de pontos para discretizar (padrão: 500)
        """
        self.x_min = x_min
        self.x_max = x_max
        self.pontos = pontos
        self.x = np.linspace(x_min, x_max, pontos)

        # Registra todas as funções com metadados
        self._funcoes = self._registrar_funcoes()

    # ========================================================================
    # MÉTODOS DE CÁLCULO (funções compostas)
    # ========================================================================
    def _registrar_funcoes(self):
        return {
            14: {
                "nome": "Função 14",
                "titulo": "Composição Aditiva: sen(x) + x",
                "descricao": "Soma de uma função seno com a reta y = x",
                "funcao": self._funcao_14,
                "retorna_tupla": True,
                "componentes": ("sen(x)", "x", "sen(x) + x"),
            },
            15: {
                "nome": "Função 15",
                "titulo": "Composição Multiplicativa: sen(x) × x",
                "descricao": "Produto de uma função seno e uma função linear",
                "funcao": self._funcao_15,
                "retorna_tupla": True,
                "componentes": ("Seno", "Linear", "Produto"),
            },
            16: {
                "nome": "Função 16",
                "titulo": "Composição: sen(2x)² (seno ao quadrado)",
                "descricao": "Quadrática aplicada ao seno com amplitude 2 e frequência 2",
                "funcao": self._funcao_16,
                "retorna_tupla": True,
                "componentes": ("Base Seno", "Quadrática Base", "Composição"),
            },
            17: {
                "nome": "Função 17",
                "titulo": "Seno com Deslocamento Vertical",
                "descricao": "Seno deslocado para cima e para baixo (±3) com frequência 2",
                "funcao": self._funcao_17,
                "retorna_tupla": True,
                "componentes": ("Seno Deslocado (+3)", "Seno Deslocado (-3)"),
            },
            18: {
                "nome": "Função 18",
                "titulo": "Divisão de Parábolas: (x² + 1) / (x² - 1)",
                "descricao": "Divisão de duas funções quadráticas com assíntotas",
                "funcao": self._funcao_18,
                "retorna_tupla": True,
                "componentes": ("Numerador", "Denominador", "Divisão"),
            },
            19: {
                "nome": "Função 19",
                "titulo": "Composição Multiplicativa: sen(2x) × e^(0.5x)",
                "descricao": "Produto de seno com frequência 2 e função exponencial",
                "funcao": self._funcao_19,
                "retorna_tupla": True,
                "componentes": ("Seno", "Exponencial", "Produto"),
            },
            20: {
                "nome": "Função 20",
                "titulo": "Divisão Trigonométrica: sen(6x) / cos(6x) (tangente)",
                "descricao": "Razão entre seno e cosseno (função tangente)",
                "funcao": self._funcao_20,
                "retorna_tupla": True,
                "componentes": ("Seno", "Cosseno", "Tangente"),
            },
            21: {
                "nome": "Função 21",
                "titulo": "produto de exponenciais: e^(bx) * e^(-bx) (função constante)",
                "descricao": "Produto de uma função exponencial e sua inversa, resultando em uma função constante",
                "funcao": self._funcao_21,
                "retorna_tupla": True,
                "componentes": ("Exponencial", "Exponencial Inversa", "Produto"),
            },
        }
    
    @staticmethod
    def _funcao_14(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Seno + linear."""
        funcao_azul = seno(x)          
        funcao_vermelha = linear(x)    
        funcao_resultado = funcao_azul + funcao_vermelha

        return funcao_azul, funcao_vermelha, funcao_resultado

    @staticmethod
    def _funcao_15(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Seno × linear."""
        linha_azul = seno(x)
        linha_vermelha = linear(x)
        return linha_azul, linha_vermelha, linha_azul * linha_vermelha

    @staticmethod
    def _funcao_16(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Quadrática aplicada ao seno."""
        base_seno = seno(x, amplitude=2, frequencia=2)
        base_quadratica = quadratica(x)
        return base_seno, base_quadratica, quadratica(base_seno)

    @staticmethod
    def _funcao_17(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Seno com deslocamento vertical"""
        deslocamento = 3.0
        funcao_azul = seno(x, amplitude=1, frequencia=2)     + deslocamento
        funcao_vermelha = seno(x, amplitude=1, frequencia=2) - deslocamento
        return funcao_azul, funcao_vermelha

    @staticmethod
    def _funcao_18(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Divisão de parábolas conforme o slide 18."""
        funcao_azul = quadratica(x, a=1, b=0, c=1)
        
        funcao_vermelha = quadratica(x, a=1, b=0, c=-1)

 
        funcao_resultado = funcao_vermelha / funcao_azul

        return funcao_azul, funcao_vermelha, funcao_resultado

    @staticmethod
    def _funcao_19(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Seno × exponencial."""
        funcao_azul = seno(x, frequencia=2)
        funcao_vermelha = exponencial(x, a=1, b=0.5)
        return funcao_azul, funcao_vermelha, funcao_azul * funcao_vermelha

    @staticmethod
    def _funcao_20(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Seno / cosseno (tangente)"""

        funcao_azul = seno(x, frequencia=6)
        funcao_vermelha = cosseno(x, frequencia=6)

        with np.errstate(divide='ignore', invalid='ignore'):
            funcao_resultado = funcao_azul / funcao_vermelha

        funcao_resultado[np.abs(funcao_resultado) > 10] = np.nan

        return funcao_azul, funcao_vermelha, funcao_resultado

    @staticmethod
    def _funcao_21(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        exponencial / exponencial invertida (resultando em uma função constante)
        """
        base = 1.5
        
        funcao_azul = exponencial(x, a=1, b=base)
        funcao_vermelha = exponencial(-x, a=1, b=base)
        
        funcao_resultado = funcao_azul * funcao_vermelha 
        
        return funcao_azul, funcao_vermelha, funcao_resultado
    # ========================================================================
    # MÉTODOS DE ACESSO E METADADOS
    # ========================================================================

    def obter_funcao(self, numero: int) -> dict:
        """
        Obtém uma função específica com seus metadados.

        Args:
            numero: Número da função (14-21)

        Returns:
            Dicionário com 'nome', 'titulo', 'descricao', 'funcao' e 'retorna_tupla'

        Raises:
            ValueError: Se número não está no intervalo válido
        """
        if numero not in self._funcoes:
            raise ValueError(f"Função {numero} não existe. Válidas: 14-21")
        return self._funcoes[numero]

    def obter_todas(self) -> dict:
        """Retorna todas as funções registradas."""
        return self._funcoes

    def listar_funcoes(self) -> list[tuple[int, str]]:
        """Lista todas as funções disponíveis."""
        return [(num, info["nome"]) for num, info in sorted(self._funcoes.items())]

    def calcular(self, numero: int) -> np.ndarray | tuple[np.ndarray, ...]:
        """
        Calcula uma função específica.

        Args:
            numero: Número da função (14-21)

        Returns:
            Array ou tupla de arrays com os valores calculados
        """
        funcao_info = self.obter_funcao(numero)
        return funcao_info["funcao"](self.x)

    def gerar_dados_plotly(self, numero: int) -> dict:
        """
        Gera dados estruturados para plotagem Plotly.

        Args:
            numero: Número da função (14-21)

        Returns:
            Dicionário com 'x', dados das linhas e metadados
        """
        funcao_info = self.obter_funcao(numero)
        resultado = self.calcular(numero)

        dados = {
            "x": self.x,
            "metadados": {
                "numero": numero,
                "titulo": funcao_info["titulo"],
                "descricao": funcao_info["descricao"],
            }
        }

        # Trata resultado simples vs tupla
        if funcao_info["retorna_tupla"]:
            componentes = funcao_info.get("componentes", [])
            for i, (y_data, nome) in enumerate(zip(resultado, componentes)):
                dados[f"y_{i}"] = y_data
                dados[f"nome_{i}"] = nome
        else:
            dados["y"] = resultado
            dados["nome"] = funcao_info["nome"]

        return dados

