import os
from divider_pages import Divider
from IA.VoiceReader import VoiceReader_es
from IA.VoiceReader import VoiceReader_en
from audio import AudioConcatenator
import config
from IA.Translator import Translator
from langdetect import detect

class PdfToAudiobookPipeline:
    def __init__(self):
        self.reader_es = VoiceReader_es()
        self.reader_en = VoiceReader_en()
        self.translator = Translator()
        self.translation_decision = None

    def run(self):
        self._setup_directories()
        self._process_pdf()
        self._generate_audio()
        self._concatenate_audio()
        print("\nPipeline finalizado con éxito!")

    def _setup_directories(self):
        print("1. Configurando directorios...")
        for directory in config.DIRECTORIES_TO_CREATE:
            os.makedirs(directory, exist_ok=True)
        print("   -> Directorios listos.")

    def _process_pdf(self):
        print("\n2. Procesando PDF y traduciendo si se requiere...")
        self._split_pdf()
        text_files = self._get_text_files()
        self._translate_files(text_files)
        print("   -> PDF dividido, texto extraído y traducido según elección del usuario.")

    def _split_pdf(self):
        divider = Divider(
            path=config.DATA_DIR,
            name_file=config.PDF_FILENAME,
            base_output_name=config.BASE_OUTPUT_NAME
        )
        divider.split_pdf()
        divider.pdfs_to_text()

    def _get_text_files(self):
        return sorted([f for f in os.listdir(config.TEXT_DIR) if f.endswith(".txt")])

    def _translate_files(self, text_files):
        if not text_files:
            return

        # Ask for translation only once based on the first file
        first_file_path = os.path.join(config.TEXT_DIR, text_files[0])
        with open(first_file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        lang = detect(text)
        if lang in ("es", "en"):
            self.translation_decision = self._ask_translation(lang)

        for txt_file in text_files:
            path = os.path.join(config.TEXT_DIR, txt_file)
            if self.translation_decision:
                with open(path, "r", encoding="utf-8") as f:
                    text_to_translate = f.read()
                
                translated_text = self.translator.translate(text_to_translate, self.translation_decision)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(translated_text)
                print(f"   -> Página {txt_file} traducida a {self.translation_decision}.")
            else:
                print(f"   -> Página {txt_file} no traducida.")


    def _ask_translation(self, lang):
        if lang == "es":
            respuesta = input("Texto detectado en español. ¿Quieres traducirlo al inglés? S/N: ").strip().lower()
            return "en" if respuesta == "s" else None
        elif lang == "en":
            respuesta = input("Texto detectado en inglés. ¿Quieres traducirlo al español? S/N: ").strip().lower()
            return "es" if respuesta == "s" else None
        return None

    def _generate_audio(self):
        print("\n3. Generando archivos de audio...")
        for txt_file in self._get_text_files():
            path = os.path.join(config.TEXT_DIR, txt_file)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            audio_path = self._build_audio_path(txt_file)

            lang = detect(text)
            print(f"   -> Generando audio para {txt_file} (Idioma final detectado: {lang})...")

            if lang == "es":
                self.reader_es.read(text, audio_path)
            elif lang == "en":
                self.reader_en.read(text, audio_path)
            else:
                print(f"   -> Idioma no reconocido o no soportado. Usando lector en español por defecto.")
                self.reader_es.read(text, audio_path)

        print("   -> Todos los archivos de audio generados.")

    def _build_audio_path(self, txt_file):
        page_number = txt_file.split('_')[-1].replace('.txt', '')
        return os.path.join(config.AUDIO_DIR, f"{config.BASE_OUTPUT_NAME}_pagina_{page_number}.wav")

    def _concatenate_audio(self):
        print("\n4. Concatenando archivos de audio...")
        wav_files = [f for f in os.listdir(config.AUDIO_DIR) if f.endswith(".wav")]
        try:
            wav_files = sorted(wav_files, key=lambda f: int(f.split('_')[-1].replace('.wav', '')))
        except (IndexError, ValueError):
            print("   -> Advertencia: No se pudieron ordenar los archivos de audio numéricamente. Usando ordenación por defecto.")
            wav_files = sorted(wav_files)

        concatenator = AudioConcatenator(input_path=config.AUDIO_DIR, output_path=config.RESULT_AUDIO_DIR)
        concatenator.concatenate(audio_files=wav_files, output_filename=f"{config.BASE_OUTPUT_NAME}_completo.wav")
        print("   -> Concatenación completada.")
