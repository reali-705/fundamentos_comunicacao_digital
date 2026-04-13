from audio_services import GravadorAudio
from receptor import processar_audio_para_texto  
import datetime

def main():
    grav = GravadorAudio()
    grav.escolher_dispositivo_interativamente()
    input("Pressione ENTER para gravar...")
    grav.iniciar_gravacao()
    input("Gravando... ENTER para parar.")
    audio = grav.parar_gravacao()
    
    if len(audio) == 0:
        print("Sem áudio.")
        return
    
    # Salva cópia
    grav.salvar_audio(audio, f"gravacao_bruta_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav")
    
    # Processa
    texto = processar_audio_para_texto(audio, sensibilidade=0.35)
    print(f"Resultado: {texto}")

if __name__ == "__main__":
    main()