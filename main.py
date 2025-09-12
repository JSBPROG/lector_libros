# main.py
# Este script divide un PDF, extrae el texto de cada página y genera un archivo de audio para cada página usando VoiceReader.

from divider_pages import Divider
from IA.VoiceReader import VoiceReader
import os
from audio import Audio_utility

if __name__ == "__main__":

    # ---------------------------
    # Configuración de rutas y nombres
    # ---------------------------
    pdf_path = "./data/LaNocheBocaArriba.pdf"
    base_output_name = "LaNocheBocaArriba"
    text_dir = "text"       
    audio_dir = "audio"     
    audio_out_dir = f"{audio_dir}/result_audio"
    # Crear carpetas si no existen
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    if not os.path.exists(audio_out_dir):
        os.makedirs(audio_out_dir)

    # ---------------------------
    # Dividir PDF y extraer texto
    # ---------------------------
    divider = Divider(path="./data", name_file="LaNocheBocaArriba.pdf", base_output_name=base_output_name)
    divider.split_pdf()
    divider.pdfs_to_text()
    print("PDF dividido y texto extraído correctamente.")

    # ---------------------------
    # Inicializar el lector de voz
    # ---------------------------
    reader = VoiceReader()
    
    # ---------------------------
    # Generar audio para cada página de texto
    # ---------------------------
    for txt_file in sorted(os.listdir(text_dir)):
        if txt_file.endswith(".txt"):
            
            txt_path = os.path.join(text_dir, txt_file)
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()

            
            page_number = txt_file.split("_")[-1].replace(".txt","") 
            audio_path = os.path.join(audio_dir, f"{base_output_name}_pagina_{page_number}.wav")

            
            print(f"Generando audio para {txt_file}...")
            reader.read(text, audio_path)

    print("Todos los audios generados correctamente.")
    print ("Concatenando archivos de audio, espera puede tardar un rato...")

    #Creamos un objeto Audio para concatenar archivos
    wav_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
    wav_files.sort(key=lambda f: int(f.split('_')[-1].replace('.wav', '')))
    audio = Audio_utility(out_path=audio_out_dir, list_audios=wav_files, path=audio_dir)
    audio.concatenate_audio()
