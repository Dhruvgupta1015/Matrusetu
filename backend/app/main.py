import base64
import os
from typing import Optional, List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .indictrans_service import translate_text, TranslationError
from .simplify import simplify
from .tribal_glossary import (
    TRIBAL_LANGUAGES_METADATA,
    CURATED_VOCABULARY,
    COMMON_LESSON_SENTENCES,
    find_tribal_word,
    get_common_phrases,
    ol_chiki_to_phonetic,
)
from .pedagogy_engine import (
    elif_simplify,
    generate_desi_kahani,
    evaluate_fln_reading,
    generate_parent_briefing,
)
from .curriculum_data import (
    get_all_books,
    get_chapter_by_id,
    get_offline_grade_bundle,
)

try:
    from .bhashini_client import BhashiniClient, BhashiniError
except ImportError:
    BhashiniClient = None
    BhashiniError = Exception

app = FastAPI(
    title="Matrubhasa AI — Vernacular Pedagogy & Real-Time Translation API",
    description="AI-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education (SIH26042)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_bhashini_client = None

def get_bhashini_client():
    global _bhashini_client
    if _bhashini_client is None:
        if BhashiniClient is None:
            return None
        user_id = os.getenv("BHASHINI_USER_ID")
        api_key = os.getenv("BHASHINI_ULCA_API_KEY")
        if not user_id or not api_key or "your_" in user_id or "your_" in api_key:
            return None
        try:
            _bhashini_client = BhashiniClient(user_id=user_id, ulca_api_key=api_key)
        except Exception as e:
            print(f"Warning: Could not initialize Bhashini Client: {e}")
            return None
    return _bhashini_client


# Request & Response Models
class ProcessRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "hi"
    simplify_text: bool = True
    use_llm_simplify: bool = False
    grade_level: str = "Grade 1-5"


class ProcessResponse(BaseModel):
    original_text: str
    simplified_text: str
    translated_text: str
    target_lang: str
    source_lang: str
    is_offline_glossary: bool = False
    pedagogy_tips: Optional[str] = None


class RealtimeTranslateRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "hi"
    grade_level: str = "Grade 1-5"


class TtsRequest(BaseModel):
    text: str
    lang: str
    gender: str = "female"


class AsrRequest(BaseModel):
    audio_base64: str
    lang: str = "hi"


class KahaniRequest(BaseModel):
    topic: str
    target_lang: str = "hi"
    grade_level: str = "Grade 1-5"


class FlnEvaluateRequest(BaseModel):
    target_text: str
    spoken_text: str
    lang: str = "hi"


class ParentBriefingRequest(BaseModel):
    lesson_title: str
    lang: str = "hi"


@app.get("/api/health")
def health():
    b_client = get_bhashini_client()
    hf_token_set = bool(os.getenv("HF_TOKEN"))
    return {
        "status": "ok",
        "bhashini_connected": b_client is not None,
        "indictrans_connected": hf_token_set,
        "offline_tribal_glossary_loaded": len(CURATED_VOCABULARY)
    }


@app.get("/api/languages")
def languages():
    """Returns rich language options with full native names, scripts, and regional context."""
    results = []
    for code, meta in TRIBAL_LANGUAGES_METADATA.items():
        results.append({
            "code": code,
            "name_en": meta["name_en"],
            "name_native": meta["name_native"],
            "script": meta["script"],
            "region": meta["region"],
            "official_status": meta["official_status"],
            "display_label": f"{meta['name_native']} ({meta['name_en']})"
        })
    return {
        "languages": results,
        "total": len(results)
    }


def _translate_with_fallback(text: str, source_lang: str, target_lang: str) -> tuple[str, bool]:
    """
    Intelligent multi-tier translation pipeline:
    1. Check if direct match in tribal / vernacular offline phrasebank.
    2. Try Bhashini client if active credentials.
    3. Try IndicTrans2 (Hugging Face) if token present.
    4. Fallback to tribal glossary word-level or transliterated output.
    """
    if not text.strip():
        return "", False

    # Auto-detect Devanagari script (Hindi) if source is set to English
    if source_lang == "en" and any('\u0900' <= c <= '\u097F' for c in text):
        source_lang = "hi"

    # Tier 1: Check curated classroom sentences
    for phrase in COMMON_LESSON_SENTENCES:
        if phrase["en"].lower() in text.lower() or text.lower() in phrase["en"].lower():
            if target_lang in phrase:
                return phrase[target_lang], True

    # Tier 2: Bhashini API
    b_client = get_bhashini_client()
    if b_client:
        try:
            translated = b_client.translate(text, source_lang, target_lang)
            return translated, False
        except Exception:
            pass

    # Tier 3: IndicTrans2 via HuggingFace
    if os.getenv("HF_TOKEN"):
        try:
            translated = translate_text(text, source_lang, target_lang)
            return translated, False
        except Exception:
            pass

    # Tier 4: Tribal Glossary Word Replacement / Fallback
    words = text.split()
    translated_words = []
    any_tribal_match = False

    for w in words:
        cleaned = w.strip(",.!?()").lower()
        match = find_tribal_word(cleaned, target_lang)
        if match:
            translated_words.append(match["translation"])
            any_tribal_match = True
        else:
            translated_words.append(w)

    if any_tribal_match:
        return " ".join(translated_words), True

    # Ultimate graceful fallback (returns simplified original with language indicator)
    meta = TRIBAL_LANGUAGES_METADATA.get(target_lang, {})
    lang_name = meta.get("name_native", target_lang)
    return f"[{lang_name}] {text}", True


@app.post("/api/process", response_model=ProcessResponse)
def process(req: ProcessRequest):
    text_to_translate = req.text
    if req.simplify_text:
        text_to_translate = elif_simplify(req.text, grade=req.grade_level)

    translated, is_offline = _translate_with_fallback(
        text_to_translate, req.source_lang, req.target_lang
    )

    pedagogy_tip = f"Concept explained for primary {req.grade_level} with conversational vernacular cues."

    return ProcessResponse(
        original_text=req.text,
        simplified_text=text_to_translate,
        translated_text=translated,
        target_lang=req.target_lang,
        source_lang=req.source_lang,
        is_offline_glossary=is_offline,
        pedagogy_tips=pedagogy_tip
    )


@app.post("/api/realtime/translate")
def realtime_translate(req: RealtimeTranslateRequest):
    """Low-latency endpoint optimized for live classroom microphone broadcasting."""
    simplified = elif_simplify(req.text, grade=req.grade_level)
    translated, is_offline = _translate_with_fallback(simplified, req.source_lang, req.target_lang)
    
    return {
        "original": req.text,
        "simplified": simplified,
        "translated": translated,
        "is_offline": is_offline,
        "target_lang": req.target_lang
    }


@app.post("/api/tts")
def tts(req: TtsRequest):
    """Text-to-speech with silence detection, tribal phonetics, and browser fallback."""
    b_client = get_bhashini_client()

    def is_silent(data: bytes) -> bool:
        if not data or len(data) < 44:
            return True
        pcm = data[44:]
        return len(pcm) < 8000 and max(pcm) <= 2

    # Transliterate Ol Chiki script to phonetic Devanagari for speech
    spoken_text = ol_chiki_to_phonetic(req.text)
    is_tribal = req.lang in ["sat", "ho", "unr", "kru", "khr", "sck"]

    if b_client:
        # If tribal language, use phonetic Hindi voice which speaks Devanagari/tribal text smoothly
        if is_tribal:
            try:
                audio_bytes = b_client.text_to_speech(spoken_text, "hi", req.gender)
                if not is_silent(audio_bytes):
                    return {
                        "source": "bhashini",
                        "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
                        "fallback_web_speech": False,
                        "spoken_text": spoken_text
                    }
            except Exception:
                pass
        else:
            # Major Indic languages (hi, bn, or, etc.)
            try:
                audio_bytes = b_client.text_to_speech(req.text, req.lang, req.gender)
                if not is_silent(audio_bytes):
                    return {
                        "source": "bhashini",
                        "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
                        "fallback_web_speech": False,
                        "spoken_text": req.text
                    }
            except Exception:
                pass

            # Fallback to Hindi phonetic voice if specific language failed
            try:
                audio_bytes = b_client.text_to_speech(spoken_text, "hi", req.gender)
                if not is_silent(audio_bytes):
                    return {
                        "source": "bhashini",
                        "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
                        "fallback_web_speech": False,
                        "spoken_text": spoken_text
                    }
            except Exception:
                pass

    # Graceful fallback: instructs client to play using browser Web Speech API
    return {
        "source": "browser_speech",
        "audio_base64": None,
        "fallback_web_speech": True,
        "lang": req.lang if not is_tribal else "hi-IN",
        "text": spoken_text
    }


@app.post("/api/asr")
def asr(req: AsrRequest):
    """Speech-to-text audio transcription with Bhashini AI ASR."""
    # Sanitize audio base64 input (strips data URI prefix like 'data:audio/wav;base64,')
    raw_b64 = req.audio_base64
    if "," in raw_b64:
        raw_b64 = raw_b64.split(",", 1)[1]
    raw_b64 = raw_b64.strip()

    if not raw_b64:
        raise HTTPException(status_code=400, detail="Empty audio data received")

    # Map tribal languages to best phonetic ASR model
    asr_lang = req.lang
    if asr_lang in ["sat", "ho", "unr", "kru", "khr", "sck"]:
        asr_lang = "hi"  # Conformer Hindi model recognizes Devanagari phonetics best
    elif asr_lang not in ["bn", "en", "gu", "hi", "kn", "ml", "mr", "or", "pa", "sa", "ta", "te", "ur"]:
        asr_lang = "hi"

    b_client = get_bhashini_client()
    if b_client:
        try:
            transcript = b_client.speech_to_text(raw_b64, asr_lang)
            return {
                "transcript": transcript,
                "source": "bhashini",
                "lang_used": asr_lang
            }
        except Exception as e:
            # If specified language fails, try Hindi conformer fallback
            if asr_lang != "hi":
                try:
                    transcript = b_client.speech_to_text(raw_b64, "hi")
                    return {
                        "transcript": transcript,
                        "source": "bhashini_fallback_hi",
                        "lang_used": "hi"
                    }
                except Exception:
                    pass
            print(f"Bhashini ASR error: {e}")
            raise HTTPException(status_code=502, detail=f"Bhashini ASR error: {e}")

    return {
        "transcript": "",
        "source": "client_speech_recognition",
        "message": "Bhashini ASR client unavailable. Using browser Web Speech API."
    }


@app.post("/api/kahani")
def kahani(req: KahaniRequest):
    """Generates an engaging, illustrated Indian folk story and flashcards from textbook concepts in chosen mother tongue."""
    result = generate_desi_kahani(req.topic, target_lang=req.target_lang)

    # If target_lang is not Hindi or English, translate the story and title using multi-tier translation
    if req.target_lang not in ["hi", "en"]:
        vernacular_story, is_off = _translate_with_fallback(result["story"], "hi", req.target_lang)
        vernacular_title, _ = _translate_with_fallback(result["title"], "hi", req.target_lang)
        if vernacular_story:
            result["story"] = vernacular_story
        if vernacular_title:
            result["title"] = vernacular_title
        result["is_offline"] = is_off

        for fc in result.get("flashcards", []):
            try:
                base_word = fc["word"].split()[0].strip("()")
                trans_w, _ = _translate_with_fallback(base_word, "hi", req.target_lang)
                if trans_w:
                    fc["word"] = f"{trans_w} ({base_word})"
            except Exception:
                pass

    result["target_lang"] = req.target_lang
    return result


@app.post("/api/fln/evaluate")
def fln_evaluate(req: FlnEvaluateRequest):
    """NIPUN Bharat Foundational Literacy and Numeracy reading assessment."""
    evaluation = evaluate_fln_reading(req.target_text, req.spoken_text)
    return evaluation


@app.post("/api/parent/briefing")
def parent_briefing(req: ParentBriefingRequest):
    """Generates a 30-second audio note script in mother tongue for rural parents."""
    script = generate_parent_briefing(req.lesson_title, req.lang)
    return {
        "lesson_title": req.lesson_title,
        "lang": req.lang,
        "audio_script": script
    }


@app.get("/api/tribal/phrases")
def tribal_phrases(lang: str = "sat"):
    """Returns pre-cached foundational classroom phrases in the chosen vernacular."""
    phrases = get_common_phrases(lang)
    return {"phrases": phrases, "lang": lang}


@app.get("/api/tribal/lookup")
def tribal_lookup(query: str, lang: str = "sat"):
    """Instant offline vocabulary lookup for tribal and regional words."""
    result = find_tribal_word(query, lang)
    if result:
        return {"found": True, "result": result}
    return {"found": False, "query": query, "message": "Word not found in core offline glossary"}


@app.get("/api/curriculum/books")
def curriculum_books(grade: Optional[int] = None, subject: Optional[str] = None):
    """Returns list of JCERT / NCERT primary chapters filtered by grade and subject."""
    books = get_all_books(grade=grade, subject=subject)
    return {"books": books, "total": len(books)}


@app.get("/api/curriculum/chapter")
def curriculum_chapter(id: str, lang: str = "sat"):
    """Fetches full chapter content and worksheets adapted to the student's mother tongue."""
    chapter = get_chapter_by_id(id, target_lang=lang)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@app.get("/api/curriculum/offline-bundle")
def curriculum_offline_bundle(grade: Optional[int] = None):
    """Returns complete curriculum bundle for bulk offline storage in client IndexedDB."""
    bundle = get_offline_grade_bundle(grade=grade)
    return {"bundle": bundle, "total": len(bundle), "grade": grade}


# Mount Frontend static files for full-stack zero-configuration serving
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

@app.get("/")
def read_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Matrubhasa AI Backend Active"}

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")