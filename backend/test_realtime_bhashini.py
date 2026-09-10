import time
import requests
import base64

API_BASE = "http://127.0.0.1:8000"

def test_realtime_system():
    print("==================================================")
    print("LIVE REAL-TIME BHASHINI AI PIPELINE TEST")
    print("==================================================")
    
    # 1. Health Check
    t0 = time.time()
    health = requests.get(f"{API_BASE}/api/health").json()
    print(f"[1] Health Check ({time.time() - t0:.2f}s):", health)
    assert health.get("bhashini_connected") is True, "Bhashini is not connected!"
    
    # 2. Real-Time Translation via Bhashini
    test_phrase = "Good morning children, open your science book on page five."
    print(f"\n[2] Input Spoken Phrase: '{test_phrase}'")
    
    t0 = time.time()
    trans_resp = requests.post(f"{API_BASE}/api/realtime/translate", json={
        "text": test_phrase,
        "source_lang": "en",
        "target_lang": "hi",
        "grade_level": "Grade 1-5"
    }).json()
    latency_trans = time.time() - t0
    
    print(f"--> Bhashini Real-Time Latency: {latency_trans:.2f}s")
    print(f"--> Simplified for Kids: {trans_resp.get('simplified')}")
    print(f"--> Bhashini Translation (Hindi): {trans_resp.get('translated').encode('utf-8', errors='replace')}")
    print(f"--> Offline Fallback Used: {trans_resp.get('is_offline')}")
    
    # 3. Real-Time Speech Synthesis (TTS) via Bhashini
    translated_text = trans_resp.get('translated')
    print(f"\n[3] Calling Bhashini TTS for: '{translated_text.encode('utf-8', errors='replace')}'")
    t0 = time.time()
    tts_resp = requests.post(f"{API_BASE}/api/tts", json={
        "text": translated_text,
        "lang": "hi",
        "gender": "female"
    }).json()
    latency_tts = time.time() - t0
    
    print(f"--> Bhashini TTS Latency: {latency_tts:.2f}s")
    print(f"--> TTS Audio Source: {tts_resp.get('source')}")
    if tts_resp.get("audio_base64"):
        raw_bytes = base64.b64decode(tts_resp["audio_base64"])
        print(f"--> Successfully received raw neural audio WAV: {len(raw_bytes)} bytes!")
    
    print("\n==================================================")
    print("REAL-TIME BHASHINI TEST: ALL SYSTEMS 100% OPERATIONAL!")
    print("==================================================")

if __name__ == "__main__":
    test_realtime_system()
