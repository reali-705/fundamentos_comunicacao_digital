import numpy as np
from config import RECORDINGS_DIR, SAMPLE_RATE
from numpy.typing import NDArray
from scipy.io import wavfile
import sounddevice as sd


class GravadorAudio:
    """Classe responsável por gravar áudio e salvar como WAV."""

    def __init__(self, gravando: bool = False, sample_rate: int = SAMPLE_RATE) -> None:
        self.gravando = gravando
        self.sample_rate = sample_rate
        self.frames = []
        self.stream = None
        self.device_id = None 


    def escolher_dispositivo_interativamente(self):
        print("\n--- DISPOSITIVOS DE ENTRADA ---")

        devices = sd.query_devices()

        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                print(f"[{i}] {d['name']}")

        print("--------------------------------")

        escolha = input("Digite o ID do microfone (ou ENTER para padrão): ").strip()

        if escolha == "":
            self.device_id = None
            print("Usando dispositivo padrão")
        else:
            self.device_id = int(escolha)
            print(f"Usando dispositivo {self.device_id}")

    # =========================
    # CALLBACK
    # =========================
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

    def parar_gravacao(self):
        self.gravando = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.frames:
            array_final = np.concatenate(self.frames, axis=0)
            return array_final.flatten()
        else:
            return np.array([])

    #redundante? sim , mas preguiça (23:57 já)
    def salvar_audio(self, audio, filename):
        return salvar_audio(audio, filename, self.sample_rate)

    def carregar_de_arquivo(self, filename: str) -> NDArray[np.float32]:
        caminho = RECORDINGS_DIR / "output" / filename
        sr, data = wavfile.read(caminho)

        if data.dtype != np.float32:
            data = data.astype(np.float32) / (np.iinfo(data.dtype).max + 1)

        if len(data.shape) > 1:
            data = data[:, 0]

        return data