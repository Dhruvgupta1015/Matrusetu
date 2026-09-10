import requests

def test_api():
    base = "http://127.0.0.1:8000"
    
    # 1. Health
    h = requests.get(f"{base}/api/health").json()
    print("Health:", h)
    
    # 2. Languages
    langs = requests.get(f"{base}/api/languages").json()
    print(f"Loaded {langs['total']} languages.")
    
    # 3. Process Santali
    p1 = requests.post(f"{base}/api/process", json={
        "text": "Plants need sunlight and water to make food.",
        "source_lang": "en",
        "target_lang": "sat",
        "simplify_text": True
    }).json()
    print("Processed Santali translation:", p1.get("translated_text").encode('utf-8', errors='replace'))
    
    # 4. Process Hindi
    p2 = requests.post(f"{base}/api/process", json={
        "text": "Welcome to school children!",
        "source_lang": "en",
        "target_lang": "hi",
        "simplify_text": True
    }).json()
    print("Processed Hindi translation:", p2.get("translated_text").encode('utf-8', errors='replace'))
    
    # 5. Kahani
    k = requests.post(f"{base}/api/kahani", json={
        "topic": "photosynthesis",
        "target_lang": "hi"
    }).json()
    print("Desi Kahani Title:", k.get("title"))
    print("Flashcards count:", len(k.get("flashcards", [])))

    # 6. FLN Evaluate
    fln = requests.post(f"{base}/api/fln/evaluate", json={
        "target_text": "dare ko jomag benaw lagid",
        "spoken_text": "dare ko jomag benaw lagid"
    }).json()
    print(f"FLN Accuracy: {fln.get('accuracy_pct')}% | Stars: {fln.get('stars')} | Words: {fln.get('correct_words')}/{fln.get('total_words')}")
    print("Cheer message:", fln.get("cheer_message"))

if __name__ == "__main__":
    test_api()
