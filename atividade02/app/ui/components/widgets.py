import flet as ft

# Este arquivo é destinado a conter componentes reutilizáveis para a interface, como cards, botões personalizados, etc.
def criar_card_saida(texto_controle):
    return ft.Container(
        content=ft.Column([
            ft.Text("TRADUÇÃO"),
            ft.Container(content=texto_controle, padding=10, width=500, height=150)
        ]),
        bgcolor="#f0f4f8",
        border_radius=10,
        padding=10
    )