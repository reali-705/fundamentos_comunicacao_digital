import flet as ft
from app.ui.components.widgets import criar_card_saida

def build(page: ft.Page):
    # Def somente para teste, enquanto não tem a API de conversão implementada
    texto_morse_saida = ft.Text("")
    def clicar_converter(e):
        if campo_entrada.value.strip().upper() == "SOS":    
            texto_morse_saida.value = "... --- ..."
        else:
            texto_morse_saida.value = "Texto não reconhecido"
        
        page.update()    

    titulo = ft.Text("Conversor Texto-Morse", size=30, weight=ft.FontWeight.BOLD)

    campo_entrada = ft.TextField(
        label="Texto de entrada", 
        hint_text="Digite seu texto aqui...", 
        multiline=True, 
        min_lines=3, 
        border_color="#2c5d87", 
        border_radius=10,
        width=500
    )

    botao_converter = ft.ElevatedButton(
        'CONVERTER PARA MORSE',
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#2c5d87", 
            shape=ft.RoundedRectangleBorder(radius=10)
        ), 
        width=500,
        on_click=clicar_converter
    )

    # Área interna do card de saída
    conteudo_interno_saida = ft.Column([
        ft.Row([
            ft.Text("Texto em Morse", size=12, weight="bold", color=ft.Colors.GREY_700),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=1, color=ft.Colors.GREY_300),
        ft.Container(
            content=texto_morse_saida,
            padding=10,
            width=500,
        )
    ])

    # Retorno da UI principal
    return ft.Row(
        controls=[
            # Coluna da Esquerda
            ft.Column(
                expand=1,
                controls=[
                    titulo,
                    campo_entrada,
                    botao_converter,
                    # Chama o widget customizado passando o conteúdo
                    criar_card_saida(texto_morse_saida)
                ],
                spacing=20
            ),
            # Coluna da Direita (Modo Telegrafista)
            ft.Column(
                expand=1,
                controls=[
                    ft.Text("Modo Telegrafista e Visualização de Áudio", size=30, weight="bold"),
                    ft.Text("O gráfico de ondas será implementado aqui.", color=ft.Colors.GREY_500)
                ]
            )
        ],
        spacing=40,
        vertical_alignment=ft.CrossAxisAlignment.START
    )