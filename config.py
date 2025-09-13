import os

# --- Input settings ---
PDF_FILENAME = "LaNocheBocaArriba.pdf"
BASE_OUTPUT_NAME = "LaNocheBocaArriba"

# --- Directory settings ---
DATA_DIR = "data"
TEXT_DIR = "text"
AUDIO_DIR = "audio"
OUTPUT_DIR = "output"
RESULT_AUDIO_DIR = os.path.join(AUDIO_DIR, "result_audio")

# --- Derived paths ---
PDF_INPUT_PATH = os.path.join(DATA_DIR, PDF_FILENAME)

# --- List of directories to create ---
DIRECTORIES_TO_CREATE = [
    TEXT_DIR,
    AUDIO_DIR,
    OUTPUT_DIR,
    RESULT_AUDIO_DIR
]
