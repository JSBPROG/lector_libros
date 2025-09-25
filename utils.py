import os
from langdetect import detect
from transformers import pipeline

def create_directories(directories: list[str]) -> None:
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def detec_lang(text: str) -> str:
    lang = str(detect(text))
    print(f"El idioma es: {lang}")
    return lang

