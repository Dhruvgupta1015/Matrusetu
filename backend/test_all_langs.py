import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

API = "http://127.0.0.1:8000/api/realtime/translate"
test_phrase = "The sun gives us light and warmth."

print("=" * 60)
print("REAL-TIME MULTI-LINGUAL TRANSLATION TEST")
print("Phrase:", test_phrase)
print("=" * 60)

langs = ["hi", "bn", "or", "sat", "khr", "sck", "ho", "unr", "sat_Olck"]

for lang in langs:
    try:
        res = requests.post(API, json={
            "text": test_phrase,
            "source_lang": "en",
            "target_lang": lang
        }, timeout=10).json()
        
        is_off = res.get("is_offline", False)
        translated = res.get("translated", "")
        source = "Offline Glossary/Rules" if is_off else "Bhashini / Online AI"
        print(f"[{lang:8}] Source: {source:25} -> {translated}")
    except Exception as e:
        print(f"[{lang:8}] Error: {e}")

print("=" * 60)
