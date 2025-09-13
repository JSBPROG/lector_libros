import os
from divider_pages import Divider
from IA.VoiceReader import VoiceReader
from audio import AudioConcatenator
import config
import utils

class PdfToAudiobookPipeline:
    def __init__(self):
        self.reader = VoiceReader()

    def run(self):
        self._setup()
        self._process_pdf()
        self._generate_audio_from_text_files()
        self._concatenate_audio_files()
        print("\nPipeline finalizado con éxito!")

    def _setup(self):
        print("1. Configurando directorios...")
        utils.create_directories(config.DIRECTORIES_TO_CREATE)
        print("   -> Directorios listos.")

    def _process_pdf(self):
        print("\n2. Procesando PDF...")
        divider = Divider(
            path=config.DATA_DIR,
            name_file=config.PDF_FILENAME,
            base_output_name=config.BASE_OUTPUT_NAME
        )
        divider.split_pdf()
        divider.pdfs_to_text()
        print("   -> PDF dividido y texto extraído.")

    def _generate_audio_from_text_files(self):
        print("\n3. Generando archivos de audio...")
        text_files = sorted([f for f in os.listdir(config.TEXT_DIR) if f.endswith(".txt")])
        
        for txt_file in text_files:
            txt_path = os.path.join(config.TEXT_DIR, txt_file)
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()

            page_number_str = txt_file.split('_')[-1].replace('.txt', '')
            audio_filename = f"{config.BASE_OUTPUT_NAME}_pagina_{page_number_str}.wav"
            audio_path = os.path.join(config.AUDIO_DIR, audio_filename)

            print(f"   -> Generando audio para {txt_file}...")
            self.reader.read(text, audio_path)
        print("   -> Todos los archivos de audio generados.")

    def _concatenate_audio_files(self):
        print("\n4. Concatenando archivos de audio...")
        wav_files = [f for f in os.listdir(config.AUDIO_DIR) if f.endswith('.wav')]
        
        try:
            wav_files.sort(key=lambda f: int(f.split('_')[-1].replace('.wav', '')))
        except (IndexError, ValueError):
            print("   -> Advertencia: No se pudieron ordenar los archivos de audio numéricamente. Usando ordenación por defecto.")
            wav_files.sort()

        concatenator = AudioConcatenator(
            input_path=config.AUDIO_DIR,
            output_path=config.RESULT_AUDIO_DIR
        )
        output_filename = f"{config.BASE_OUTPUT_NAME}_completo.wav"
        concatenator.concatenate(audio_files=wav_files, output_filename=output_filename)
        print(f"   -> Concatenación completada.")