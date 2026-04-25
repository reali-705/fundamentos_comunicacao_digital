import plotly.graph_objects as go
from plotly.offline import plot, get_plotlyjs
from .funcoes import GerenciadorFuncoes


def montar_figura(dados: dict, meta: dict) -> go.Figure:
    fig = go.Figure()

    i = 0
    while f"y_{i}" in dados:
        fig.add_trace(
            go.Scatter(
                x=dados["x"],
                y=dados[f"y_{i}"],
                mode="lines",
                name=dados[f"nome_{i}"],
            )
        )
        i += 1

    fig.update_layout(
        title=meta["titulo"],
        template="plotly_white",
        height=520,
        legend_title_text="Curvas",
        margin=dict(l=60, r=30, t=70, b=50),
        xaxis_title="x",
        yaxis_title="y",
    )

    return fig


def criar_dashboard():
    gerenciador = GerenciadorFuncoes(pontos= 10000)

    formulas = {
        14: r"$f(x) = \sin(x) + x$",
        15: r"$f(x) = \sin(x)\cdot x$",
        16: r"$f(x) = (\sin(2x))^2$",
        17: r"$f(x) = \sin(2x) + 3 \quad \text{e} \quad g(x) = \sin(2x) - 3$",
        18: r"$f(x) = x^2 + 1 \quad \text{e} \quad g(x) = x^2 - 1$",
        19: r"$f(x) = \sin(2x)\cdot e^{0.5x}$",
        20: r"$f(x) = \dfrac{\sin(6x)}{\cos(6x)}$",
        21: r"$f(x) = \dfrac{\b^{x}}{b^{-x}}$",
    }

    html_final = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Visualização de Funções Matemáticas</title>

    <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }}
    }};
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <script type="text/javascript">
    {get_plotlyjs()}
    </script>

    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px;
            line-height: 1.6;
            background: #fff;
            color: #111;
        }}
        h1, h2 {{
            margin-bottom: 0.4rem;
        }}
        .bloco-funcao {{
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 12px;
            background: #fafafa;
        }}
        .descricao {{
            margin-bottom: 16px;
        }}
        .formula {{
            margin: 8px 0 18px 0;
            font-size: 1.05rem;
        }}
    </style>
</head>
<body>
    <h1>Visualização de Funções Matemáticas</h1>
    <p>Este documento reúne todas as funções da atividade 03 de fundamentos da matemática digital.
     Questões:
     17) Qual operação desloca:
            - a função para cima ou para baixo? (resposta: adição ou subtração de uma constante)
    
     18.1) Qual dos dois polinômios corresponde ao gráfico em azul:
            - f(x) = x² + 1
     18.2) Qual dos dois polinômios corresponde ao gráfico em vermelho:
            - g(x) = x² - 1
     21) QUe funções quando multiplicadas resultam em uma função constante? (resposta: e^(bx) e e^(-bx))
     
    
     
       </p>
"""

    for numero, _ in gerenciador.listar_funcoes():
        dados = gerenciador.gerar_dados_plotly(numero)
        meta = dados["metadados"]
        fig = montar_figura(dados, meta)

        grafico_html = plot(
            fig,
            output_type="div",
            include_plotlyjs=False,
        )

        formula = formulas.get(numero, "")

        html_final += f"""
    <section class="bloco-funcao">
        <h2>{meta["titulo"]}</h2>
        <p class="descricao">{meta["descricao"]}</p>
        <p class="formula">{formula}</p>
        {grafico_html}
    </section>
"""

    html_final += """
</body>
</html>
"""

    from pathlib import Path

    caminho_saida = Path("atividade03") / "atividade03.html"

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    print(f"Dashboard completo gerado: {caminho_saida}")


