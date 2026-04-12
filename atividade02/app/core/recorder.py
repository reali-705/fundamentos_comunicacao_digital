import threading
from typing import Any

import numpy as np
import sounddevice as sd
from app.core.config import RECORDINGS_DIR, SAMPLE_RATE
from numpy.typing import NDArray
from scipy.io import wavfile


class RecorderManager:
    def __init__(self):
        self.stop_event = threading.Event()
        self.recording_thread: threading.Thread | None = None

    def _record_task(self, filename: str, fs: int = SAMPLE_RATE) -> None:
        """
        Executa a captura de áudio em tempo real.
        """
        print(f"[DEBUG] A iniciar captura de hardware no diretório: {filename}")
        recording_data: list[NDArray[np.float32]] = []

        def callback(
            indata: NDArray[np.float32],
            frames: int,
            time: Any,
            status: Any,
        ) -> None:
            if status:
                print(f"[DEBUG] Status do áudio: {status}")
            recording_data.append(indata.copy())

        # Abre o fluxo de entrada do microfone
        with sd.InputStream(samplerate=fs, channels=1, callback=callback):
            while not self.stop_event.is_set():
                sd.sleep(100)  # type: ignore

        # Consolida os dados e grava o diretório LPCM (WAV) sem compressão
        audio_np = np.concatenate(recording_data, axis=0)
        wavfile.write(filename, fs, audio_np)  # type: ignore
        print("[DEBUG] Gravação finalizada com sucesso.")

    def start(self, filename: str = "input.wav", fs: int = SAMPLE_RATE) -> bool:
        if self.recording_thread and self.recording_thread.is_alive():
            return False  # Já está gravando
        self.stop_event.clear()
        caminho_audio = str(RECORDINGS_DIR / filename)
        self.recording_thread = threading.Thread(
            target=self._record_task, args=(caminho_audio, fs)
        )
        self.recording_thread.start()
        return True

    def stop(self):
        self.stop_event.set()
        if self.recording_thread:
            self.recording_thread.join()
