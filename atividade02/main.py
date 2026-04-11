import flet as ft
from app.ui.main_ui import build
def main(page: ft.Page):
    page.title = "SIMULADOR DE CÓDIGO MORSE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1100
    page.window_height = 700
    layout = build(page)
    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)
