# Lector de Libros a Audio

Este proyecto convierte un libro en formato PDF a un audiolibro en formato WAV. El proceso incluye la división del PDF en páginas, la extracción del texto de cada página y la generación de una voz en español para cada una, para finalmente unir todos los audios en un único archivo.

## Características

- Divide archivos PDF en páginas individuales.
- Extrae el texto de cada página.
- Convierte el texto a voz usando un modelo de IA de Hugging Face (`facebook/mms-tts-spa`).
- Concatena los audios generados en un único archivo de audiolibro.

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo.

1.  **Clonar el repositorio**
    ```bash
    git clone <URL-del-repositorio>
    cd lector_libros
    ```

2.  **Crear y activar un entorno virtual**
    ```bash
    # Crear el entorno
    python -m venv .venv

    # Activar en Windows
    .venv\Scripts\activate

    # Activar en macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instalar dependencias**
    Instala todas las librerías necesarias usando el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    > **Nota:** La librería `pydub` requiere [FFmpeg](https://ffmpeg.org/download.html) para funcionar correctamente. Asegúrate de tenerlo instalado y disponible en el PATH de tu sistema.

## Uso

1.  **Añadir el PDF**
    Coloca el archivo PDF que deseas convertir en la carpeta `data/`.

2.  **Configurar el nombre del archivo**
    Abre el archivo `config.py` y modifica la siguiente variable:
    - `PDF_FILENAME`: Cambia el valor por el nombre de tu archivo PDF. Por ejemplo: `"mi_libro.pdf"`.
    - `BASE_OUTPUT_NAME`: (Opcional) Cambia el nombre base que se usará para los archivos generados.

3.  **Ejecutar el proyecto**
    ```bash
    python main.py
    ```

4.  **Encontrar el resultado**
    - Los audios de cada página se guardarán en la carpeta `audio/`.
    - El audiolibro final se encontrará en la carpeta `audio/result_audio/` con el nombre `{BASE_OUTPUT_NAME}_completo.wav`.

## Estructura del Proyecto

```
lector_libros/
├── data/                   # Contiene los PDFs de entrada
├── audio/                  # Guarda los audios generados por página
│   └── result_audio/       # Guarda el audiolibro final concatenado
├── output/                 # Carpeta temporal para las páginas del PDF
├── text/                   # Carpeta temporal para el texto extraído
├── IA/
│   └── VoiceReader.py      # Clase para la conversión de texto a voz
├── .gitignore
├── audio.py                # Clase para la manipulación de audio (concatenar)
├── config.py               # Archivo de configuración de rutas y nombres
├── divider_pages.py        # Clase para dividir el PDF y extraer texto
├── main.py                 # Script de entrada que ejecuta el pipeline
├── pipeline.py             # Orquesta todo el proceso de conversión
├── utils.py                # Funciones de utilidad (ej. crear directorios)
└── requirements.txt        # Lista de dependencias de Python
```
