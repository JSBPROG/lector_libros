import numpy as np
from transformers import pipeline
import wave
import torch

class VoiceReader:
    """
    Clase para convertir texto a voz utilizando un modelo de Transformers.

    Utiliza un pipeline de `text-to-speech` para generar audio a partir
    de un texto dado y lo guarda como un archivo .wav.

    Attributes
    ----------
    pipe : transformers.pipelines.Pipeline
        El pipeline de Hugging Face para la síntesis de voz.
    """
    def __init__(self, model="facebook/mms-tts-spa"):
        """
        Inicializa el VoiceReader con un pipeline de texto a voz.

        Parameters
        ----------
        model : str, optional
            El identificador del modelo de Hugging Face a utilizar.
            Por defecto es "facebook/mms-tts-spa".
        """
        # Determinar el dispositivo a utilizar (GPU si está disponible)
        device = 0 if torch.cuda.is_available() else -1
        self.pipe = pipeline("text-to-speech", model=model, device=device)
        if device == 0:
            print("Pipeline de texto a voz inicializado en GPU.")
        else:
            print("Pipeline de texto a voz inicializado en CPU.")

    def read(self, text: str, output_path: str) -> None:
        """
        Genera audio a partir del texto y lo guarda en un archivo .wav.

        Parameters
        ----------
        text : str
            El texto que se convertirá en audio.
        output_path : str
            La ruta del archivo .wav donde se guardará el audio generado.
        """
        output = self.pipe(text)
        
        audio_np = output["audio"]
        samplerate = output["sampling_rate"]
        
        # Convierte el array de numpy de float32 a enteros de 16-bit
        audio_int16 = (audio_np * 32767).astype(np.int16)

        with wave.open(output_path, 'w') as wf:
            wf.setnchannels(1)       # Mono
            wf.setsampwidth(2)       # 2 bytes = 16-bit
            wf.setframerate(samplerate)
            wf.writeframes(audio_int16.tobytes())
        
        #print(f"Audio guardado en {output_path}")

if __name__ == '__main__':
    # Ejemplo de uso de la clase VoiceReader
    print("Ejecutando ejemplo de VoiceReader...")
    reader = VoiceReader()
    
    text_to_read = "Hola, esto es una prueba de la clase VoiceReader. Quiero una voz natural con acento español de España."
    output_file = "voz_espanol_clase.wav"
    
    reader.read(text_to_read, output_file)
    print(f"Ejemplo finalizado. Audio guardado en {output_file}")
