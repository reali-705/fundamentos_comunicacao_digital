import flet as ft
import os
import time
from app.ui.components.api_cliente import converter_texto_para_morse

# Este arquivo é destinado a conter funções relacionadas a botões e seus handlers, para manter a lógica de eventos separada dos componentes visuais.
def setup_handlers(page, campo_entrada, texto_morse_saida, tipo_frequencia, audio_controle):
    async def clicar_converter(e):
        base_url = "http://127.0.0.1:8000"
        texto_entrada = campo_entrada.value
        if not texto_entrada:
            texto_morse_saida.value = "Por favor, insira um texto para converter."
            texto_morse_saida.color = ft.Colors.RED
            page.update()
            return

        try:
            freq = int(tipo_frequencia.value)
            resultado = converter_texto_para_morse(texto_entrada, frequencia=freq)
            texto_morse_saida.value = resultado.get("codigo_morse")

            caminho_audio = resultado.get("caminho_audio")
            print(caminho_audio)
            audio_controle.src = f"{base_url}{caminho_audio}?t={int(time.time())}"
            print(caminho_audio)
            page.update()
            time.sleep(0.1)
            await audio_controle.play()
        except Exception as ex:
            texto_morse_saida.value = f"Erro: {str(ex)}"    
        page.update()
    
    return clicar_converter