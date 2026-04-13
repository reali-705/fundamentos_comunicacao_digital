import flet as ft
from app.ui.components.widgets import criar_card_saida, criar_campo_entrada,frequencia_dropdown, criar_secao_telegrafista
from app.ui.components.botoes import setup_handlers

def build(page: ft.Page):
    texto_morse_saida = ft.Text("", size=25, weight=ft.FontWeight.BOLD)
    titulo = ft.Text("Conversor Texto-Morse", size=30, weight=ft.FontWeight.BOLD)
    campo_entrada = criar_campo_entrada()
    tipo_frequencia = frequencia_dropdown()
    telegrapista = criar_secao_telegrafista()
    on_convert = setup_handlers(page, campo_entrada, texto_morse_saida)
    # Retorno da UI principal
    return ft.Row(
        controls=[
            ft.Column(
                expand=1,
                controls=[
                    ft.Text("Conversor Texto-Morse", size=30, weight="bold"),
                    campo_entrada,
                    ft.ElevatedButton('CONVERTER PARA MORSE', style=ft.ButtonStyle(
                        bgcolor="#2c5d87", color="white", 
                        shape=ft.RoundedRectangleBorder(radius=10)), 
                        width=500, on_click=on_convert),
                    criar_card_saida(texto_morse_saida),
                    tipo_frequencia
                ],
                spacing=20
            ),
            telegrapista
        ],
        spacing=40
    )