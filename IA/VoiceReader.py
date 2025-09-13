import numpy as np
from transformers import pipeline
import wave
import torch

class VoiceReader:
    def __init__(self, model="facebook/mms-tts-spa"):
        device = self._get_device()
        self.pipe = self._initialize_pipeline(model, device)
        self._print_device_info(device)

    def _get_device(self) -> int:
        return 0 if torch.cuda.is_available() else -1

    def _initialize_pipeline(self, model: str, device: int):
        return pipeline("text-to-speech", model=model, device=device)

    def _print_device_info(self, device: int) -> None:
        if device == 0:
            print("Pipeline de texto a voz inicializado en GPU.")
        else:
            print("Pipeline de texto a voz inicializado en CPU.")

    def _generate_audio_from_text(self, text: str) -> dict:
        return self.pipe(text)

    def _convert_audio_to_int16(self, audio_np: np.ndarray) -> np.ndarray:
        return (audio_np * 32767).astype(np.int16)

    def _save_audio_to_wav(self, audio_int16: np.ndarray, samplerate: int, output_path: str) -> None:
        with wave.open(output_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_int16.tobytes())

    def read(self, text: str, output_path: str) -> None:
        output = self._generate_audio_from_text(text)
        audio_np = output["audio"]
        samplerate = output["sampling_rate"]
        audio_int16 = self._convert_audio_to_int16(audio_np)
        self._save_audio_to_wav(audio_int16, samplerate, output_path)

if __name__ == '__main__':
    print("Ejecutando ejemplo de VoiceReader...")
    reader = VoiceReader()
    
    text_to_read = "Hola, esto es una prueba de la clase VoiceReader. Quiero una voz natural con acento español de España."
    output_file = "voz_espanol_clase.wav"
    
    reader.read(text_to_read, output_file)
    print(f"Ejemplo finalizado. Audio guardado en {output_file}")