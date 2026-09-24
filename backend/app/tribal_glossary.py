"""
Indigenous and Vernacular Language Glossary for Jharkhand & Eastern India.
Provides offline fallback dictionaries, phrasebanks, and pedagogical vocabulary
for languages where standard MT APIs (including Bhashini) may have sparse coverage
or during offline classroom sessions:
  - Santali (Ol Chiki script & Latin transliteration)
  - Ho (Warang Citi & Devanagari/Latin)
  - Mundari
  - Kurukh / Oraon
  - Khortha
  - Nagpuri / Sadri
  - Hindi, Bengali, Odia
"""

TRIBAL_LANGUAGES_METADATA = {
    "sat": {
        "name_en": "Santali",
        "name_native": "ᱥᱟᱱᱛᱟᱲᱤ",
        "script": "Ol Chiki",
        "region": "Santhal Pargana, Jharkhand",
        "official_status": "8th Schedule of Indian Constitution",
    },
    "ho": {
        "name_en": "Ho",
        "name_native": "ᱦᱳ / हो",
        "script": "Warang Citi / Devanagari",
        "region": "Kolhan Division, West Singhbhum, Jharkhand",
        "official_status": "Indigenous Tribal Language",
    },
    "unr": {
        "name_en": "Mundari",
        "name_native": "মুণ্ডারী / मुंडारी",
        "script": "Devanagari / Bengali / Ol Onol",
        "region": "Ranchi, Khunti, Jharkhand",
        "official_status": "Austroasiatic / Munda Family",
    },
    "kru": {
        "name_en": "Kurukh (Oraon)",
        "name_native": "कुड़ुख़",
        "script": "Tolong Siki / Devanagari",
        "region": "Chota Nagpur, Gumla, Lohardaga, Jharkhand",
        "official_status": "Dravidian Family Tribal Language",
    },
    "khr": {
        "name_en": "Khortha",
        "name_native": "खोरठा",
        "script": "Devanagari",
        "region": "North Chotanagpur, Dhanbad, Bokaro, Hazaribagh",
        "official_status": "Major Regional Vernacular",
    },
    "sck": {
        "name_en": "Nagpuri (Sadri)",
        "name_native": "नागपुरी (सादरी)",
        "script": "Devanagari",
        "region": "South Chotanagpur, Ranchi, Simdega",
        "official_status": "Lingua Franca of Jharkhand",
    },
    "hi": {
        "name_en": "Hindi",
        "name_native": "हिन्दी",
        "script": "Devanagari",
        "region": "Pan-India / Jharkhand Official",
        "official_status": "Union Official Language",
    },
    "bn": {
        "name_en": "Bengali",
        "name_native": "বাংলা",
        "script": "Bengali",
        "region": "East Singhbhum, Jamtara, West Bengal",
        "official_status": "8th Schedule of Indian Constitution",
    },
    "or": {
        "name_en": "Odia",
        "name_native": "ଓଡ଼ିଆ",
        "script": "Odia",
        "region": "Saraikela-Kharsawan, Odisha border",
        "official_status": "8th Schedule / Classical Language",
    },
    "en": {
        "name_en": "English",
        "name_native": "English",
        "script": "Latin",
        "region": "Curriculum Language",
        "official_status": "Associate Official Language",
    }
}

# Core vocabulary curated for Class 1-5 Primary School Concepts
CURATED_VOCABULARY = [
    {
        "concept": "sun",
        "category": "nature",
        "en": "Sun",
        "hi": "सूरज (Suraj)",
        "sat": "ᱥᱤᱧ ᱪᱟᱸᱫᱚ (Sing Chando)",
        "ho": "ᱥᱤᱝᱜᱤ (Singi)",
        "unr": "सिंगी (Singi)",
        "kru": "बिड़ी (Bidi)",
        "khr": "रोइद / सुरुज (Roid / Suruj)",
        "sck": "सूरज (Suraj)",
        "bn": "সূর্য (Surjo)",
        "or": "ସୂର୍ଯ୍ୟ (Surjya)",
        "meaning_for_kids": "Suraj hamen dhoop aur roshni deta hai, jisse paudhe apna khana banate hain."
    },
    {
        "concept": "water",
        "category": "nature",
        "en": "Water",
        "hi": "पानी (Paani)",
        "sat": "ᱫᱟᱜ (Daag)",
        "ho": "ᱫᱟᱜ (Daah)",
        "unr": "दाः (Daah)",
        "kru": "अम्म (Amm)",
        "khr": "पानी (Paani)",
        "sck": "पानी (Paani)",
        "bn": "জল (Jol)",
        "or": "ପାଣି (Paani)",
        "meaning_for_kids": "Paani peene ke liye aur paudhon ko badhane ke liye zaroori hai."
    },
    {
        "concept": "tree",
        "category": "nature",
        "en": "Tree / Plant",
        "hi": "पेड़ / पौधा (Ped / Paudha)",
        "sat": "ᱫᱟᱨᱮ (Dare)",
        "ho": "ᱫᱟᱨᱩ (Daru)",
        "unr": "दारू (Daaru)",
        "kru": "मन्न (Mann)",
        "khr": "गाछ (Gaachh)",
        "sck": "गाछ / पेड़ (Gaachh / Ped)",
        "bn": "গাছ (Gaach)",
        "or": "ଗଛ (Gachha)",
        "meaning_for_kids": "Ped hamen meetha fal aur saaf hawa (oxygen) dete hain."
    },
    {
        "concept": "rain",
        "category": "science",
        "en": "Rain",
        "hi": "बारिश (Baarish)",
        "sat": "ᱫᱟᱜ ᱡᱟᱹᱲᱤ (Daag Jari)",
        "ho": "ᱡᱟᱹᱲᱤ (Jari)",
        "unr": "जाड़ी (Jaadi)",
        "kru": "झड़ी (Jhari)",
        "khr": "बरखा (Barkha)",
        "sck": "बरखा (Barkha)",
        "bn": "বৃষ্টি (Brishti)",
        "or": "ବର୍ଷା (Barsha)",
        "meaning_for_kids": "Aakash ke baadal thande hokar boondon ke roop mein zameen par aate hain."
    },
    {
        "concept": "book",
        "category": "classroom",
        "en": "Book",
        "hi": "किताब / पुस्तक (Kitaab)",
        "sat": "ᱯᱩᱛᱷᱤ (Puthi)",
        "ho": "ᱯᱩᱛᱷᱤ (Puthi)",
        "unr": "पुथी (Puthi)",
        "kru": "पुथी (Puthi)",
        "khr": "किताब (Kitaab)",
        "sck": "किताब / पोथी (Kitaab / Pothi)",
        "bn": "বই (Boi)",
        "or": "ବହି (Bahi)",
        "meaning_for_kids": "Kitaab mein sundar kahaniyan aur gyan hota hai."
    },
    {
        "concept": "school",
        "category": "classroom",
        "en": "School",
        "hi": "विद्यालय / स्कूल (School)",
        "sat": "ᱟᱥᱲᱟ (Ashra)",
        "ho": "ᱤᱛᱩᱱ ᱟᱥᱲᱟ (Itun Ashra)",
        "unr": "इतुन आषड़ा (Itun Ashra)",
        "kru": "स्कूल / पढ़ना अखाड़ा (School)",
        "khr": "स्कूल / पाठशाला (Paathshala)",
        "sck": "स्कूल (School)",
        "bn": "বিদ্যালয় / স্কুল (Bidyalay)",
        "or": "ବିଦ୍ୟାଳୟ (Bidyalaya)",
        "meaning_for_kids": "Jahan hum dosto ke saath khelte aur nayi cheezein seekhte hain."
    },
    {
        "concept": "teacher",
        "category": "classroom",
        "en": "Teacher",
        "hi": "शिक्षक / गुरुजी (Guruji / Teacher)",
        "sat": "ᱢᱟᱪᱮᱫ (Machet)",
        "ho": "ᱢᱟᱪᱮᱫ (Machet)",
        "unr": "माचेत (Machet)",
        "kru": "मास्टर / गुरु (Guru)",
        "khr": "मास्टर जी (Master Ji)",
        "sck": "गुरुजी (Guruji)",
        "bn": "শিক্ষক / দিদিমণি (Shikkhok)",
        "or": "ଶିକ୍ଷକ (Shikshyaka)",
        "meaning_for_kids": "Jo hamen pyaar se nayi kahaniyan aur path sikhate hain."
    },
    {
        "concept": "friend",
        "category": "social",
        "en": "Friend",
        "hi": "दोस्त / मित्र (Dost / Mitr)",
        "sat": "ᱜᱟᱛᱮ (Gate)",
        "ho": "ᱡᱩᱲᱤ (Juri)",
        "unr": "जोड़ी (Jodi)",
        "kru": "संगिया (Sangiya)",
        "khr": "संगी (Sangi)",
        "sck": "संगी / साथी (Sangi / Saathi)",
        "bn": "বন্ধু (Bondhu)",
        "or": "ସାଙ୍ଗ (Saanga)",
        "meaning_for_kids": "Jiske saath hum tiffin baant-te hain aur khushi se khelte hain."
    },
    {
        "concept": "good_morning",
        "category": "greetings",
        "en": "Good Morning / Greetings",
        "hi": "नमस्ते / सुप्रभात (Namaste)",
        "sat": "ᱡᱚᱦᱟᱨ (Johar)",
        "ho": "ᱡᱚᱦᱟᱨ (Johar)",
        "unr": "जोहार (Johar)",
        "kru": "जय जोहार (Jay Johar)",
        "khr": "प्रणाम / जोहार (Johar)",
        "sck": "जोहार / प्रणाम (Johar)",
        "bn": "নমস্কার / সুপ্রভাত (Nomoshkar)",
        "or": "ନମସ୍କାର (Namaskara)",
        "meaning_for_kids": "Bado aur dosto ko aadar se pranam kehna."
    },
    {
        "concept": "earth",
        "category": "science",
        "en": "Earth",
        "hi": "धरती (Dharti)",
        "sat": "ᱫᱷᱟᱹᱨᱛᱤ (Dharti)",
        "ho": "ᱫᱷᱟᱹᱨᱛᱤ (Dharti)",
        "unr": "धरती (Dharti)",
        "kru": "धरती (Dharti)",
        "khr": "धरती (Dharti)",
        "sck": "भुइयां / धरती (Bhuiyan / Dharti)",
        "bn": "পৃথিবী (Prithibi)",
        "or": "ପୃଥିବୀ (Pruthibi)",
        "meaning_for_kids": "Hamara pyaara ghar jahan hum sab rehte hain."
    }
]

# Common foundational classroom sentences translated for instant offline fallback
COMMON_LESSON_SENTENCES = [
    {
        "id": "welcome_class",
        "en": "Welcome to school children! Today we will learn something new and fun.",
        "hi": "बच्चों स्कूल में आपका स्वागत है! आज हम कुछ नया और मजेदार सीखेंगे।",
        "sat": "ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱟᱥᱲᱟ ᱛᱮ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ! ᱛᱮᱦᱮᱧ ᱵᱚᱱ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱟᱶᱟ ᱟᱨ ᱨᱟᱹᱥᱠᱟᱹ ᱪᱮᱫᱚᱜᱼᱟ᱾",
        "ho": "ᱜᱤᱫᱤᱨ ᱠᱚ ᱟᱥᱲᱟ ᱨᱮ ᱡᱚᱦᱟᱨ! ᱛᱤᱥᱤᱝ ᱟᱵᱩ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱟᱶᱟ ᱠᱟᱡᱤ ᱪᱮᱫᱚᱜᱼᱟ᱾",
        "unr": "होन्हार को आषड़ा रे जोहार! तिशिंग अबु मियद नवा काजी चेदोआ।",
        "kru": "खद्दर मन स्कूल नू जोहार! इन्ना नाम कुछु नया अरा दव कत्था सिकभो।",
        "khr": "छौआ सभ, स्कूल में तोहीन के सुवागत हे! आज हमनी कुछ नवा अउर मजेदार सिखबई।",
        "sck": "छौवा मनके स्कूल में जोहार! आज हमरे कुछु नवा अउर बेस चीज सीखब।",
        "bn": "বাচ্চারা স্কুলে তোমাদের স্বাগতম! আজ আমরা নতুন ও মজার কিছু শিখব।",
        "or": "ପିଲାମାନେ ବିଦ୍ୟାଳୟକୁ ସ୍ୱାଗତ! ଆଜି ଆମେ କିଛି ନୂଆ ଓ ମଜାଦାର ଶିଖିବା।"
    },
    {
        "id": "plants_sunlight",
        "en": "Plants need sunlight and water to make food.",
        "hi": "पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।",
        "sat": "ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾",
        "ho": "ᱫᱟᱨᱩ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾",
        "unr": "दारू को जोमा बाई लागिन सिंगी मारसाल आर दाः लाकतीया।",
        "kru": "मन्न मनके खना कमआगे बिड़ी रौद अरा अम्म चाहि।",
        "khr": "गाछ-बिरिछ के आपन खाना बनावे ले घाम (रौद) अउर पानी के जरूरत होवऽ हे।",
        "sck": "गाछ मनके आपन भोजन बनाएक ले रौद अउर पानी चाही।",
        "bn": "গাছের খাদ্য তৈরির জন্য সূর্যের আলো এবং জলের প্রয়োজন।",
        "or": "ଗଛକୁ ଖାଦ୍ୟ ତିଆରି କରିବା ପାଇଁ ସୂର୍ଯ୍ୟାଲୋକ ଓ ପାଣି ଦରକାର।"
    },
    {
        "id": "read_together",
        "en": "Open your book and let us read this story together.",
        "hi": "अपनी किताब खोलो और आओ मिलकर यह कहानी पढ़ें।",
        "sat": "ᱟᱢᱟᱜ ᱯᱩᱛᱷᱤ ᱡᱷᱤᱡᱽ ᱢᱮ ᱟᱨ ᱫᱮᱞᱟ ᱵᱚᱱ ᱱᱚᱶᱟ ᱠᱟᱹᱦᱱᱤ ᱢᱤᱫ ᱛᱮ ᱵᱚᱱ ᱯᱟᱲᱦᱟᱣᱼᱟ᱾",
        "ho": "ᱟᱢᱟᱜ ᱯᱩᱛᱷᱤ ᱠᱩᱞᱤ ᱢᱮ ᱟᱨ ᱫᱮᱞᱟ ᱱᱮᱱ ᱠᱟᱹᱦᱱᱤ ᱯᱟᱲᱦᱟᱣ ᱢᱮ᱾",
        "unr": "आमाः पुथी झिज मे आर देला नेन कहानी मिद ते पढ़वआ।",
        "kru": "तांग्है पुथी उथरा अरा बरा नाम संगे ई खीरी पढा।",
        "khr": "आपन किताब खोला अउर आवा मिल के ई कहानी पढ़ल जाय।",
        "sck": "आपन किताब खोलू अउर आवा संगे ई कहानी पढ़ब।",
        "bn": "তোমার বই খোলো এবং এসো আমরা একসঙ্গে এই গল্পটি পড়ি।",
        "or": "ତୁମ ବହି ଖୋଲ ଏବଂ ଆସ ଆମେ ଏକାଠି ଏହି ଗଳ୍ପ ପଢ଼ିବା।"
    }
]

def find_tribal_word(query: str, target_lang: str = "sat") -> dict:
    """Finds a word or concept in the offline tribal glossary."""
    query_lower = query.strip().lower()
    for item in CURATED_VOCABULARY:
        if (
            item["concept"].lower() == query_lower
            or query_lower in item["en"].lower()
            or query_lower in item["hi"].lower()
        ):
            return {
                "concept": item["concept"],
                "english": item["en"],
                "hindi": item["hi"],
                "target_lang": target_lang,
                "translation": item.get(target_lang, item["hi"]),
                "kids_explanation": item["meaning_for_kids"],
                "category": item["category"]
            }
    return None

def get_common_phrases(target_lang: str = "sat"):
    """Returns foundational classroom phrases for the given language."""
    results = []
    for s in COMMON_LESSON_SENTENCES:
        results.append({
            "id": s["id"],
            "english": s["en"],
            "hindi": s["hi"],
            "target": s.get(target_lang, s["hi"])
        })
    return results


OL_CHIKI_TO_DEVANAGARI = {
    'ᱚ': 'अ', 'ᱛ': 'त', 'ᱜ': 'ग', 'ᱝ': 'ं', 'ᱞ': 'ल',
    'ᱟ': 'आ', 'ᱠ': 'क', 'ᱡ': 'ज', 'ᱢ': 'म', 'ᱣ': 'व',
    'ᱤ': 'इ', 'ᱥ': 'स', 'ᱦ': 'ह', 'ᱧ': 'ञ', 'ᱨ': 'र',
    'ᱩ': 'उ', 'ᱪ': 'च', 'ᱫ': 'द', 'ᱬ': 'ण', 'ᱭ': 'य',
    'ᱮ': 'ए', 'ᱯ': 'प', 'ᱰ': 'ड', 'ᱱ': 'न', 'ᱲ': 'ड़',
    'ᱳ': 'ओ', 'ᱴ': 'ट', 'ᱵ': 'ब', 'ᱶ': 'ं', 'ᱷ': 'ह',
    'ᱸ': 'ं', 'ᱹ': '', 'ᱺ': '', 'ᱻ': '', 'ᱼ': '', 'ᱽ': '',
    '᱾': '।', '᱿': '।'
}

def ol_chiki_to_phonetic(text: str) -> str:
    """Converts Ol Chiki (Santali) text to natural phonetic Devanagari for neural voice synthesis."""
    if not text:
        return ""
    # Check if text contains any Ol Chiki characters (U+1C50 to U+1C7F)
    has_ol_chiki = any('\u1C50' <= char <= '\u1C7F' for char in text)
    if not has_ol_chiki:
        return text
    converted = "".join(OL_CHIKI_TO_DEVANAGARI.get(c, c) for c in text)
    return converted
