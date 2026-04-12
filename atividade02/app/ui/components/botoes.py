import flet as ft
from app.ui.components.api_cliente import converter_texto_para_morse

# Este arquivo é destinado a conter funções relacionadas a botões e seus handlers, para manter a lógica de eventos separada dos componentes visuais.
def setup_handlers(page, campo_entrada, texto_morse_saida):
    def clicar_converter(e):
        texto_entrada = campo_entrada.value
        if not texto_entrada:
            texto_morse_saida.value = "Por favor, insira um texto para converter."
            texto_morse_saida.color = ft.Colors.RED
            page.update()
            return

        try:
            resultado = converter_texto_para_morse(texto_entrada)
            texto_morse_saida.value = resultado.get("codigo_morse")
        except Exception as ex:
            texto_morse_saida.value = f"Erro: {str(ex)}"    
        page.update()
    
    return clicar_converter