from pydub import AudioSegment
import os

class AudioConcatenator:

    def __init__(self, input_path: str, output_path: str):
        self._input_path = input_path
        self._output_path = output_path

    def _read_audio_segment(self, file_path: str) -> AudioSegment:
        print(f"Añadiendo: {file_path}")
        return AudioSegment.from_wav(file_path)

    def _ensure_wav_extension(self, filename: str) -> str:
        if not filename.lower().endswith('.wav'):
            return filename + '.wav'
        return filename

    def _build_concatenated_segment(self, audio_files: list[str]) -> AudioSegment:
        concatenated_audio = AudioSegment.empty()
        for audio_file in audio_files:
            audio_path = os.path.join(self._input_path, audio_file)
            audio_segment = self._read_audio_segment(audio_path)
            concatenated_audio += audio_segment
        return concatenated_audio

    def _export_concatenated_audio(self, concatenated_audio: AudioSegment, output_filename: str) -> None:
        output_filename = self._ensure_wav_extension(output_filename)
        output_file = os.path.join(self._output_path, output_filename)
        concatenated_audio.export(output_file, format="wav")
        print(f"\nAudio concatenado con éxito en: {output_file}")

    def concatenate(self, audio_files: list[str], output_filename: str) -> None:
        print("Concatenando archivos de audio...")
        concatenated_audio = self._build_concatenated_segment(audio_files)
        self._export_concatenated_audio(concatenated_audio, output_filename)
