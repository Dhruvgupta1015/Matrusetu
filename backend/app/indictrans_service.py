import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_EN_INDIC = "ai4bharat/indictrans2-en-indic-1B"
HF_MODEL_INDIC_EN = "ai4bharat/indictrans2-indic-en-1B"
HF_API_URL = "https://api-inference.huggingface.co/models/{model}"

LANG_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "sat": "sat_Olck",
    "or": "ory_Orya",
    "bn": "ben_Beng",
    "kru": "kru_Deva",
    "khr": "hin_Deva",
    "sck": "hin_Deva",
    "ho": "sat_Olck",
    "unr": "hin_Deva",
}


class TranslationError(Exception):
    pass


def translate_text(text: str, source_lang: str = "en", target_lang: str = "hi") -> str:
    if not HF_TOKEN:
        raise TranslationError("Missing HF_TOKEN in .env")
    if not text or not text.strip():
        raise ValueError("Text to translate cannot be empty")

    src_code = LANG_CODES.get(source_lang)
    tgt_code = LANG_CODES.get(target_lang)
    if not src_code or not tgt_code:
        raise TranslationError(f"Unsupported language pair: {source_lang} -> {target_lang}")

    model = HF_MODEL_EN_INDIC if source_lang == "en" else HF_MODEL_INDIC_EN
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"src_lang": src_code, "tgt_lang": tgt_code}}

    response = requests.post(HF_API_URL.format(model=model), headers=headers, json=payload, timeout=30)

    if response.status_code == 503:
        raise TranslationError("Model loading on Hugging Face, retry in ~20s.")
    if response.status_code != 200:
        raise TranslationError(f"Translation failed: {response.status_code} {response.text}")

    result = response.json()
    if isinstance(result, list) and result and "translation_text" in result[0]:
        return result[0]["translation_text"]

    raise TranslationError(f"Unexpected response: {result}")