import numpy as np
from audio_services import GravadorAudio
from receptor import processar_audio_para_texto
from config import DURACAO_PONTO

def main():
    # 1. Inicialização
    gravador = GravadorAudio()
    
    print("\n--- DISPOSITIVOS DETECTADOS ---")
    dispositivos = gravador.listar_dispositivos()
    for d in dispositivos:
        print(f"ID: {d['id']} | Nome: {d['nome']} | SR Padrão: {d['default_sr']}Hz")
    
    escolha = input("\nDigite o ID do microfone (ou pressione ENTER para o padrão): ").strip()
    idx = int(escolha) if escolha.isdigit() else None
    
    # Configura o dispositivo selecionado
    config_status = gravador.configurar_dispositivo(idx)
    print(f"-> {config_status['message']}")

    # 3. Gravação
    input("\n[TESTE] Pressione ENTER para começar a gravar...")
    gravador.iniciar_gravacao()
    
    input("[GRAVANDO] Emita o som ou aproxime o áudio. ENTER para parar.")
    audio_bruto = gravador.parar_gravacao()
    
    if audio_bruto.size == 0:
        print("❌ Erro: Nenhum áudio capturado.")
        return

    # 4. Salvamento e Diagnóstico
    # Salvamos o bruto para referência
    gravador.salvar_audio(audio_bruto, "captura_bruta.wav")
    
    # Geramos e salvamos a versão limpa usando o método da classe
    # Isso ajuda a validar se o filtro (500-1000Hz) está correto para o seu som
    audio_limpo = gravador.pre_processar(audio_bruto)
    gravador.salvar_audio(audio_limpo, "captura_processada.wav")
    
    # 5. Decodificação
    print("\n--- Iniciando Decodificação Morse ---")
    
    # Dica: sensibilidade de 0.3 a 0.4 costuma ser ideal para áudio de celular
    # Ajustamos duracao_ponto conforme o seu config.py
    texto = processar_audio_para_texto(
        audio_bruto, 
        sensibilidade=0.35, 
        duracao_ponto=DURACAO_PONTO
    )
    
    print("-" * 30)
    print(f"📝 TEXTO TRADUZIDO: {texto}")
    print("-" * 30)

if __name__ == "__main__":
    main()