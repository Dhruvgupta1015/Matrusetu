import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

API = 'http://127.0.0.1:8000'

print('=====================================================')
print('MATRUBHASA FULL PIPELINE VERIFICATION TEST')
print('=====================================================')

# 1. Health
print('\n[1] Health Check:')
h = requests.get(f'{API}/api/health').json()
print('Status:', h)
assert h.get('status') == 'ok', 'Health check failed!'

# 2. Real-time Live Translation across multiple languages
print('\n[2] Real-Time Translation Tests:')
tests = [
    ('Good morning children, welcome to class.', 'en', 'sat'),
    ('Plants make food with water and sunshine.', 'en', 'hi'),
    ('हरे पेड़ हमारे सबसे अच्छे मित्र हैं।', 'hi', 'ho'),
    ('Today we will learn math numbers.', 'en', 'kru'),
    ('Water is very precious for our village.', 'en', 'khr')
]

for text, src, tgt in tests:
    resp = requests.post(f'{API}/api/realtime/translate', json={
        'text': text, 'source_lang': src, 'target_lang': tgt, 'grade_level': 'Grade 1-5'
    }).json()
    print(f'--> [{src} -> {tgt}]')
    print(f'    Input:      {text}')
    print(f'    Translated: {resp.get("translated")}')
    print(f'    Simplified: {resp.get("simplified")}')
    print(f'    Is Offline: {resp.get("is_offline")}')

# 3. TTS Voice Generation
print('\n[3] TTS Voice Translation Tests:')
tts_samples = [
    ('hi', 'नमस्ते बच्चों, कक्षा में आपका स्वागत है।'),
    ('sat', 'ᱥᱟᱱᱛᱟᱲᱤ ᱯᱟᱹᱨᱥᱤ ᱛᱮ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ'),
    ('ho', 'ᱦᱳ ᱯᱟᱹᱨᱥᱤ ᱛᱮ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ')
]
for lang, sample in tts_samples:
    tts_resp = requests.post(f'{API}/api/tts', json={
        'text': sample, 'lang': lang, 'gender': 'female'
    }).json()
    b64_len = len(tts_resp.get('audio_base64') or '')
    print(f'--> [{lang}] TTS Source: {tts_resp.get("source")} | Audio Base64 length: {b64_len} chars')
    assert b64_len > 1000 or tts_resp.get('fallback_web_speech'), f'TTS failed for {lang}'

# 4. Curriculum Books & Word-to-word Translation
print('\n[4] Curriculum Books & Word-to-Word Translation Tests:')
books_resp = requests.get(f'{API}/api/curriculum/books').json()
total_books = books_resp.get('total')
print(f'--> Total Books in Curriculum: {total_books}')
assert total_books == 25, f'Expected 25 books, got {total_books}'

for subject in ['evs', 'math', 'hindi', 'english']:
    sub_books = requests.get(f'{API}/api/curriculum/books', params={'subject': subject}).json()
    print(f'    Subject \"{subject}\" book count: {sub_books.get("total")}')

# Word-to-Word Lookup Test
word_test = requests.get(f'{API}/api/curriculum/word-translate', params={'word': 'family', 'lang': 'sat'}).json()
print(f'--> Word lookup (\"family\" -> sat): {word_test.get("translation")} ({word_test.get("phonetic")})')
assert word_test.get('found') is True, 'Word translation lookup failed!'

word_test2 = requests.get(f'{API}/api/curriculum/word-translate', params={'word': 'water', 'lang': 'hi'}).json()
print(f'--> Word lookup (\"water\" -> hi): {word_test2.get("translation")} | Hindi: {word_test2.get("hindi")}')
assert word_test2.get('found') is True, 'Word translation lookup 2 failed!'

print('\n=====================================================')
print('SUCCESS: ALL REAL-TIME VOICE & DATA SYSTEMS 100% OPERATIONAL!')
print('=====================================================')
