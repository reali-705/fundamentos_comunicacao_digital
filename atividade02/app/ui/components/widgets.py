import flet as ft
from app.ui.components.botoes import setup_handlers

# Este arquivo é destinado a conter componentes reutilizáveis para a interface, como cards, botões personalizados, etc.
def criar_card_saida(texto_controle):
    return ft.Container(
        content=ft.Column([
            ft.Text("TRADUÇÃO"),
            ft.Container(content=texto_controle, padding=10, width=500, height=200)
        ]),
        bgcolor="#f0f4f8",
        border_radius=10,
        padding=10
    )
# Função para criar um campo de entrada de texto personalizado
def criar_campo_entrada():
    return ft.TextField(
        label="Texto de entrada", 
        hint_text="Digite seu texto aqui...", 
        multiline=True, 
        min_lines=3, 
        border_color="#2c5d87", 
        border_radius=10,
        width=500
    )

# Função para criar um campo de saída de texto personalizado
def criar_campo_saida(texto_morse_saida):
    return ft.Column([
        ft.Row([
            ft.Text("", size=12, weight="bold", color=ft.Colors.GREY_700),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=1, color=ft.Colors.GREY_300),
        ft.Container(
            content= texto_morse_saida,
            padding=10,
            width=500,
            
        )
    ])

# Função para criar um botão que faz a conversão do texto para Morse, com estilo personalizado
def criar_botao_converter(clicar_converter):
    return ft.ElevatedButton(
        'CONVERTER PARA MORSE',
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#2c5d87", 
            shape=ft.RoundedRectangleBorder(radius=10)
        ), 
        width=500,
        on_click=clicar_converter
    )

# Função para criar um dropdown de seleção de frequência, com opções pré-definidas
def frequencia_dropdown():
    return ft.Dropdown(
        label="Frequência (Hz)",
        value="800",
        options=[
            ft.dropdown.Option("200"),
            ft.dropdown.Option("400"),
            ft.dropdown.Option("800"),
            ft.dropdown.Option("1000"),
            ft.dropdown.Option("1500"),
            ft.dropdown.Option("2000"),
        ],
        width=150,
        
    )

'''Função para criar a seção de telegrafista, que inclui um gráfico 
de ondas de áudio e botões para baixar o áudio e copiar o Morse'''
import flet as ft

def criar_secao_telegrafista(btn_gravacao, status_text):
    return ft.Column(
        controls=[
            ft.Text("Modo Telegrafista e Visualização de Áudio", size=30, weight="bold"),
            # Exibição do Status de Gravação acima do gráfico
            status_text, 
            ft.Container(
                content=ft.Column([
                    ft.Text("Gráfico de Ondas de Áudio", weight="bold", color=ft.Colors.GREY_500),
                    # O botão de gravação fica centralizado dentro do container ou logo abaixo
                    btn_gravacao
                ]),
                bgcolor="#f0f4f8",
                padding=20,
                border_radius=10,
                height=500,
                width=600,
            ),
            ft.Row([
                ft.Button("Baixar Áudio"),
                ft.Button("Copiar Morse"),
            ], spacing=10)
        ],
        spacing=15
    )