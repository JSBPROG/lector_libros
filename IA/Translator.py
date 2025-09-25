from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langdetect import detect

class Translator:
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Modelo NLLB-200 3.3B cargado en {self.device.upper()}.")

        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-3.3B")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-3.3B").to(self.device)

        self.lang_codes = {
            "es": "spa_Latn",
            "en": "eng_Latn"
        }

    def translate(self, text: str, target_language: str) -> str:
        if target_language not in self.lang_codes:
            raise ValueError(f"Idioma destino no soportado: {target_language}")

        source_lang = detect(text)
        source_code = self.lang_codes.get(source_lang)
        target_code = self.lang_codes[target_language]

        if not source_code:
            raise ValueError(f"Idioma fuente no soportado para NLLB: {source_lang}")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        
        forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(target_code)

        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id
        )

        return self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
