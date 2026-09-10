"""
Vernacular Pedagogy Engine for Primary Education (Class 1-5).
Provides:
  1. ELI6 (Explain Like I'm 6) pedagogical concept simplification.
  2. 'Desi Kahani' generator: converts formal science/math topics into relatable Indian cultural stories.
  3. Interactive Bilingual Flashcard generator.
  4. NIPUN Bharat FLN Reading & Pronunciation evaluation with gamified star scoring.
  5. Parent Audio Briefing generator in mother tongue.
"""

import re
import difflib
from typing import List, Dict, Any

# Pedagogical topic analogies for primary kids
INDIAN_PEDAGOGICAL_ANALOGIES = {
    "photosynthesis": {
        "title": "Chintu Patta Aur Suraj Chacha ki Rasoi",
        "story_hi": "Ped ke hare patte chhote rasoiye hote hain! Suraj chacha apni dhoop bhejte hain, baadal paani dete hain, aur paudha maze se meetha bhojan banata hai.",
        "story_en": "Green leaves are little master-chefs! With sunshine from the sky and water from the soil, they cook delicious food for the plant.",
        "keywords": ["Sunlight (धूप)", "Water (पानी)", "Leaf (पत्ता)", "Food (भोजन)"]
    },
    "water cycle": {
        "title": "Boondi ki Aakash Yatra",
        "story_hi": "Nadi ki ek nanhi boond 'Boondi' dhoop lagne par bhaanp bankar aakash mein chali gayi. Wahan badal ban kar dosto se mili, aur phir thandi hokar baarish ban ke zameen par laut aayi!",
        "story_en": "Little raindrop Boondi warmed up in the sun and flew to the clouds as steam! When it got cool, she happily fell back as sweet rain.",
        "keywords": ["Evaporation (भाप)", "Clouds (बादल)", "Rain (बारिश)"]
    },
    "gravity": {
        "title": "Dharti Mata ka Pyar",
        "story_hi": "Jab bhi hum koi gend aakash mein uchhalte hain, woh hamesha zameen par laut aati hai. Kyunki Dharti Mata sabhi cheezon ko apne gale lagane ke liye apni taraf kheenchti hain!",
        "story_en": "Whenever you throw a ball in the air, it drops back down. That is Earth's friendly hug pulling everything gently towards herself!",
        "keywords": ["Earth (धरती)", "Pull (खिंचाव)", "Fall (गिरना)"]
    }
}

def elif_simplify(text: str, grade: str = "Grade 1-3") -> str:
    """Simplifies formal textbook sentences into vivid, kid-friendly language."""
    text_clean = text.strip()
    
    # Check for direct conceptual analogies
    for concept, data in INDIAN_PEDAGOGICAL_ANALOGIES.items():
        if concept in text_clean.lower():
            return data["story_en"]

    # Rule-based primary pedagogical simplification
    # Replace overly academic terms with active, kid-friendly verbs
    replacements = [
        (r"\butilize[s]?\b", "uses"),
        (r"\bapproximately\b", "about"),
        (r"\bconsequently\b", "so"),
        (r"\bdemonstrate[s]?\b", "shows"),
        (r"\bfacilitate[s]?\b", "helps"),
        (r"\bnumerous\b", "many"),
        (r"\bfundamental\b", "main"),
        (r"\bprecipitation\b", "rain"),
        (r"\bconsumption\b", "eating"),
        (r"\bmanufacture[s]?\b", "makes"),
        (r"\babsorb[s]?\b", "drinks in"),
    ]
    
    simplified = text_clean
    for pat, rep in replacements:
        simplified = re.sub(pat, rep, simplified, flags=re.IGNORECASE)

    # Break into short, joyful sentences (<= 10 words for Grade 1-5)
    sentences = re.split(r"(?<=[.!?])\s+", simplified)
    short_sentences = []
    for s in sentences:
        words = s.split()
        if len(words) > 12:
            mid = len(words) // 2
            short_sentences.append(" ".join(words[:mid]) + ".")
            short_sentences.append(" ".join(words[mid:]))
        else:
            short_sentences.append(s)

    return " ".join(short_sentences).replace("..", ".")

def generate_desi_kahani(topic_or_text: str, target_lang: str = "hi") -> Dict[str, Any]:
    """Generates an Indian cultural story for primary learners based on topic."""
    topic_lower = topic_or_text.lower()
    
    # Match against known analogies or generate a structured story
    matched = None
    for k, v in INDIAN_PEDAGOGICAL_ANALOGIES.items():
        if k in topic_lower:
            matched = v
            break
            
    if not matched:
        # Default structured story for any primary topic
        matched = {
            "title": f"Nanhe Ustaad Ki Khoj: {topic_or_text[:30]}",
            "story_hi": f"Ek baar ek gaon mein goli aur chintu naam ke do nanhe dost the. Unhone school mein '{topic_or_text[:40]}' ke baare mein suna aur khushi se kood pade. Unke master ji ne bataya ki kaise prakriti har roz naye chamatkar karti hai!",
            "story_en": f"Once in a cheerful village school, two little friends learned about {topic_or_text[:40]}. Their teacher showed them how nature works together every single day!",
            "keywords": ["Friend (दोस्त)", "School (पाठशाला)", "Discovery (खोज)"]
        }

    return {
        "title": matched["title"],
        "story": matched.get(f"story_{target_lang}", matched["story_hi"]),
        "english_story": matched["story_en"],
        "flashcards": [
            {"word": kw, "prompt": "Tap to listen & repeat"} for kw in matched["keywords"]
        ],
        "quiz_question": {
            "question": f"Is kahani se humne kya seekha?",
            "options": ["Prakriti hamari dost hai", "Padhna boring hai", "Khelna mana hai"],
            "correct_index": 0
        }
    }

def evaluate_fln_reading(target_text: str, spoken_text: str) -> Dict[str, Any]:
    """
    Evaluates student pronunciation & reading fluency aligned with NIPUN Bharat FLN.
    Returns word-level status (correct, mispronounced, missing) and awarded stars (1-3).
    """
    def clean_words(t: str) -> List[str]:
        return [re.sub(r'[^\w\s]', '', w).lower() for w in t.strip().split() if w.strip()]

    target_words = clean_words(target_text)
    spoken_words = clean_words(spoken_text)

    if not target_words:
        return {"accuracy": 0, "stars": 0, "words": []}

    matcher = difflib.SequenceMatcher(None, target_words, spoken_words)
    word_evaluations = []
    correct_count = 0

    spoken_idx = 0
    for tw in target_words:
        # Find if target word was spoken near current position
        is_match = False
        if spoken_idx < len(spoken_words):
            ratio = difflib.SequenceMatcher(None, tw, spoken_words[spoken_idx]).ratio()
            if ratio >= 0.75:
                is_match = True
                spoken_idx += 1
            else:
                # Lookahead 1 word
                if spoken_idx + 1 < len(spoken_words):
                    look_ratio = difflib.SequenceMatcher(None, tw, spoken_words[spoken_idx + 1]).ratio()
                    if look_ratio >= 0.75:
                        is_match = True
                        spoken_idx += 2

        if is_match:
            correct_count += 1
            word_evaluations.append({"word": tw, "status": "correct"})
        else:
            word_evaluations.append({"word": tw, "status": "retry"})

    accuracy = int((correct_count / len(target_words)) * 100)
    
    if accuracy >= 85:
        stars = 3
        badge = "🌟 Super Reader / उत्तम पाठक!"
        cheer = "Wah! Shandaar padha! Aapko 3 taare mile!"
    elif accuracy >= 60:
        stars = 2
        badge = "⭐ Rising Star / होनहार पाठक!"
        cheer = "Bahut badiya prayas! Thoda aur koshish karein!"
    else:
        stars = 1
        badge = "🌱 Little Learner / सीखने वाला!"
        cheer = "Koi baat nahi, aao dobara sunkar bolein!"

    return {
        "accuracy_pct": accuracy,
        "stars": stars,
        "badge": badge,
        "cheer_message": cheer,
        "word_details": word_evaluations,
        "total_words": len(target_words),
        "correct_words": correct_count
    }

def generate_parent_briefing(lesson_title: str, vernacular_lang: str = "hi") -> str:
    """Generates a warm 30-second audio script for parents who don't read English."""
    briefings = {
        "hi": f"नमस्ते अभिभावक जी! आज स्कूल में आपके बच्चे ने '{lesson_title}' के बारे में सीखा। घर पर बच्चे से पूछें कि आज उसने क्या नया सीखा और उसकी प्रशंसा करें। धन्यवाद!",
        "sat": f"ᱡᱚᱦᱟᱨ ᱟᱭᱳ-ᱵᱟᱵᱟ ᱠᱚ! ᱛᱮᱦᱮᱧ ᱟᱥᱲᱟ ᱨᱮ ᱟᱢᱤᱡ ᱜᱤᱫᱽᱨᱟᱹ '{lesson_title}' ᱵᱟᱵᱚᱛ ᱮ ᱪᱮᱫ ᱠᱮᱫᱼᱟ᱾ ᱚᱲᱟᱜ ᱨᱮ ᱟᱡ ᱥᱟᱶ ᱠᱟᱛᱷᱟ ᱢᱮ ᱟᱨ ᱩᱫᱽᱜᱟᱹᱣ ᱮ ᱢᱮ᱾ ᱥᱟᱨᱦᱟᱣ!",
        "bn": f"নমস্কার অভিভাবক মশাই! আজ স্কুলে আপনার সন্তান '{lesson_title}' সম্পর্কে শিখেছে। বাড়িতে তার কাছে জানতে চান সে কি শিখেছে এবং তাকে উৎসাহিত করুন। ধন্যবাদ!",
        "or": f"ନମସ୍କାର ଅଭିଭାବକ ମହାଶୟ! ଆଜି ବିଦ୍ୟାଳୟରେ ଆପଣଙ୍କ ପିଲା '{lesson_title}' ବିଷୟରେ ଶିଖିଲା। ଘରେ ତାକୁ ପଚାରନ୍ତୁ ଏବଂ ତା'ର ପ୍ରଶଂସା କରନ୍ତୁ। ଧନ୍ୟବାଦ!",
        "khr": f"प्रणाम अभिभावक जी! आज स्कूल में तोहर छौवा '{lesson_title}' के बारे में सिखलइ। घर में ओकरा से जरूर पूछिया अउर ओकर हौसला बढ़इहा। धन्यवाद!",
        "sck": f"जोहार अभिभावक जी! आज स्कूल में राउर छौवा '{lesson_title}' के बारे में सीखलक। घर में ओकर से पूछू अउर शाबाशी देऊ। जोहार!",
        "ho": f"ᱡᱚᱦᱟᱨ ᱟᱭᱳ-ᱵᱟᱵᱟ ᱠᱚ! ᱛᱤᱥᱤᱝ ᱟᱥᱲᱟ ᱨᱮ ᱟᱢᱤᱡ ᱜᱤᱫᱽᱨᱟᱹ '{lesson_title}' ᱪᱮᱛᱟᱱ ᱨᱮ ᱪᱮᱫ ᱠᱮᱫᱟ᱾ ᱚᱲᱟᱜ ᱨᱮ ᱟᱡ ᱥᱟᱶ ᱠᱩᱞᱤ ᱢᱮ ᱟᱨ ᱥᱟᱨᱦᱟᱣ ᱮ ᱢᱮ᱾ ᱡᱚᱦᱟᱨ!",
        "unr": f"जोहार अभिभावक को! तिशिंग स्कूल रे आपन बच्चा '{lesson_title}' के बारे में सिखलई। घर रे ओकर से जरूर पूछू। जोहार!",
        "kru": f"जोहार अभिभावक जी! ईंज स्कूल नू अक्कू बच्चा '{lesson_title}' गही बारे नू सीखचा। एड़पा नू ओकर से हूरहा। जोहार!"
    }
    return briefings.get(vernacular_lang, briefings["hi"])
