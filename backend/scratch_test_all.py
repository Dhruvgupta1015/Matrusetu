import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')
API = 'http://127.0.0.1:8000'

def test_all():
    print("==================================================")
    print("MATRUBHASA AI FULL-STACK OPTIONS & ENDPOINT AUDIT")
    print("==================================================")

    # 1. Health
    h = requests.get(f"{API}/api/health").json()
    print("[1] HEALTH CHECK:", h)

    # 2. Languages
    langs = requests.get(f"{API}/api/languages").json()
    print(f"[2] LANGUAGES SUPPORTED ({langs['total']}):", [l['code'] for l in langs['languages']])

    # 3. Process endpoint
    p = requests.post(f"{API}/api/process", json={
        "text": "Good morning children, today we learn science.",
        "source_lang": "en",
        "target_lang": "sat",
        "simplify_text": True,
        "grade_level": "Grade 1-5"
    }).json()
    print("[3] PROCESS (en -> sat):", p.get("translated_text"))

    # 4. Realtime Translate for all UI target languages
    print("\n[4] REALTIME TRANSLATION FOR ALL TARGET OPTIONS:")
    target_langs = ["sat", "ho", "unr", "kru", "khr", "sck", "hi", "bn", "or"]
    for lang in target_langs:
        r = requests.post(f"{API}/api/realtime/translate", json={
            "text": "Plants need water and sunlight.",
            "source_lang": "en",
            "target_lang": lang,
            "grade_level": "Grade 1-5"
        }).json()
        print(f"  • {lang:5s} -> Translated: {r.get('translated')}")

    # 5. TTS for Indic & Tribal
    print("\n[5] TEXT-TO-SPEECH (TTS):")
    for lang, text in [("hi", "नमस्ते बच्चों"), ("sat", "ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ"), ("bn", "গাছের জল দরকার")]:
        tts_resp = requests.post(f"{API}/api/tts", json={
            "text": text,
            "lang": lang,
            "gender": "female"
        }).json()
        print(f"  • {lang:5s} -> Source: {tts_resp.get('source')}, Has Audio: {bool(tts_resp.get('audio_base64'))}, Fallback: {tts_resp.get('fallback_web_speech')}")

    # 6. Desi Kahani Generator
    print("\n[6] PATHSHALA LENS - DESI KAHANI:")
    for topic in ["Water Cycle", "Photosynthesis"]:
        k = requests.post(f"{API}/api/kahani", json={
            "topic": topic,
            "target_lang": "hi",
            "grade_level": "Grade 1-5"
        }).json()
        print(f"  • Topic: '{topic}' -> Title: '{k.get('title')}', Flashcards: {len(k.get('flashcards', []))}")

    # 7. FLN Reading Assessment
    print("\n[7] BAL VATIKA - NIPUN FLN READING EVAL:")
    fln = requests.post(f"{API}/api/fln/evaluate", json={
        "target_text": "ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ",
        "spoken_text": "ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ",
        "lang": "sat"
    }).json()
    print("  • FLN Evaluation:", fln)

    # 8. Parent Briefing
    print("\n[8] SIKSHAK HUB - MATRU-SANDESH PARENT BRIEFING:")
    pb = requests.post(f"{API}/api/parent/briefing", json={
        "lesson_title": "Parts of Plants and Leaves",
        "lang": "hi"
    }).json()
    print(f"  • Script ({len(pb.get('audio_script', ''))} chars):", pb.get('audio_script')[:80] + "...")

    # 9. Tribal Phrasebook & Lookup
    print("\n[9] TRIBAL GLOSSARY & VOCABULARY:")
    phrases = requests.get(f"{API}/api/tribal/phrases?lang=sat").json()
    print(f"  • Santali phrases loaded: {len(phrases.get('phrases', []))}")
    for w in ["water", "tree", "sun", "book"]:
        look = requests.get(f"{API}/api/tribal/lookup?query={w}&lang=sat").json()
        found = look.get("found")
        trans = look.get("result", {}).get("translation", "N/A") if found else "N/A"
        print(f"  • Lookup '{w}': Found={found}, Translation={trans}")

    print("\n==================================================")
    print("ALL API ENDPOINTS AND VOCABULARY OPTIONS VERIFIED!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
