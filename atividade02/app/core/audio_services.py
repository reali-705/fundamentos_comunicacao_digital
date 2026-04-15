import numpy as np
from config import RECORDINGS_DIR, SAMPLE_RATE
from numpy.typing import NDArray
from scipy.io import wavfile
from scipy.signal import butter, filtfilt 
import sounddevice as sd

class GravadorAudio:
    """Classe responsável por gravar, salvar e processar áudio (filtros e normalização)."""

    def __init__(self, gravando: bool = False, sample_rate: int = SAMPLE_RATE) -> None:
        self.gravando = gravando
        self.sample_rate = sample_rate
        self.frames = []
        self.stream = None
        self.device_id = None 

    def listar_dispositivos(self) -> list[dict]:
        """Retorna uma lista de dicionários com dispositivos de entrada para o frontend."""
        devices = sd.query_devices()
        dispositivos_entrada = []
        
        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                dispositivos_entrada.append({
                    "id": i,
                    "nome": d["name"],
                    "canais": d["max_input_channels"],
                    "default_sr": d["default_samplerate"]
                })
        return dispositivos_entrada

    def configurar_dispositivo(self, dispositivo_id: int | None = None) -> dict:
        """
        Configura o dispositivo baseado em um ID enviado pelo frontend.
        Se dispositivo_id for None, usa o padrão do sistema.
        """
        try:
            if dispositivo_id is not None:
                # Valida se o ID existe antes de atribuir
                sd.query_devices(dispositivo_id, 'input')
                self.device_id = dispositivo_id
                msg = f"Dispositivo {dispositivo_id} selecionado."
            else:
                self.device_id = None
                msg = "Dispositivo padrão selecionado."
            
            return {"status": "sucesso", "message": msg}
        except Exception as e:
            return {"status": "erro", "message": f"ID de dispositivo inválido: {e}"}

    def _callback_audio(
        self,
        indata: np.ndarray,
        frames: int,
        time: dict,
        status: sd.CallbackFlags
    ) -> None:
        if status:
            print(f"⚠️ Status do Stream: {status}", flush=True)
        if self.gravando:
            self.frames.append(indata.copy())

    def iniciar_gravacao(self) -> dict:
        self.gravando = True
        self.frames = []
        self.stream = sd.InputStream(
            device=self.device_id, 
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=self._callback_audio
        )
        self.stream.start()
        return {
            "status": "gravando",
            "message": f"Gravação iniciada (device={self.device_id})"
        }

    def parar_gravacao(self) -> NDArray[np.float32]:
        self.gravando = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.frames:
            array_final = np.concatenate(self.frames, axis=0)
            return array_final.flatten()
        return np.array([], dtype=np.float32)

    def salvar_audio(self, audio: NDArray[np.floating], filename: str) -> str:
        caminho_completo = RECORDINGS_DIR / "output" / filename
        caminho_completo.parent.mkdir(parents=True, exist_ok=True)
        audio32: NDArray[np.float32] = np.asarray(audio, dtype=np.float32)
        try:
            wavfile.write(caminho_completo, self.sample_rate, audio32)
            print(f"Sucesso! Áudio salvo como: {filename}")
            return str(caminho_completo)
        except Exception as e:
            print(f"Erro ao salvar áudio: {e}")
        return ""

    def carregar_de_arquivo(self, filename: str) -> NDArray[np.float32]:
        caminho = RECORDINGS_DIR / "output" / filename
        sr, data = wavfile.read(caminho)
        if data.dtype != np.float32:
            data = data.astype(np.float32) / (np.iinfo(data.dtype).max + 1)
        if len(data.shape) > 1:
            data = data[:, 0]
        return data

    # --- NOVOS MÉTODOS DE PROCESSAMENTO DE SINAL ---

    def filtrar_audio(
        self,
        audio: NDArray[np.floating],
        freq_baixa: int = 500,
        freq_alta: int = 1000,
    ) -> NDArray[np.floating]:
        """Aplica filtro Butterworth passa-banda para isolar a faixa do Morse."""
        nyquist = 0.5 * self.sample_rate
        low = freq_baixa / nyquist
        high = freq_alta / nyquist
        b, a = butter(4, [low, high], btype='band')
        return filtfilt(b, a, audio)

    def normalizar_amplitude(
        self,
        audio: NDArray[np.floating],
        amplitude_alvo: float = 0.5,
        limiar_fraco: float = 0.05,
    ) -> NDArray[np.floating]:
        """Amplifica o sinal se a amplitude máxima estiver abaixo do limiar."""
        pico = np.max(np.abs(audio))
        if pico < limiar_fraco:
            ganho = amplitude_alvo / (pico + 1e-6)
            print(f"[ganho automático] fator aplicado: {ganho:.2f}x")
            return audio * ganho
        return audio
    def encontrar_frequencia_dominante(self, audio: NDArray[np.floating]) -> int:
        """Ajusta o receptor para a frequência real captada pelo driver."""
        if audio.size == 0: return 800
        
        # Analisa o espectro de frequências (FFT)
        fourier = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), d=1/self.sample_rate)
        
        # Pega a frequência com maior pico de energia
        f_central = freqs[np.argmax(np.abs(fourier))]
        
        # Filtro de sanidade: Morse costuma estar entre 400Hz e 1200Hz
        if 300 < f_central < 2500:
            print(f"[Auto-Tune] Frequência do driver detectada: {f_central:.2f}Hz")
            return int(f_central)
        return 800 # Volta pro padrão se detectar algo estranho

    def pre_processar(self, audio: NDArray[np.floating]) -> NDArray[np.floating]:
        """Pipeline adaptativo completo."""
        # 1. Identifica a banda do sinal atual
        f_central = self.encontrar_frequencia_dominante(audio)
        
        # 2. Ajusta as janelas do filtro dinamicamente (+- 150Hz de margem)
        f_baixa = max(300, f_central - 150)
        f_alta = min(self.sample_rate // 2 - 1, f_central + 150)
        
        # 3. Processa com os novos parâmetros
        audio_filtrado = self.filtrar_audio(audio, f_baixa, f_alta)
        audio_normal = self.normalizar_amplitude(audio_filtrado)
        
        return audio_normal

    def pre_processar(self, audio, freq_baixa=500, freq_alta=1000,
                  amplitude_alvo=0.5, limiar_fraco=0.05,
                  auto_tune=True):
        if auto_tune:
            f_central = self.encontrar_frequencia_dominante(audio)
            if f_central != 800:
                freq_baixa = max(300, f_central - 150)
                freq_alta = min(self.sample_rate // 2 - 1, f_central + 150)

        audio_filtrado = self.filtrar_audio(audio, freq_baixa, freq_alta)
        return self.normalizar_amplitude(audio_filtrado, amplitude_alvo, limiar_fraco)