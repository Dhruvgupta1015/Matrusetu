import os
from dotenv import load_dotenv

load_dotenv()

user_id = os.getenv("BHASHINI_USER_ID", "").strip()
ulca_api_key = os.getenv("BHASHINI_ULCA_API_KEY", "").strip()
inference_api_key = os.getenv("BHASHINI_INFERENCE_API_KEY", "").strip()

print(f"Loaded User ID: {user_id}")
print(f"Loaded ULCA Key prefix: {ulca_api_key[:10]}...")
print(f"Loaded Inference Key prefix: {inference_api_key[:10]}...")

from app.bhashini_client import BhashiniClient

try:
    client = BhashiniClient(user_id=user_id, ulca_api_key=ulca_api_key)
    print("SUCCESS: Bhashini Pipeline Config Loaded Successfully!")
    print("Available Translation languages:", len(client.available_languages("translation")))
    print("Available TTS languages:", len(client.available_languages("tts")))
    print("Available ASR languages:", len(client.available_languages("asr")))
except Exception as e:
    print(f"Bhashini Pipeline Config test failed: {e}")
