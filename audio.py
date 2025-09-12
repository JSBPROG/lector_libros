from pydub import AudioSegment
import os

class Audio_utility:
    """
    Clase de utilidad para trabajar con archivos de audio.

    Actualmente, proporciona una funcionalidad para concatenar
    múltiples archivos de audio en uno solo.

    Attributes
    ----------
    __out_path : str
        Ruta del directorio donde se guardará el audio resultante.
    __list_audios : list[str]
        Lista de nombres de archivo de los audios a concatenar.
    __path : str
        Ruta del directorio donde se encuentran los audios a concatenar.
    """
    def __init__(self, out_path: str, list_audios: list[str], path: str):
        """
        Inicializa la clase Audio_utility.

        Parameters
        ----------
        out_path : str
            Ruta del directorio donde se guardará el audio resultante.
        list_audios : list[str]
            Lista de nombres de archivo de los audios a concatenar.
        path : str
            Ruta del directorio donde se encuentran los audios a concatenar.
        """
        self.__out_path = out_path
        self.__list_audios = list_audios  
        self.__path = path

    
    def concatenate_audio(self) -> None:
        """
        Concatena una lista de archivos de audio en un único archivo WAV.

        Los archivos de audio de entrada se leen desde el directorio `path`,
        se unen en orden y el resultado se exporta a un archivo llamado
        `audio_concatenado_final.wav` en el directorio `out_path`.
        """
        print("Concatenando archivos de audio...")
        audio_concatenated = AudioSegment.empty()

        for audio_file in self.__list_audios:
            audio_path = os.path.join(self.__path, audio_file)
            print(f"Añadiendo: {audio_path}")
            audio_segment = AudioSegment.from_wav(audio_path)
            audio_concatenated += audio_segment

        output_file = os.path.join(self.__out_path, "audio_concatenado_final.wav")
        audio_concatenated.export(output_file, format="wav")
        print(f"\nAudio concatenado con éxito en: {output_file}")