"""
Matrubhasa AI — Jharkhand JCERT / NCERT Primary Curriculum Dataset (Classes 1–5)
Provides comprehensive, syllabus-aligned bilingual notebooks, chapter explanations,
vernacular translations, visual vocabulary, word-to-word translation maps,
and practice exercises for rural and tribal students across all subjects:
  1. पर्यावरण एवं परिवेश / आस-पास (EVS / Science)
  2. गणित का जादू (Mathematics)
  3. भाषा / हिन्दी - रिमझिम / वीणा (Hindi Language)
  4. English - Mridang / Marigold (English Language)
Supports 9 regional & tribal languages:
  Santali (sat - Ol Chiki), Ho (ho), Mundari (unr), Kurukh (kru), Kharia (khr),
  Khortha (sck), Bengali (bn), Odia (or), Hindi (hi), and English (en).
"""

from typing import List, Dict, Optional

# Comprehensive global vocabulary mapping for word-to-word instant translation lookup
GLOBAL_WORD_DICTIONARY: Dict[str, Dict[str, str]] = {
    # Nature & Living
    "family": {"en": "Family", "hi": "परिवार", "phonetic": "Gharonj", "sat": "ᱜᱷᱟᱨᱚᱸᱡᱽ", "ho": "ᱜᱷᱟᱨᱚᱸᱡᱽ", "unr": "परिवार", "kru": "परिवार", "khr": "परिवार", "sck": "परिवार", "bn": "পরিবার", "or": "ପରିବାର", "meaning": "माता-पिता और बच्चे"},
    "home": {"en": "Home / House", "hi": "घर", "phonetic": "Orak", "sat": "ᱚᱲᱟᱜ", "ho": "ᱚᱲᱟᱜ", "unr": "ओड़ाः", "kru": "एड़पा", "khr": "घर", "sck": "घर", "bn": "বাড়ি", "or": "ଘର", "meaning": "सुरक्षित बसेरा"},
    "love": {"en": "Love / Affection", "hi": "प्यार / स्नेह", "phonetic": "Dular", "sat": "ᱫᱩᱞᱟᱹᱲ", "ho": "ᱫᱩᱞᱟᱹᱲ", "unr": "दुलार", "kru": "दुलार", "khr": "प्यार", "sck": "मया-दुलार", "bn": "ভালোবাসা", "or": "ସ୍ନେହ", "meaning": "आपसी अपनापन"},
    "tree": {"en": "Tree", "hi": "पेड़ / वृक्ष", "phonetic": "Dare", "sat": "ᱫᱟᱨᱮ", "ho": "ᱫᱟᱨᱩ", "unr": "दारू", "kru": "मन्न", "khr": "गाछ", "sck": "गाछ-बिरिछ", "bn": "গাছ", "or": "ଗଛ", "meaning": "फल-छाया देने वाला वृक्ष"},
    "plant": {"en": "Plant", "hi": "पौधा", "phonetic": "Dare", "sat": "ᱫᱟᱨᱮ", "ho": "ᱫᱟᱨᱩ", "unr": "दारू", "kru": "मन्न", "khr": "पौधा", "sck": "पौधा", "bn": "চারাগাছ", "or": "ଗଛ", "meaning": "छोटा वनस्पति"},
    "water": {"en": "Water", "hi": "पानी / जल", "phonetic": "Daag", "sat": "ᱫᱟᱜ", "ho": "ᱫᱟᱜ", "unr": "दाः", "kru": "अम्म", "khr": "पानी", "sck": "पानी", "bn": "জল", "or": "ପାଣି", "meaning": "जीवन रस"},
    "sun": {"en": "Sun", "hi": "सूरज / सूर्य", "phonetic": "Sing Chando", "sat": "ᱥᱤᱧ ᱪᱟᱸᱫᱚ", "ho": "ᱥᱤᱝᱜᱤ", "unr": "सिंगी", "kru": "बिड़ी", "khr": "सुरुज", "sck": "सूरज", "bn": "সূর্য", "or": "ସୂର୍ଯ୍ୟ", "meaning": "प्रकाशदाता तारा"},
    "sunlight": {"en": "Sunlight", "hi": "धूप / प्रकाश", "phonetic": "Marsal", "sat": "ᱢᱟᱨᱥᱟᱞ", "ho": "ᱢᱟᱨᱥᱟᱞ", "unr": "मारसाल", "kru": "रौद", "khr": "घाम", "sck": "रौद", "bn": "সূর্যালোক", "or": "ଖରା", "meaning": "सूरज की रोशनी"},
    "flower": {"en": "Flower", "hi": "फूल / पुष्प", "phonetic": "Baha", "sat": "ᱵᱟᱦᱟ", "ho": "ᱵᱟᱦᱟ", "unr": "बाहा", "kru": "पूप", "khr": "फूल", "sck": "फूल", "bn": "ফুল", "or": "ଫୁଲ", "meaning": "सुगंधित पुष्प"},
    "leaf": {"en": "Leaf", "hi": "पत्ती / पत्ता", "phonetic": "Sakam", "sat": "ᱥᱟᱠᱟᱢ", "ho": "ᱥᱟᱠᱟᱢ", "unr": "साकाम", "kru": "अट्टी", "khr": "पत्ता", "sck": "पत्ती", "bn": "পাতা", "or": "ପତ୍ର", "meaning": "पेड़ का भोजन अंग"},
    "soil": {"en": "Soil / Earth", "hi": "मिट्टी", "phonetic": "Hasa", "sat": "ᱦᱟᱥᱟ", "ho": "ᱦᱟᱥᱟ", "unr": "हासा", "kru": "खैखो", "khr": "माटी", "sck": "माटी", "bn": "মাটি", "or": "ମାଟି", "meaning": "धरती की उपजाऊ मिट्टी"},
    "food": {"en": "Food", "hi": "भोजन / खाना", "phonetic": "Jomag", "sat": "ᱡᱚᱢᱟᱜ", "ho": "ᱡᱚᱢᱟ", "unr": "जोमा", "kru": "खना", "khr": "खाना", "sck": "भोजन", "bn": "খাবার", "or": "ଖାଦ୍ୟ", "meaning": "आहार"},
    "children": {"en": "Children", "hi": "बच्चे", "phonetic": "Gidra ko", "sat": "ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ", "ho": "ᱜᱤᱫᱤᱨ ᱠᱚ", "unr": "होन्हार को", "kru": "खद्दर", "khr": "छौआ-पुता", "sck": "छौवा मन", "bn": "শিশুরা", "or": "ପିଲାମାନେ", "meaning": "नन्हे बालक-बालिकाएं"},
    "school": {"en": "School", "hi": "विद्यालय / स्कूल", "phonetic": "Asra", "sat": "ᱟᱥᱲᱟ", "ho": "ᱟᱥᱲᱟ", "unr": "आषड़ा", "kru": "स्कूल", "khr": "स्कूल", "sck": "स्कूल", "bn": "বিদ্যালয়", "or": "ବିଦ୍ୟାଳୟ", "meaning": "शिक्षा का मंदिर"},
    "teacher": {"en": "Teacher", "hi": "शिक्षक / गुरुजी", "phonetic": "Machet", "sat": "ᱢᱟᱪᱮᱛ", "ho": "ᱢᱟᱪᱮᱛ", "unr": "माचेत", "kru": "गुरुजी", "khr": "मास्टर बाबू", "sck": "मास्टर", "bn": "শিক্ষক", "or": "ଶିକ୍ଷକ", "meaning": "ज्ञान देने वाले"},
    "book": {"en": "Book", "hi": "किताब / पुस्तक", "phonetic": "Pothab", "sat": "ᱯᱚᱛᱷᱚᱵ", "ho": "ᱯᱚᱛᱚᱵ", "unr": "पोतोब", "kru": "किताब", "khr": "किताब", "sck": "किताब", "bn": "বই", "or": "ବହି", "meaning": "पढ़ने की पुस्तक"},
    "friend": {"en": "Friend", "hi": "मित्र / दोस्त", "phonetic": "Gate", "sat": "ᱜᱟᱛᱮ", "ho": "ᱡᱩᱲᱤ", "unr": "जोड़ी", "kru": "संगिया", "khr": "संगी", "sck": "संगी", "bn": "বন্ধু", "or": "ବନ୍ଧୁ", "meaning": "सच्चा साथी"},
    "bird": {"en": "Bird", "hi": "पक्षी / चिड़िया", "phonetic": "Chene", "sat": "ᱪᱮᱬᱮ", "ho": "ᱪᱮᱬᱮ", "unr": "चेणे", "kru": "ओड़ा", "khr": "चिरई", "sck": "चिरई", "bn": "পাখি", "or": "ପକ୍ଷୀ", "meaning": "उड़ने वाला जीव"},
    "fish": {"en": "Fish", "hi": "मछली", "phonetic": "Haku", "sat": "ᱦᱟᱹᱠᱩ", "ho": "ᱦᱟᱹᱠᱩ", "unr": "हाकु", "kru": "ईंजो", "khr": "मछरी", "sck": "मछरी", "bn": "মাছ", "or": "ମାଛ", "meaning": "जल का जीव"},
    "cow": {"en": "Cow", "hi": "गाय / गौमाता", "phonetic": "Gai", "sat": "ᱜᱟᱹᱭ", "ho": "ᱜᱟᱹᱭ", "unr": "गाई", "kru": "ओई", "khr": "गैया", "sck": "गुरू-गाई", "bn": "গরু", "or": "ଗାଈ", "meaning": "दूध देने वाली गाय"},
    "dog": {"en": "Dog", "hi": "कुत्ता", "phonetic": "Seta", "sat": "ᱥᱮᱛᱟ", "ho": "ᱥᱮᱛᱟ", "unr": "सेता", "kru": "अल्ला", "khr": "कुकुर", "sck": "कुकुर", "bn": "কুকুর", "or": "କୁକୁର", "meaning": "वफादार पालतू पशु"},
    "river": {"en": "River", "hi": "नदी / सरिता", "phonetic": "Gada", "sat": "ᱜᱟᱰᱟ", "ho": "ᱜᱟᱲᱟ", "unr": "गड़ा", "kru": "नदी", "khr": "नदी", "sck": "नदी-नाला", "bn": "নদী", "or": "ନଦୀ", "meaning": "बहती जलधारा"},
    "rain": {"en": "Rain", "hi": "बारिश / वर्षा", "phonetic": "Jari", "sat": "ᱡᱟᱹᱲᱤ", "ho": "ᱡᱟᱹᱲᱤ", "unr": "जाड़ी", "kru": "झरी", "khr": "बरसात", "sck": "बरखा", "bn": "বৃষ্টি", "or": "ବର୍ଷା", "meaning": "मेघों से बरसता जल"},
    "cloud": {"en": "Cloud", "hi": "बादल / मेघ", "phonetic": "Rimil", "sat": "ᱨᱤᱢᱤᱞ", "ho": "ᱨᱤᱢᱤᱞ", "unr": "रिमिल", "kru": "बादल", "khr": "बदली", "sck": "बादल", "bn": "মেঘ", "or": "ମେଘ", "meaning": "आकाश के मेघ"},
    "village": {"en": "Village", "hi": "गाँव / ग्राम", "phonetic": "Aatu", "sat": "ᱟᱹᱛᱩ", "ho": "ᱦᱟᱛᱩ", "unr": "हतू", "kru": "पद्धा", "khr": "गाँव", "sck": "गाँव-घर", "bn": "গ্রাম", "or": "ଗାଁ", "meaning": "ग्रामीण बस्ती"},
    "farmer": {"en": "Farmer", "hi": "किसान", "phonetic": "Chasi", "sat": "ᱪᱟᱹᱥᱤ", "ho": "ᱠᱤᱥᱟᱹᱱ", "unr": "चासी", "kru": "उइय्यार", "khr": "किसान", "sck": "किसान", "bn": "কৃষক", "or": "କୃଷକ", "meaning": "अन्नदाता"},
    "market": {"en": "Weekly Market", "hi": "हाट / बाज़ार", "phonetic": "Haat", "sat": "ᱦᱟᱴ", "ho": "ᱦᱟᱴ", "unr": "हाट", "kru": "पेठिया", "khr": "हतिया", "sck": "हाट-बाजार", "bn": "হাট", "or": "ହାଟ", "meaning": "साप्ताहिक ग्रामीण बाजार"},
    # Numbers
    "one": {"en": "One (1)", "hi": "एक (१)", "phonetic": "Mit", "sat": "ᱢᱤᱫ", "ho": "ᱢᱤᱭᱟᱹᱫᱽ", "unr": "मियद", "kru": "ओन्द", "khr": "एगो", "sck": "एके", "bn": "এক", "or": "ଏକ", "meaning": "संख्या १"},
    "two": {"en": "Two (2)", "hi": "दो (२)", "phonetic": "Bar", "sat": "ᱵᱟᱨ", "ho": "ᱵᱟᱨᱤᱭᱟ", "unr": "बरिया", "kru": "ओंड़ंग्गो", "khr": "दुगो", "sck": "दुइ", "bn": "দুই", "or": "ଦୁଇ", "meaning": "संख्या २"},
    "three": {"en": "Three (3)", "hi": "तीन (३)", "phonetic": "Pe", "sat": "ᱯᱮ", "ho": "ᱯᱮᱭᱟ", "unr": "पेया", "kru": "मूंद", "khr": "तीनगो", "sck": "तीन", "bn": "তিন", "or": "ତିନି", "meaning": "संख्या ३"},
    "four": {"en": "Four (4)", "hi": "चार (४)", "phonetic": "Pon", "sat": "ᱯᱩᱱ", "ho": "ᱯᱩᱱᱤᱭᱟ", "unr": "पुनिया", "kru": "नाख", "khr": "चारगो", "sck": "चार", "bn": "চার", "or": "ଚାରି", "meaning": "संख्या ४"},
    "five": {"en": "Five (5)", "hi": "पाँच (५)", "phonetic": "More", "sat": "ᱢᱚᱬᱮ", "ho": "ᱢᱚᱬᱮᱭᱟ", "unr": "मोड़ेया", "kru": "पंचे", "khr": "पाँचगो", "sck": "पाँच", "bn": "পাঁচ", "or": "ପାଞ୍ଚ", "meaning": "संख्या ५"},
    "ten": {"en": "Ten (10)", "hi": "दस (१०)", "phonetic": "Gel", "sat": "ᱜᱮᱞ", "ho": "ᱜᱮᱞ", "unr": "गेल", "kru": "दसे", "khr": "दसगो", "sck": "दस", "bn": "দশ", "or": "ଦଶ", "meaning": "संख्या १०"},
    "hundred": {"en": "Hundred (100)", "hi": "सौ / शतक (१००)", "phonetic": "Sae", "sat": "ᱥᱟᱭ", "ho": "ᱥᱟᱭ", "unr": "साय", "kru": "सय", "khr": "सउ", "sck": "सउ", "bn": "একশত", "or": "ଶହେ", "meaning": "संख्या १००"}
}


# NIPUN Bharat Foundational Learning Outcomes Framework (NEP 2020 Aligned)
NIPUN_FLN_FRAMEWORK = {
    "L-FLN-01": {"domain": "Oral Language", "title_hi": "मौखिक भाषा विकास एवं पारिवारिक संवाद", "title_en": "Oral Language Development & Dialogue"},
    "L-FLN-02": {"domain": "Phonics & Word Reading", "title_hi": "ध्वनि जागरूकता एवं वर्ण-ध्वनि संबंध", "title_en": "Phonological Awareness & Phonics"},
    "L-FLN-03": {"domain": "Reading Comprehension", "title_hi": "चित्र पठन एवं प्रारंभिक समझ", "title_en": "Picture Reading & Emergent Comprehension"},
    "L-FLN-04": {"domain": "Folk Literature & Expression", "title_hi": "मातृभाषा लोक-कथा एवं अभिव्यक्ति", "title_en": "Vernacular Folk Narrative & Expression"},
    "M-FLN-01": {"domain": "Foundational Numeracy", "title_hi": "मूर्त वस्तुओं से संख्या ज्ञान १-२०", "title_en": "Concrete Number Sense 1-20"},
    "M-FLN-02": {"domain": "Applied Arithmetic", "title_hi": "जोड़, घटाव एवं स्थानीय मान", "title_en": "Basic Addition, Subtraction & Place Value"},
    "M-FLN-03": {"domain": "Spatial & Measurement", "title_hi": "आकार, स्थान एवं स्थानीय मापन", "title_en": "Shapes, Space & Local Measurement"},
    "E-FLN-01": {"domain": "Nature & Living", "title_hi": "प्राकृतिक परिवेश एवं पेड़-पौधे", "title_en": "Natural Environment & Flora"},
    "E-FLN-02": {"domain": "Water & Weather", "title_hi": "जल, मौसम एवं प्राकृतिक चक्र", "title_en": "Water Cycle & Weather Dynamics"},
    "E-FLN-03": {"domain": "Community & Culture", "title_hi": "सामुदायिक जीवन एवं स्थानीय संस्कृति", "title_en": "Community Life & Local Heritage"}
}

CURRICULUM_CHAPTERS: List[Dict] = [
    # =========================================================================
    # CLASS 1 (Grade 1 / Bal Vatika)
    # =========================================================================
    {
        "id": "cl1_evs_ch1",
        "nipun_code": "L-FLN-01",
        "nipun_outcome": "मौखिक भाषा विकास एवं पारिवारिक संवाद (Oral Language & Family Dialogue)",
        "grade": 1,
        "grade_label": "कक्षा 1 (Class 1)",
        "subject": "evs",
        "subject_name": "पर्यावरण एवं परिवेश (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 1,
        "title_hi": "हमारा प्यारा परिवार और घर",
        "title_en": "Our Loving Family and Home",
        "concept_summary": "परिवार में माता-पिता, दादा-दादी और भाई-बहन मिलकर प्यार से रहते हैं और एक-दूसरे की मदद करते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Our home is where our family lives together with love and care.",
                "hi": "हमारा घर वह प्यारी जगह है जहाँ हमारा परिवार मिलकर प्यार और स्नेह से रहता है।",
                "sat": "ᱟᱵᱚᱣᱟᱜ ᱚᱲᱟᱜ ᱫᱚ ᱚᱱᱟ ᱡᱟᱭᱜᱟ ᱠᱟᱱᱟ ᱡᱟᱦᱟᱸ ᱨᱮ ᱟᱵᱚ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱢᱤᱫ ᱛᱮ ᱫᱩᱞᱟᱹᱲ ᱛᱮ ᱵᱚᱱ ᱛᱟᱦᱮᱸᱱᱟ᱾",
                "ho": "ᱟᱵᱩᱣᱟᱜ ᱚᱲᱟᱜ ᱫᱚ ᱱᱮᱱ ᱡᱟᱭᱜᱟ ᱠᱟᱱᱟ ᱡᱟᱦᱟᱸ ᱨᱮ ᱟᱵᱩ ᱦᱟᱛᱩ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱫᱩᱞᱟᱹᱲ ᱛᱮ ᱵᱚᱱ ᱛᱟᱦᱮᱸᱱᱟ᱾",
                "unr": "अबुवाः ओड़ाः दो नेन दाया जायगा तना जहाँ अबु परिवार मिद ते दुलार तेबो ताईना।",
                "kru": "नामगै एड़पा आ गद्दी तली एकासन नामगै परिवार संगे दुलार ती रइना।",
                "khr": "हमर घर उहे सुंदर जगह हे जहाँ हमर पूरा परिवार मिल-जुल के प्यार से रहे हे।",
                "sck": "हमर घर उहे बेस जगह हे जहाँ हमर परिवार संगे मया-दुलार से रहेला।",
                "bn": "আমাদের বাড়ি সেই ভালোবাসার জায়গা যেখানে আমাদের পরিবার একসঙ্গে পরম যত্নে বাস করে।",
                "or": "ଆମ ଘର ହେଉଛି ସେହି ସ୍ଥାନ ଯେଉଁଠାରେ ଆମ ପରିବାର ପ୍ରେମ ଓ ଯତ୍ନ ସହିତ ଏକାଠି ରୁହନ୍ତି।"
            },
            {
                "id": "p2",
                "en": "Grandmother tells us sweet folk stories at night, and grandfather takes us to the village field.",
                "hi": "दादी माँ रात को हमें मीठी लोक-कहानियाँ सुनाती हैं, और दादा जी हमें गाँव के खेतों में घुमाने ले जाते हैं।",
                "sat": "ᱟᱹᱭᱩᱵ ᱵᱮᱲᱟ ᱵᱩᱰᱷᱤ ᱟᱭᱳ ᱥᱤᱵᱤᱞ ᱠᱟᱹᱦᱱᱤ ᱞᱟᱹᱭ ᱟᱵᱚᱱᱟ, ᱟᱨ ᱦᱟᱲᱟᱢ ᱵᱟᱵᱟ ᱟᱹᱛᱩ ᱠᱷᱮᱛ ᱥᱮᱫ ᱫᱟᱬᱟᱸᱭ ᱤᱫᱤ ᱵᱚᱱᱟ᱾",
                "ho": "ᱟᱹᱭᱩᱵ ᱵᱩᱰᱷᱤ ᱟᱭᱳ ᱥᱤᱵᱤᱞ ᱠᱟᱹᱦᱱᱤ ᱠᱟᱡᱤᱭᱟ, ᱟᱨ ᱦᱟᱲᱟᱢ ᱵᱟᱵᱟ ᱦᱟᱛᱩ ᱵᱟᱹᱫᱽ ᱛᱮ ᱫᱟᱬᱟᱸᱭ ᱤᱫᱤ ᱵᱚᱱᱟ᱾",
                "unr": "आयूमा बुढ़ी आयो सोब कहानी कजीया, आर हाड़ाम बा हतू बद ते दाड़ांय इदीया।",
                "kru": "अड़की बीड़ी बड्डी खीरी कत्था तिंगी, अरा बब्बा नामन पद्ध नु बयडा तरा ओयोस।",
                "khr": "दादी रात के हमनी के मीठ-मीठ कहानी सुनावऽ हथिन, अउर दादा जी खेत घुमावे ले जा हथिन।",
                "sck": "आजी रात के हमके बेस-बेस कहानी सुनावेला, अउर आजा गाँव के खेत-खरिहान घुमावेला।",
                "bn": "দিদিমা রাতে আমাদের মিষ্টি রূপকথার গল্প শোনান এবং দাদু আমাদের গ্রামের সবুজ মাঠে বেড়াতে নিয়ে যান।",
                "or": "ଜେଜେମା ରାତିରେ ଆମକୁ ମିଠା ଲୋକକଥା ଶୁଣାନ୍ତି ଏବଂ ଜେଜେବାପା ଆମକୁ ଗାଁ ବିଲକୁ ବୁଲାଇବାକୁ ନିଅନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "family", "en": "Family", "hi": "परिवार (Parivar)", "sat": "ᱜᱷᱟᱨᱚᱸᱡᱽ (Gharonj)", "meaning": "माता-पिता, दादा-दादी और बच्चे"},
            {"concept": "home", "en": "Home", "hi": "घर (Ghar)", "sat": "ᱚᱲᱟᱜ (Orak)", "meaning": "सुरक्षित और प्यारा बसेरा"},
            {"concept": "love", "en": "Love / Affection", "hi": "प्यार व दुलार (Pyaar)", "sat": "ᱫᱩᱞᱟᱹᱲ (Dular)", "meaning": "आपसी स्नेह और देखभाल"}
        ],
        "abhyas_questions": [
            {"q": "आपके घर में कौन-कौन रहते हैं?", "hint": "माता, पिता, भाई, बहन, दादा, दादी"},
            {"q": "रात को आपको कौन कहानी सुनाता है?", "hint": "दादी माँ या नानी माँ"},
            {"q": "आप अपने परिवार की मदद कैसे करते हैं?", "hint": "छोटे-छोटे कामों में हाथ बँटाकर"}
        ]
    },
    {
        "id": "cl1_evs_ch2",
        "nipun_code": "E-FLN-01",
        "nipun_outcome": "प्राकृतिक परिवेश एवं पेड़-पौधे (Flora & Environment)",
        "grade": 1,
        "grade_label": "कक्षा 1 (Class 1)",
        "subject": "evs",
        "subject_name": "पर्यावरण एवं परिवेश (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 2,
        "title_hi": "पेड़-पौधे और फल-फूल",
        "title_en": "Plants, Trees and Flowers",
        "concept_summary": "हरे पेड़ हमारे सच्चे मित्र हैं। वे हमें मीठे फल, सुंदर फूल, छाया और ताजी हवा देते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Green trees are our best friends. They give us sweet mangoes, shade, and clean air.",
                "hi": "हरे-भरे पेड़ हमारे सबसे सच्चे दोस्त हैं। वे हमें मीठे आम, ठंडी छाया और ताजी हवा देते हैं।",
                "sat": "ᱦᱟᱹᱨᱭᱟᱹᱲ ᱫᱟᱨᱮ ᱠᱚ ᱫᱚ ᱟᱵᱚᱣᱟᱜ ᱥᱟᱹᱨᱤ ᱜᱟᱛᱮ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱩᱱᱠᱩ ᱟᱵᱚ ᱥᱤᱵᱤᱞ ᱩᱞ, ᱩᱢᱩᱞ ᱟᱨ ᱥᱟᱯᱷᱟ ᱦᱚᱭ ᱠᱚ ᱮᱢᱟᱵᱚᱱᱟ᱾",
                "ho": "ᱦᱟᱹᱨᱭᱟᱹᱲ ᱫᱟᱨᱩ ᱠᱚ ᱟᱵᱩᱣᱟᱜ ᱥᱟᱹᱨᱤ ᱡᱩᱲᱤ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱱᱤᱠᱩ ᱥᱤᱵᱤᱞ ᱩᱞ ᱟᱨ ᱥᱟᱯᱷᱟ ᱦᱚᱭ ᱮᱢᱟᱵᱩᱣᱟ᱾",
                "unr": "हरियर दारू को अबुवाः सारी जोड़ी तना। निकु सिबिल उल आर साफा होय एमाबुया।",
                "kru": "हरियर मन्न मन नामगै दव संगिया तली। आर नामन मिठा आम, छाँही अरा निर्मल हवा चीना।",
                "khr": "हरियर-हरियर गाछ हमर सबले बेस संगी हे। उ हमनी के मीठ आम, छाया अउर शुद्ध हवा देवे हे।",
                "sck": "हरियर गाछ-बिरिछ हमर सच्चा संगी हेकें। ऊ मन हमके मीठा आंबा, छांह अउर साफ हवा देवेला।",
                "bn": "সবুজ গাছেরা আমাদের পরম বন্ধু। তারা আমাদের মিষ্টি আম, শীতল ছায়া এবং বিশুদ্ধ বাতাস দেয়।",
                "or": "ସବୁଜ ଗଛ ଆମର ପ୍ରକୃତ ବନ୍ଧୁ। ସେମାନେ ଆମକୁ ମିଠା ଆମ୍ବ, ଛାଇ ଏବଂ ସଫା ପବନ ଦିଅନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "tree", "en": "Tree", "hi": "पेड़ (Ped)", "sat": "ᱫᱟᱨᱮ (Dare)", "meaning": "फल और छाया देने वाला पौधा"},
            {"concept": "flower", "en": "Flower", "hi": "फूल (Phool)", "sat": "ᱵᱟᱦᱟ (Baha)", "meaning": "सुंदर खुशबूदार पुष्प"},
            {"concept": "water", "en": "Water", "hi": "पानी (Paani)", "sat": "ᱫᱟᱜ (Daag)", "meaning": "पौधों का जीवन रस"}
        ],
        "abhyas_questions": [
            {"q": "पेड़ हमें क्या-क्या देते हैं?", "hint": "फल, फूल, लकड़ी, छाया और ताजी हवा"},
            {"q": "आपके घर के पास कौन-सा पेड़ है?", "hint": "आम, नीम, महुआ या बरगद"}
        ]
    },
    {
        "id": "cl1_math_ch1",
        "nipun_code": "M-FLN-01",
        "nipun_outcome": "मूर्त वस्तुओं से संख्या ज्ञान १-१० (Concrete Numbers 1-10)",
        "grade": 1,
        "grade_label": "कक्षा 1 (Class 1)",
        "subject": "math",
        "subject_name": "गणित का जादू (Math Magic)",
        "subject_icon": "🔢",
        "chapter_no": 1,
        "title_hi": "गिनतारा: १ से १० तक गिनती",
        "title_en": "Counting Numbers: 1 to 10",
        "concept_summary": "उंगलियों और कंकड़ों से गिनना सीखें: १ सूरज, २ आँखें, ३ पहिए, ४ पैर।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Look up at the sky, there is one bright sun. We have two bright eyes to see the world.",
                "hi": "आकाश में देखो, एक चमकता हुआ सूरज है। संसार को देखने के लिए हमारे पास दो सुंदर आँखें हैं।",
                "sat": "ᱥᱮᱨᱢᱟ ᱨᱮ ᱧᱮᱞ ᱢᱮ, ᱢᱤᱫᱴᱟᱹᱝ ᱡᱩᱞᱩᱜ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱢᱮᱱᱟᱭᱟ᱾ ᱫᱷᱟᱹᱨᱛᱤ ᱧᱮᱞ ᱞᱟᱹᱜᱤᱫ ᱟᱵᱚᱣᱟᱜ ᱵᱟᱨᱭᱟ ᱢᱮᱫ ᱢᱮᱱᱟᱜᱼᱟ᱾",
                "ho": "ᱥᱮᱨᱢᱟ ᱨᱮ ᱱᱮᱞ ᱢᱮ, ᱢᱤᱭᱟᱹᱫᱽ ᱥᱤᱝᱜᱤ ᱢᱮᱱᱟᱭᱟ᱾ ᱫᱤᱥᱩᱢ ᱱᱮᱞ ᱞᱟᱹᱜᱤᱱ ᱟᱵᱩᱣᱟᱜ ᱵᱟᱨᱤᱭᱟ ᱢᱮᱫ ᱢᱮᱱᱟᱜᱼᱟ᱾",
                "unr": "सेरमा रे नेल मे, मियद सिंगी मेनाया। दिसुम नेल लागिन अबुवाः बरिया मेद मेनाः।",
                "kru": "अंबर तरा एरा, ओन्द बिड़ी रौद चीई। संसार एरआगे नामगै ओंड़ंग्गो खन्न रई।",
                "khr": "आसमान में देखा, एके गो चमकइत सुरुज हे। संसार देखे ले हमर दु गो आँख हे।",
                "sck": "अकास में देखू, एके गो सूरज चमकेला। दुनिया देखेक ले हमर दुइ गो आँख हे।",
                "bn": "আকাশে তাকাও, একটি উজ্জ্বল সূর্য আছে। পৃথিবী দেখার জন্য আমাদের দুটি সুন্দর চোখ আছে।",
                "or": "ଆକାଶକୁ ଦେଖ, ଗୋଟିଏ ଉଜ୍ଜ୍ୱଳ ସୂର୍ଯ୍ୟ ଅଛି। ଦୁନିଆ ଦେଖିବା ପାଇଁ ଆମର ଦୁଇଟି ସୁନ୍ଦର ଆଖି ଅଛି।"
            }
        ],
        "keywords": [
            {"concept": "one", "en": "One (1)", "hi": "एक (Ek)", "sat": "ᱢᱤᱫ (Mit)", "meaning": "संख्या १"},
            {"concept": "two", "en": "Two (2)", "hi": "दो (Do)", "sat": "ᱵᱟᱨ (Bar)", "meaning": "संख्या २"},
            {"concept": "three", "en": "Three (3)", "hi": "तीन (Teen)", "sat": "ᱯᱮ (Pe)", "meaning": "संख्या ३"}
        ],
        "abhyas_questions": [
            {"q": "आपके एक हाथ में कितनी उंगलियाँ हैं?", "hint": "पाँच (5)"},
            {"q": "ऑटो रिक्शा में कितने पहिए होते हैं?", "hint": "तीन (3)"}
        ]
    },
    {
        "id": "cl1_hindi_ch1",
        "nipun_code": "L-FLN-02",
        "nipun_outcome": "ध्वनि जागरूकता एवं लयबद्ध बालगीत (Phonological Awareness & Rhyme)",
        "grade": 1,
        "grade_label": "कक्षा 1 (Class 1)",
        "subject": "hindi",
        "subject_name": "रिमझिम / भाषा (Hindi)",
        "subject_icon": "📖",
        "chapter_no": 1,
        "title_hi": "झूला (The Swing - कविता व बालगीत)",
        "title_en": "The Swing - Nursery Poetry",
        "concept_summary": "अम्मा आज लगा दे झूला! पेड़ की डाल पर झूलते हुए बच्चे आसमान छूने का सपना देखते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Mother, put up a swing for me today on the big mango branch! I will swing high and touch the clouds.",
                "hi": "अम्मा आज लगा दे झूला, इस झूले पर मैं झूलूँगा! इस पर चढ़कर, ऊपर बढ़कर, आसमान को मैं छू लूँगा।",
                "sat": "ᱟᱭᱳ ᱛᱮᱦᱮᱧ ᱫᱚ ᱦᱤᱞᱟᱹᱣ ᱵᱮᱱᱟᱣ ᱢᱮ! ᱩᱞ ᱫᱟᱨᱮ ᱰᱟᱹᱨ ᱨᱮ ᱤᱧ ᱦᱤᱞᱟᱹᱣᱜᱼᱟ ᱟᱨ ᱥᱮᱨᱢᱟ ᱨᱤᱢᱤᱞ ᱤᱧ ᱡᱚᱴᱮᱫᱟ᱾",
                "ho": "ᱟᱭᱳ ᱛᱤᱥᱤᱝ ᱫᱚ ᱡᱷᱩᱞᱟ ᱞᱟᱜᱟᱣ ᱢᱮ! ᱩᱞ ᱫᱟᱨᱩ ᱨᱮ ᱤᱧ ᱡᱷᱩᱞᱟᱣᱜᱼᱟ ᱟᱨ ᱥᱮᱨᱢᱟ ᱡᱚᱴᱮᱫᱟ᱾",
                "unr": "आयो तिसिंग दो झूला लगाओ मे! उल दारू रे इञ झूलाओआ आर सेरमा जोतेदा।",
                "kru": "अयो इन्ना झूला कमिके चीअ! आम मन्न नु एन झुलरोस अरा अंबरन धरओस।",
                "khr": "माय आज हमरा ले झूला टांग दे! आम के डार पर झूल के हम आसमान छू लेबइ।",
                "sck": "आयो आज मोके झूला बनाय दे! आंबा गाछ में झूल-झूल के अकास छू लेब।",
                "bn": "মাগো আজ দোলনা ঝুলিয়ে দাও গাছে! আমি দুলে দুলে আকাশ ছোঁব।",
                "or": "ମାଆ ଆଜି ଦୋଳିଟିଏ ଲଗାଇଦିଅ! ମୁଁ ଝୁଲି ଝୁଲି ଆକାଶ ଛୁଇଁବି।"
            }
        ],
        "keywords": [
            {"concept": "swing", "en": "Swing", "hi": "झूला (Jhoola)", "sat": "ᱦᱤᱞᱟᱹᱣ (Hilao)", "meaning": "पेड़ पर झूलने की रस्सी"},
            {"concept": "mother", "en": "Mother", "hi": "अम्मा / माँ (Amma)", "sat": "ᱟᱭᱳ (Aayo)", "meaning": "जननी व माता"}
        ],
        "abhyas_questions": [
            {"q": "झूला किस पेड़ की डाल पर लगाया जाता है?", "hint": "आम, नीम या बरगद की मजबूत डाल पर"},
            {"q": "झूलते समय बच्चा क्या छूना चाहता है?", "hint": "नीला आसमान"}
        ]
    },
    {
        "id": "cl1_eng_ch1",
        "nipun_code": "L-FLN-01",
        "nipun_outcome": "बुनियादी आत्म-परिचय एवं शब्दावली (Self-Expression & Vocabulary)",
        "grade": 1,
        "grade_label": "कक्षा 1 (Class 1)",
        "subject": "english",
        "subject_name": "Mridang (English)",
        "subject_icon": "🔤",
        "chapter_no": 1,
        "title_hi": "मेरा परिवार और मैं (My Family and Me)",
        "title_en": "My Family and Me",
        "concept_summary": "I have a happy family. We sing, play, and love each other every day.",
        "paragraphs": [
            {
                "id": "p1",
                "en": "I have two hands to clap and two feet to run. My family smiles together under the warm sun.",
                "hi": "मेरे पास ताली बजाने के लिए दो हाथ और दौड़ने के लिए दो पैर हैं। मेरा परिवार धूप में हँसता-खेलता है।",
                "sat": "ᱤᱧᱟᱜ ᱛᱷᱟᱹᱭᱚ ᱞᱟᱹᱜᱤᱫ ᱵᱟᱨᱭᱟ ᱛᱤ ᱟᱨ ᱫᱟᱹᱲ ᱞᱟᱹᱜᱤᱫ ᱵᱟᱨᱭᱟ ᱡᱟᱝᱜᱟ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱟᱞᱮ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱩᱢᱩᱞ ᱨᱮ ᱨᱟᱹᱥᱠᱟᱹ ᱛᱮ ᱛᱟᱦᱮᱸᱱᱟ᱾",
                "ho": "ᱤᱧᱟᱜ ᱵᱟᱨᱤᱭᱟ ᱛᱤ ᱟᱨ ᱵᱟᱨᱤᱭᱟ ᱠᱟᱴᱟ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱟᱞᱮ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱨᱮ ᱞᱟᱸᱫᱟᱭᱟ᱾",
                "unr": "इञाः बरिया ती आर बरिया काटा मेनाः। अले परिवार सिंगी मारसाल रे लांदाय तना।",
                "kru": "एंगै ओंड़ंग्गो खैखा अरा ओंड़ंग्गो खेड्ड रई। एंगै परिवार रौद नू अलखना।",
                "khr": "हमर ताली बजावे ले दु गो हाथ अउर दौड़े ले दु गो गोड़ हे। हमर परिवार खुश रहे हे।",
                "sck": "हमर ताली मारेक ले दुइ गो हाथ अउर दउड़ेक ले दुइ गो गोड़ हे। हमर परिवार खुश रहेला।",
                "bn": "আমার তালি দেওয়ার জন্য দুটি হাত ও দৌড়ানোর জন্য দুটি পা আছে।",
                "or": "ମୋର ତାଳି ମାରିବାକୁ ଦୁଇଟି ହାତ ଏବଂ ଦୌଡ଼ିବାକୁ ଦୁଇଟି ଗୋଡ଼ ଅଛି।"
            }
        ],
        "keywords": [
            {"concept": "hand", "en": "Hand", "hi": "हाथ (Haath)", "sat": "ᱛᱤ (Ti)", "meaning": "काम करने का अंग"},
            {"concept": "feet", "en": "Feet / Leg", "hi": "पैर (Pair)", "sat": "ᱡᱟᱝᱜᱟ (Janga)", "meaning": "चलने-दौड़ने का अंग"}
        ],
        "abhyas_questions": [
            {"q": "How many hands do you have?", "hint": "Two hands (दो हाथ)"},
            {"q": "What do we do with our hands?", "hint": "Clap, write and eat (ताली बजाना, लिखना)"}
        ]
    },

    # =========================================================================
    # CLASS 2 (Grade 2)
    # =========================================================================
    {
        "id": "cl2_evs_ch1",
        "nipun_code": "E-FLN-03",
        "nipun_outcome": "सामुदायिक मददगार एवं ग्रामीण जीवन (Community Helpers)",
        "grade": 2,
        "grade_label": "कक्षा 2 (Class 2)",
        "subject": "evs",
        "subject_name": "पर्यावरण अध्ययन (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 1,
        "title_hi": "हमारे गाँव के मददगार",
        "title_en": "Our Village Helpers",
        "concept_summary": "किसान अन्न उगाते हैं, शिक्षक पढ़ाते हैं, और कुम्हार मिट्टी के सुंदर बर्तन बनाते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Farmers plow the fields in rain and heat to grow golden paddy and fresh vegetables for all of us.",
                "hi": "किसान धूप और बरसात में खेतों में हल चलाकर हम सभी के लिए सुनहरे धान और ताजी सब्जियाँ उगाते हैं।",
                "sat": "ᱪᱟᱹᱥᱤ ᱠᱚ ᱥᱤᱛᱩᱝ ᱟᱨ ᱫᱟᱜ ᱡᱟᱹᱲᱤ ᱨᱮ ᱠᱷᱮᱛ ᱨᱮ ᱥᱤ ᱠᱟᱛᱮ ᱥᱚᱱᱟ ᱞᱮᱠᱟᱱ ᱦᱳᱲᱳ ᱟᱨ ᱛᱟᱡᱟ ᱩᱛᱩ ᱡᱤᱱᱤᱥ ᱠᱚ ᱟᱨᱡᱟᱣᱟ᱾",
                "ho": "ᱠᱤᱥᱟᱹᱱ ᱠᱚ ᱡᱟᱹᱲᱤ ᱟᱨ ᱥᱤᱛᱩᱝ ᱨᱮ ᱵᱟᱹᱫᱽ ᱨᱮ ᱥᱤ ᱠᱮᱛᱮ ᱦᱳᱲᱳ ᱟᱨ ᱩᱛᱩ ᱠᱚ ᱪᱟᱥᱟ᱾",
                "unr": "चासी को जाड़ी आर सितुंग रे बद रे सी केते होड़ो आर उतू को चासा।",
                "kru": "उइय्यार मन रौद अरा झरी नू खड्ड नू जोखे कादना अरा नामगै बागे खस्सी धान अरा तरकारी कमअना।",
                "khr": "किसान भाई घाम अउर बरसात में खेत जोत के हमनी ले धान अउर तरकारी उपजावऽ हथिन।",
                "sck": "किसान मन रौद अउर बरखा में खेत जोइत के हमर ले धान अउर साग-भाजी उपजावेना।",
                "bn": "কৃষকরা রোদ ও বৃষ্টিতে জমিতে হাল চাষ করে আমাদের সকলের জন্য সোনার ধান ও টাটকা শাকসবজি ফলান।",
                "or": "କୃଷକମାନେ ଖରା ଓ ବର୍ଷାରେ ଜମିରେ ହଳ ଚଳାଇ ଆମ ସମସ୍ତଙ୍କ ପାଇଁ ସୁନେଲି ଧାନ ଓ ତାଜା ପନିପରିବା ଚାଷ କରନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "farmer", "en": "Farmer", "hi": "किसान (Kisaan)", "sat": "ᱪᱟᱹᱥᱤ (Chasi)", "meaning": "खेतों में अन्न उगाने वाला"},
            {"concept": "teacher", "en": "Teacher", "hi": "शिक्षक (Shikshak)", "sat": "ᱢᱟᱪᱮᱛ (Machet)", "meaning": "ज्ञान व अच्छाई सिखाने वाला"}
        ],
        "abhyas_questions": [
            {"q": "मिट्टी के घड़े और दीये कौन बनाता है?", "hint": "कुम्हार"},
            {"q": "बीमार होने पर हमारा इलाज कौन करता है?", "hint": "डॉक्टर या नर्स"}
        ]
    },
    {
        "id": "cl2_evs_ch2",
        "nipun_code": "E-FLN-02",
        "nipun_outcome": "जल संरक्षण एवं दैनिक उपयोग (Water Conservation)",
        "grade": 2,
        "grade_label": "कक्षा 2 (Class 2)",
        "subject": "evs",
        "subject_name": "पर्यावरण अध्ययन (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 2,
        "title_hi": "जल ही जीवन है",
        "title_en": "Water is Life",
        "concept_summary": "पानी पीने, खाना पकाने और खेती के लिए जरूरी है। कुओं और तालाबों को साफ रखना चाहिए।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Water is precious. Every drop of rain should be saved in village ponds and harvested from our roofs.",
                "hi": "जल अनमोल है। बारिश की हर बूँद को गाँव के तालाबों और घरों की छतों पर सहेजना चाहिए।",
                "sat": "ᱫᱟᱜ ᱫᱚ ᱟᱹᱰᱤ ᱜᱚᱱᱚᱝᱟᱱᱟ᱾ ᱡᱟᱹᱲᱤ ᱨᱮᱱᱟᱜ ᱡᱚᱛᱚ ᱴᱷᱤᱯᱤ ᱫᱟᱜ ᱟᱹᱛᱩ ᱯᱩᱠᱷᱨᱤ ᱟᱨ ᱚᱲᱟᱜ ᱥᱟᱹᱲᱤᱢ ᱨᱮ ᱥᱟᱧᱪᱟᱣ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾",
                "ho": "ᱫᱟᱜ ᱫᱚ ᱟᱹᱰᱤ ᱜᱚᱱᱚᱝ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱡᱟᱹᱲᱤ ᱫᱟᱜ ᱵᱟᱹᱫᱽ ᱟᱨ ᱯᱩᱠᱷᱩᱨᱤ ᱨᱮ ᱡᱚᱜᱟᱣ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾",
                "unr": "दाः दो अडी गोनोंग मेनाः। जाड़ी दाः बद आर पोखरा रे जोगाओ लाकतीया।",
                "kru": "अम्म अक्कबक्क दव अरा कीमती रई। झरी अम्म नू पोखड़ा अरा एड़पा नू संजोवे चाहि।",
                "khr": "पानी बड़ा कीमती हे। बरसात के हर बूँद के गाँव के तालाब अउर डोभा में बचवे के चाही।",
                "sck": "पानी बहुते बेस अउर कीमती हेके। बरखा के पानी के डोभा अउर तालाब में जमा करेक चाही।",
                "bn": "জল অমূল্য। বৃষ্টির প্রতিটি ফোঁটা গ্রামের পুকুরে এবং বাড়ির ছাদে সংরক্ষণ করা উচিত।",
                "or": "ଜଳ ଅମୂଲ୍ୟ। ବର୍ଷାର ପ୍ରତ୍ୟେକ ବୁନ୍ଦାକୁ ଗାଁ ପୋଖରୀ ଏବଂ ଘର ଛାତରେ ସଂରକ୍ଷଣ କରିବା ଉଚିତ୍।"
            }
        ],
        "keywords": [
            {"concept": "pond", "en": "Pond", "hi": "तालाब / पोखर (Talab)", "sat": "ᱯᱩᱠᱷᱨᱤ (Pukhri)", "meaning": "पानी जमा करने का जलाशय"},
            {"concept": "rain", "en": "Rain", "hi": "बारिश (Baarish)", "sat": "ᱡᱟᱹᱲᱤ (Jaari)", "meaning": "बादलों से बरसता जल"}
        ],
        "abhyas_questions": [
            {"q": "आपके गाँव में पानी कहाँ-कहाँ से मिलता है?", "hint": "कुआँ, चापाकल, नदी या तालाब"},
            {"q": "पानी बचाने के दो उपाय बताइए।", "hint": "नल बंद रखना, पानी बर्बाद न करना"}
        ]
    },
    {
        "id": "cl2_math_ch1",
        "nipun_code": "M-FLN-03",
        "nipun_outcome": "आकार, स्थान एवं ज्यामितीय अवलोकन (Shapes & Spatial Sense)",
        "grade": 2,
        "grade_label": "कक्षा 2 (Class 2)",
        "subject": "math",
        "subject_name": "गणित का जादू (Math Magic)",
        "subject_icon": "🔢",
        "chapter_no": 1,
        "title_hi": "क्या है लंबा, क्या है गोल?",
        "title_en": "What is Long, What is Round?",
        "concept_summary": "गोल चीजें लुढ़कती हैं जैसे गेंद और संतरा। लंबी और चपटी चीजें सरकती हैं जैसे डिब्बा और माचिस।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "A round football rolls smoothly on the ground, while a flat wooden block slides without rolling.",
                "hi": "गोल फुटबॉल जमीन पर सरपट लुढ़कती है, जबकि चपटा लकड़ी का गुटका बिना घूमे फिसलता है।",
                "sat": "ᱜᱩᱞᱢᱟᱹᱞ ᱯᱷᱩᱴᱵᱚᱞ ᱫᱷᱟᱹᱨᱛᱤ ᱨᱮ ᱜᱩᱰᱨᱟᱹᱣᱜᱼᱟ, ᱟᱨ ᱪᱟᱯᱲᱟ ᱠᱟᱴ ᱫᱚ ᱵᱟᱝ ᱜᱩᱰᱨᱟᱹᱣ ᱠᱟᱛᱮ ᱜᱤᱸᱫᱩᱲᱟᱹᱣᱜᱼᱟ᱾",
                "ho": "ᱜᱩᱞᱢᱟᱹᱞ ᱯᱷᱩᱴᱵᱚᱞ ᱚᱛ ᱨᱮ ᱜᱩᱰᱨᱟᱹᱣᱟ, ᱟᱨ ᱪᱟᱯᱲᱟ ᱫᱟᱨᱩ ᱫᱚ ᱜᱤᱸᱫᱩᱲᱟᱹᱣᱟ᱾",
                "unr": "गुलमल फुटबाल ओत रे गुड़राओआ, आर चापड़ा दारू दो घिसियाओआ।",
                "kru": "गोल गेंद खैखो नू गुड़री, अरा चपटी काठ गही टुकड़ा सरकी।",
                "khr": "गोलका फुटबॉल माटी पर लुढ़कऽ हे, अउर चपटा काठ के टुकड़ा घिसिया हे।",
                "sck": "गोल गेंद भुईं में लुढ़केला, अउर चपटा काठ घिसटेला।",
                "bn": "গোল ফুটবল মাটিতে গড়িয়ে যায়, কিন্তু চ্যাপ্টা কাঠের টুকরো পিছলে যায়।",
                "or": "ଗୋଲ ଫୁଟବଲ୍ ଭୂଇଁରେ ଗଡ଼ିଯାଏ, କିନ୍ତୁ ଚେପ୍ଟା କାଠ ଖଣ୍ଡ ଘୁଷୁରି ଯାଏ।"
            }
        ],
        "keywords": [
            {"concept": "round", "en": "Round", "hi": "गोल (Gol)", "sat": "ᱜᱩᱞᱢᱟᱹᱞ (Gulmal)", "meaning": "वृत्ताकार आकृति"},
            {"concept": "roll", "en": "Roll", "hi": "लुढ़कना (Ludhakna)", "sat": "ᱜᱩᱰᱨᱟᱹᱣ (Gudrao)", "meaning": "घूमते हुए आगे बढ़ना"}
        ],
        "abhyas_questions": [
            {"q": "लुढ़कने वाली दो चीजों के नाम लिखो।", "hint": "गेंद और सिक्का"},
            {"q": "सरकने वाली दो चीजों के नाम लिखो।", "hint": "किताब और माचिस की डिब्बी"}
        ]
    },
    {
        "id": "cl2_hindi_ch1",
        "nipun_code": "L-FLN-02",
        "nipun_outcome": "वर्ण-मात्रा पहचान एवं कविता पठन (Reading Fluency & Phonics)",
        "grade": 2,
        "grade_label": "कक्षा 2 (Class 2)",
        "subject": "hindi",
        "subject_name": "रिमझिम / भाषा (Hindi)",
        "subject_icon": "📖",
        "chapter_no": 1,
        "title_hi": "ऊँट चला (The Camel's Journey)",
        "title_en": "The Camel's Journey",
        "concept_summary": "ऊँट चला भाई ऊँट चला! हिलता-डुलता ऊँट चला। बालू में भी वह नहीं फँसता।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "The tall camel walks nodding with heavy load on sand. It never tires in heat or dust.",
                "hi": "ऊँट चला भाई ऊँट चला, हिलता-डुलता ऊँट चला! इतनी ऊँची गर्दन, इतनी ऊँची पीठ, पीठ उठाए ऊँट चला। बालू में भी नहीं फँसता।",
                "sat": "ᱩᱸᱴ ᱫᱚ ᱪᱟᱞᱟᱜ ᱠᱟᱱᱟ! ᱩᱥᱩᱞ ᱦᱚᱛᱚᱜ ᱟᱨ ᱩᱥᱩᱞ ᱰᱮᱦᱮᱨ ᱛᱮ ᱩᱱᱤ ᱵᱟᱹᱞᱤ ᱨᱮᱦᱚᱸ ᱵᱟᱭ ᱡᱷᱟᱹᱞᱤᱜᱼᱟ᱾",
                "ho": "ᱩᱸᱴ ᱥᱮᱱᱚᱜ ᱛᱟᱱᱟ! ᱩᱥᱩᱞ ᱩᱸᱴ ᱵᱟᱹᱞᱤ ᱨᱮ ᱠᱟ ᱡᱷᱟᱹᱞᱤᱭᱟ᱾",
                "unr": "ऊँट सेनोअ तना! उसुल ऊँट बाली रे का झाँलिया।",
                "kru": "ऊँट काअदस! उईय्या ऊँट बाली नु मल्ला अड़खी।",
                "khr": "ऊँट हिलते-डोलते चलल जा हे! बालू में ओकर पैर ना धँसे हे।",
                "sck": "ऊँट चललक भाई ऊँट चललक! बालू में ओकर गोड़ नी गड़ेला।",
                "bn": "উট হেলেদুলে বালির ওপর দিয়ে বোঝা নিয়ে হেঁটে চলেছে।",
                "or": "ଓଟ ହଲି ହଲି ବାଲି ଉପରେ ଚାଲି ଚାଲି ଯାଉଛି।"
            }
        ],
        "keywords": [
            {"concept": "camel", "en": "Camel", "hi": "ऊँट (Oont)", "sat": "ᱩᱸᱴ (Unt)", "meaning": "रेगिस्तान का जहाज"},
            {"concept": "sand", "en": "Sand", "hi": "बालू / रेत (Balu)", "sat": "ᱵᱟᱹᱞᱤ (Bali)", "meaning": "नदी व रेगिस्तान की रेत"}
        ],
        "abhyas_questions": [
            {"q": "ऊँट कहाँ आसानी से चल सकता है?", "hint": "रेत और बालू पर"},
            {"q": "ऊँट की पीठ कैसी होती है?", "hint": "ऊँची कूबड़ वाली"}
        ]
    },
    {
        "id": "cl2_eng_ch1",
        "nipun_code": "L-FLN-01",
        "nipun_outcome": "कक्षा निर्देश एवं दैनिक वार्तालाप (Classroom Greetings & Commands)",
        "grade": 2,
        "grade_label": "कक्षा 2 (Class 2)",
        "subject": "english",
        "subject_name": "Mridang (English)",
        "subject_icon": "🔤",
        "chapter_no": 1,
        "title_hi": "विद्यालय में स्वागत (Welcome to School)",
        "title_en": "Welcome to School",
        "concept_summary": "Ding-dong goes the morning school bell. We carry our colorful bags with big bright smiles.",
        "paragraphs": [
            {
                "id": "p1",
                "en": "The golden morning bell rings 'ding-dong'. Children run to school to read, write, and play happily.",
                "hi": "सुबह की घंटी 'टन-टन' बजती है। बच्चे खुशी से पढ़ने, लिखने और खेलने के लिए स्कूल दौड़ते हैं।",
                "sat": "ᱥᱮᱛᱟᱜ ᱜᱷᱟᱹᱱᱴᱤ 'ᱴᱤᱝ-ᱴᱚᱝ' ᱥᱟᱰᱮᱜᱼᱟ᱾ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱯᱟᱲᱦᱟᱣ, ᱚᱞ ᱟᱨ ᱮᱱᱮᱡ ᱞᱟᱹᱜᱤᱫ ᱟᱥᱲᱟ ᱠᱚ ᱫᱟᱹᱲᱟ᱾",
                "ho": "ᱥᱮᱛᱟᱜ ᱜᱷᱟᱹᱱᱴᱤ ᱨᱟᱜᱟ᱾ ᱜᱤᱫᱤᱨ ᱠᱚ ᱯᱟᱲᱦᱟᱣ ᱟᱨ ᱮᱱᱮᱡ ᱞᱟᱹᱜᱤᱱ ᱟᱥᱲᱟ ᱠᱚ ᱫᱟᱹᱲᱟ᱾",
                "unr": "सेताः घंटी राग तन। होन्हार को पढ़व आर एनेज लागिन आषड़ा को दउड़ा।",
                "kru": "पैरी घंटी बजरी। खद्दर मन पढा अरा खेलबा आगे स्कूल कुदना।",
                "khr": "बिहाने स्कूल के घंटी बाजे हे। सब छौआ पढ़े अउर खेले ले दौड़े हथिन।",
                "sck": "बिहान बेरा स्कूल कर घंटी बाजेला। छौवा मन पढ़े-खेलेक ले दउड़ेना।",
                "bn": "সকালে স্কুলের ঘণ্টা বেজে ওঠে। বাচ্চারা হাসিমুখে পড়তে ও খেলতে স্কুলে ছোটে।",
                "or": "ସକାଳେ ସ୍କୁଲ ଘଣ୍ଟି ବାଜିଉଠେ। ପିଲାମାନେ ଖୁସିରେ ପାଠ ପଢ଼ିବାକୁ ଦୌଡ଼ି ଆସନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "bell", "en": "Bell", "hi": "घंटी (Ghanti)", "sat": "ᱜᱷᱟᱹᱱᱴᱤ (Ghanti)", "meaning": "आवाज देने वाला घंटा"},
            {"concept": "write", "en": "Write", "hi": "लिखना (Likhna)", "sat": "ᱚᱞ (Ol)", "meaning": "कलम से कॉपी पर लिखना"}
        ],
        "abhyas_questions": [
            {"q": "What sounds 'ding-dong' in the morning?", "hint": "The school bell (स्कूल की घंटी)"},
            {"q": "Why do children go to school?", "hint": "To learn, read, and play (पढ़ने और खेलने)"}
        ]
    },

    # =========================================================================
    # CLASS 3 (Grade 3)
    # =========================================================================
    {
        "id": "cl3_evs_ch1",
        "nipun_code": "E-FLN-01",
        "nipun_outcome": "जीव-जंतुओं का आवास एवं स्वभाव (Animal Habitats & Habits)",
        "grade": 3,
        "grade_label": "कक्षा 3 (Class 3)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 1,
        "title_hi": "पूनम की दिनचर्या (जीव-जंतुओं का संसार)",
        "title_en": "Poonam's Day Out: World of Animals",
        "concept_summary": "पेड़ों, जमीन, पानी और हवा में रहने वाले जीव-जंतुओं के खान-पान और आवाजों की विविधता।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Poonam saw many animals on the tree: crows cawing, squirrels running fast, and monkeys jumping happily.",
                "hi": "पूनम ने पेड़ पर कई जीव देखे: कौवे काँव-काँव कर रहे थे, गिलहरियाँ फुदक रही थीं और बंदर मस्ती में कूद रहे थे।",
                "sat": "ᱯᱩᱱᱚᱢ ᱫᱟᱨᱮ ᱨᱮ ᱟᱭᱢᱟ ᱡᱤᱵᱽ ᱡᱤᱭᱟᱹᱞᱤ ᱧᱮᱞ ᱠᱮᱫ ᱠᱚᱣᱟ: ᱠᱟᱟᱦᱩ ᱠᱚ ᱨᱟᱜ ᱮᱫ ᱛᱟᱦᱮᱸᱫ, ᱛᱩᱲᱩ ᱠᱚ ᱫᱟᱹᱲ ᱮᱫ ᱛᱟᱦᱮᱸᱫ ᱟᱨ ᱜᱟᱹᱲᱤ ᱠᱚ ᱫᱚᱱ ᱮᱫ ᱛᱟᱦᱮᱸᱫ᱾",
                "ho": "ᱯᱩᱱᱚᱢ ᱫᱟᱨᱩ ᱨᱮ ᱟᱭᱢᱟ ᱡᱤᱣ ᱡᱤᱭᱟᱹᱞᱤ ᱱᱮᱞ ᱠᱮᱫ ᱠᱚᱣᱟ: ᱠᱟᱣᱟ ᱠᱚ ᱨᱟᱜ ᱛᱟᱱ ᱛᱟᱭᱠᱮᱱᱟ ᱟᱨ ᱥᱟᱨᱟ ᱠᱚ ᱫᱚᱱ ᱛᱟᱱ ᱛᱟᱭᱠᱮᱱᱟ᱾",
                "unr": "पूनम दारू रे आयमा जीव-जंतु नेल केद कोवा: कउवा को राग तन ताइकेना आर बंदर को दोन तन ताइकेना।",
                "kru": "पूनम मन्न नू बघ्घे जिया-जन्तु एरया: खाखा चिल्लारआ लग्गिया अरा बान्दरा बुँदरा नू कुदरआ लग्गिया।",
                "khr": "पूनम गाछ पर कई गो जीव देखलकै: कौवा काँव-काँव करऽ हल, गिलहरी दौड़ऽ हल अउर बानर कूदा-फांदी करऽ हल।",
                "sck": "पूनम गाछ में बहुते जीव-जन्तु देखलक: कउवा बोलेला, रुखुवा दउड़ेला अउर बान्दर मन कूदेना।",
                "bn": "পুনম গাছে অনেক পশুপাখি দেখেছিল: কাকেরা ডাকছিল, কাঠবিড়ালিরা ছুটছিল এবং বাঁদরেরা ডালে ডালে লাফাচ্ছিল।",
                "or": "ପୁନମ୍ ଗଛରେ ଅନେକ ଜୀବଜନ୍ତୁ ଦେଖିଲା: କାଉମାନେ ରାବୁଥିଲେ, ଗୁଣ୍ଡୁଚିମୂଷା ଦୌଡ଼ୁଥିଲେ ଏବଂ ମାଙ୍କଡ଼ମାନେ ଡେଉଁଥିଲେ।"
            }
        ],
        "keywords": [
            {"concept": "squirrel", "en": "Squirrel", "hi": "गिलहरी (Gilahari)", "sat": "ᱛᱩᱲᱩ (Turu)", "meaning": "पेड़ों पर फुदकने वाला छोटा जीव"},
            {"concept": "monkey", "en": "Monkey", "hi": "बंदर (Bandar)", "sat": "ᱜᱟᱹᱲᱤ (Gari)", "meaning": "पेड़ों पर छलांग लगाने वाला जानवर"}
        ],
        "abhyas_questions": [
            {"q": "पेड़ पर रहने वाले किन्हीं तीन पक्षियों के नाम बताओ।", "hint": "कौवा, तोता, मैना"},
            {"q": "पानी में रहने वाले दो जीवों के नाम बताओ।", "hint": "मछली, मेंढक"}
        ]
    },
    {
        "id": "cl3_evs_ch2",
        "nipun_code": "E-FLN-01",
        "nipun_outcome": "पौधों के भाग एवं प्रकाश-संश्लेषण (Plant Parts & Sunlight)",
        "grade": 3,
        "grade_label": "कक्षा 3 (Class 3)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 2,
        "title_hi": "पौधों की परी (पत्तियों और जड़ों का संसार)",
        "title_en": "The Plant Fairy: Leaves, Stems and Roots",
        "concept_summary": "पत्तियाँ अलग-अलग आकार और गंध की होती हैं। वे सूर्य की धूप में भोजन पकाती हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Leaves have different shapes, edges, and smells: neem leaves are bitter, mint smells fresh, and peepal leaves are broad.",
                "hi": "पत्तियों के कई आकार और खुशबू होती हैं: नीम की पत्ती कड़वी और औषधीय होती है, पुदीना सुगंधित होता है, और पीपल का पत्ता चौड़ा होता है।",
                "sat": "ᱥᱟᱠᱟᱢ ᱨᱮᱱᱟᱜ ᱟᱭᱢᱟ ᱨᱩᱯ ᱟᱨ ᱥᱚ ᱛᱟᱦᱮᱸᱱᱟ: ᱱᱤᱢ ᱥᱟᱠᱟᱢ ᱫᱚ ᱦᱟᱫᱽ ᱟᱨ ᱨᱟᱱ ᱠᱟᱱᱟ, ᱯᱩᱫᱤᱱᱟ ᱫᱚ ᱥᱤᱵᱤᱞ ᱥᱚᱻᱟ ᱟᱨ ᱦᱮᱸᱥᱟᱜ ᱥᱟᱠᱟᱢ ᱫᱚ ᱪᱟᱯᱲᱟ ᱜᱮᱭᱟ᱾",
                "ho": "ᱥᱟᱠᱟᱢ ᱨᱮᱭᱟᱜ ᱟᱭᱢᱟ ᱞᱮᱠᱟᱱ ᱜᱚᱲᱦᱚᱱ ᱢᱮᱱᱟᱜᱼᱟ: ᱱᱤᱢ ᱥᱟᱠᱟᱢ ᱦᱟᱲᱟᱫ ᱜᱮᱭᱟ, ᱟᱨ ᱯᱤᱯᱟᱹᱲ ᱥᱟᱠᱟᱢ ᱪᱟᱯᱲᱟ ᱜᱮᱭᱟ᱾",
                "unr": "साकाम रेयाः आयमा लेकान गड़हन मेनाः: नीम साकाम हाड़ाद गेया, आर पीपड़ साकाम चापड़ा गेया।",
                "kru": "अट्टी गही जुदा-जुदा रूप अरा महक रई: नीम अट्टी कड़वा अरा दवाई तली, अरा पीपर अट्टी चउड़ा रई।",
                "khr": "पत्ता के ढेरे रूप अउर महक होवऽ हे: नीम पत्ता तीता अउर दवाई नियर हे, अउर पीपल पत्ता चउड़ा होवऽ हे।",
                "sck": "पत्ती मनक अलग-अलग रूप अउर गंध होवेला: नीम पत्ता तीता अउर दवाई हेके, पीपल पत्ता चउड़ा हेके।",
                "bn": "পাতার নানা আকার ও সুবাস থাকে: নিমপাতা তিতো ও ভেষজ গুণসম্পন্ন, পুদিনা সুগন্ধি এবং অশ্বত্থ পাতা চওড়া।",
                "or": "ପତ୍ରର ବିଭିନ୍ନ ଆକାର ଓ ବାସ୍ନା ଥାଏ: ନିମ ପତ୍ର ପିତା ଓ ଔଷଧୀୟ, ପୋଦିନା ସୁଗନ୍ଧିତ ଏବଂ ଓସ୍ତ ପତ୍ର ଓସାରିଆ।"
            }
        ],
        "keywords": [
            {"concept": "leaf", "en": "Leaf", "hi": "पत्ती (Patti)", "sat": "ᱥᱟᱠᱟᱢ (Sakam)", "meaning": "पौधे का रसोईघर"},
            {"concept": "neem", "en": "Neem", "hi": "नीम (Neem)", "sat": "ᱱᱤᱢ (Nim)", "meaning": "रोग दूर करने वाला औषधीय वृक्ष"}
        ],
        "abhyas_questions": [
            {"q": "दवाइयों के काम आने वाले दो पौधों के नाम लिखो।", "hint": "तुलसी और नीम"},
            {"q": "पत्तियाँ भोजन कैसे बनाती हैं?", "hint": "धूप और पानी की मदद से"}
        ]
    },
    {
        "id": "cl3_math_ch1",
        "nipun_code": "M-FLN-02",
        "nipun_outcome": "संख्या विस्तार एवं स्थानीय मान १०० तक (Place Value & Skip Counting)",
        "grade": 3,
        "grade_label": "कक्षा 3 (Class 3)",
        "subject": "math",
        "subject_name": "गणित का जादू (Math Magic)",
        "subject_icon": "🔢",
        "chapter_no": 1,
        "title_hi": "संख्याओं की उछल-कूद (शतक और दहाई)",
        "title_en": "Fun with Numbers: Centuries and Bundles",
        "concept_summary": "क्रिकेट में शतक (100 रन), दस-दस के बंडल और हाट में मुद्रा विनिमय।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Dhoni hit a sixer to complete his century of 100 runs. Ten bundles of ten sticks make one hundred.",
                "hi": "धोनी ने छक्का मारकर अपना शतक (100 रन) पूरा किया। दस-दस लकड़ियों के दस बंडल मिलकर पूरे १०० बनते हैं।",
                "sat": "ᱫᱷᱳᱱᱤ ᱫᱚ ᱪᱷᱟᱠᱠᱟ ᱜᱤᱰᱤ ᱠᱟᱛᱮ ᱟᱡᱟᱜ ᱥᱟᱭ (᱑᱐᱐) ᱨᱟᱱ ᱮ ᱯᱩᱨᱟᱹᱣ ᱠᱮᱫᱟ᱾ ᱜᱮᱞ-ᱜᱮᱞ ᱠᱟᱴᱷᱤ ᱨᱮᱱᱟᱜ ᱜᱮᱞ ᱴᱤᱸᱰᱟᱹ ᱢᱤᱞᱟᱹᱣ ᱠᱟᱛᱮ ᱢᱤᱫ ᱥᱟᱭ ᱦᱩᱭᱩᱜᱼᱟ᱾",
                "ho": "ᱫᱷᱳᱱᱤ ᱪᱷᱟᱠᱠᱟ ᱮᱢ ᱠᱮᱛᱮ ᱥᱟᱭ (᱑᱐᱐) ᱨᱟᱱ ᱯᱩᱨᱟᱹᱣ ᱠᱮᱫᱟ᱾ ᱜᱮᱞ-ᱜᱮᱞ ᱴᱤᱸᱰᱟᱹ ᱛᱮ ᱢᱤᱫ ᱥᱟᱭ ᱵᱟᱭᱚᱜᱼᱟ᱾",
                "unr": "धोनी छक्का मार केते साय (१००) रन पूरा केदा। गेल-गेल काठी रेयाः गेल बंडल मिद साय होबोआ।",
                "kru": "धोनी छक्का लउरस अरा सय रन पूरा कमचस। दसे-दसे गही दसे मुट्ठा सय मनी।",
                "khr": "धोनी छक्का मार के १०० रन के शतक बनवलकै। दस-दस गो लकड़ी के दस बंडल मिल के १०० होवऽ हे।",
                "sck": "धोनी छक्का मार के आपन शतक (१०० रन) पूरा करलक। दस-दस गो के दस बंडल से १०० बनेला।",
                "bn": "ধোনি ছক্কা মেরে তার শতক (১০০ রান) পূর্ণ করল। দশের দশটি বান্ডিলে একশত হয়।",
                "or": "ଧୋନି ଛକା ମାରି ନିଜର ଶତକ (୧୦୦ ରନ୍) ପୂରଣ କଲେ। ଦଶଟି ଦଶର ବିଡ଼ା ମିଶି ଶହେ ହୁଏ।"
            }
        ],
        "keywords": [
            {"concept": "century", "en": "Century / Hundred", "hi": "शतक / सौ (100)", "sat": "ᱥᱟᱭ (Sae)", "meaning": "संख्या १००"},
            {"concept": "bundle", "en": "Bundle of Ten", "hi": "दहाई / बंडल (10)", "sat": "ᱜᱮᱞ (Gel)", "meaning": "१० का समूह"}
        ],
        "abhyas_questions": [
            {"q": "१ शतक में कितने रन होते हैं?", "hint": "१०० रन"},
            {"q": "९९ के बाद कौन-सी संख्या आती है?", "hint": "१०० (एक सौ)"}
        ]
    },
    {
        "id": "cl3_hindi_ch1",
        "nipun_code": "L-FLN-03",
        "nipun_outcome": "भावपूर्ण पठन एवं शब्द-रचना (Expressive Reading & Synonyms)",
        "grade": 3,
        "grade_label": "कक्षा 3 (Class 3)",
        "subject": "hindi",
        "subject_name": "रिमझिम / भाषा (Hindi)",
        "subject_icon": "📖",
        "chapter_no": 1,
        "title_hi": "कक्कू (The Playful Boy - कविता)",
        "title_en": "Kakku the Boy",
        "concept_summary": "नाम है उसका कक्कू, कक्कू माने कोयल होता! लेकिन यह तो दिन भर रोता, इसीलिए हम इसे चिढ़ाते।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "His name is Kakku, which means sweet Cuckoo bird. But he gets angry over small jokes, so friends tease him.",
                "hi": "नाम है उसका कक्कू, कक्कू माने कोयल होता! लेकिन यह तो दिन भर रोता, इसीलिए हम इसे चिढ़ाते, कहते इसको सक्कू।",
                "sat": "ᱩᱱᱤᱭᱟᱜ ᱧᱩᱛᱩᱢ ᱫᱚ ᱠᱟᱠᱠᱩ, ᱠᱟᱠᱠᱩ ᱢᱮᱱᱮᱛ ᱫᱚ ᱠᱩᱦᱩ ᱪᱮᱬᱮ! ᱢᱮᱱᱠᱷᱟᱱ ᱩᱱᱤ ᱫᱤᱱᱟᱹᱢ ᱮ ᱨᱟᱜᱟ, ᱚᱱᱟᱛᱮ ᱜᱟᱛᱮ ᱠᱚ ᱞᱟᱸᱫᱟᱣᱟᱭᱟ᱾",
                "ho": "ᱮᱱᱤᱭᱟᱜ ᱧᱩᱛᱩᱢ ᱠᱟᱠᱠᱩ! ᱠᱟᱠᱠᱩ ᱢᱮᱱᱮᱛ ᱠᱩᱦᱩ ᱪᱮᱬᱮ᱾ ᱢᱮᱱᱫᱚ ᱱᱤ ᱫᱤᱱᱟᱹᱢ ᱨᱟᱜᱟ᱾",
                "unr": "एनियाः नुतूम कक्कू! कक्कू मने कुहू चेणे। मेनदो नी दिनुम रागा।",
                "kru": "आसिगही नामे कक्कू रई! कक्कू माने कोयल मनी। पाहे आस दिन्ने-दिन्ने रोइती रअदस।",
                "khr": "ओकर नाम कक्कू हे, कक्कू माने कोयल! बाकिर उ दिन भर रोवऽ हे, तबे संगी सब ओकरा चिढ़ावऽ हे।",
                "sck": "ओकर नाम कक्कू हेके, कक्कू माने कोयल! मने ऊ दिन भर खिझायला, सेहेले सभे सक्कू कहेना।",
                "bn": "তার নাম কাক্কু, কাক্কু মানে কোকিল পাখি। কিন্তু সে সারাদিন শুধু রেগে যায়।",
                "or": "ତା'ର ନାମ କାକ୍କୁ, କାକ୍କୁ ମାନେ କୋଇଲି! କିନ୍ତୁ ସେ ସବୁବେଳେ ରାଗିଯାଏ।"
            }
        ],
        "keywords": [
            {"concept": "cuckoo", "en": "Cuckoo Bird", "hi": "कोयल (Koyal)", "sat": "ᱠᱩᱦᱩ ᱪᱮᱬᱮ (Kuhu Chene)", "meaning": "मीठी बोली वाली पक्षी"},
            {"concept": "weep", "en": "Cry / Weep", "hi": "रोना (Rona)", "sat": "ᱨᱟᱜ (Raag)", "meaning": "आँसू बहाना"}
        ],
        "abhyas_questions": [
            {"q": "कोयल की बोली कैसी होती है?", "hint": "मीठी और सुरीली (कुहू-कुहू)"},
            {"q": "कक्कू को दोस्त क्या कहकर चिढ़ाते थे?", "hint": "सक्कू (क्योंकि वह बात-बात पर गुस्सा होता था)"}
        ]
    },
    {
        "id": "cl3_eng_ch1",
        "nipun_code": "L-FLN-03",
        "nipun_outcome": "वर्णनात्मक गद्यांश पठन (Descriptive Paragraph Comprehension)",
        "grade": 3,
        "grade_label": "कक्षा 3 (Class 3)",
        "subject": "english",
        "subject_name": "Santoor / Marigold (English)",
        "subject_icon": "🔤",
        "chapter_no": 1,
        "title_hi": "जादुई बगीचा (The Magic Garden)",
        "title_en": "The Magic Garden",
        "concept_summary": "The flowers loved the little school children because they watered their thirsty roots every afternoon.",
        "paragraphs": [
            {
                "id": "p1",
                "en": "The sun-flowers and roses stood proudly by the school wall. They whispered, 'We love the children because they bring water cans.'",
                "hi": "सूरजमुखी और गुलाब के फूल स्कूल की दीवार के पास मुस्कुरा रहे थे। वे बोले, 'हमें बच्चे बहुत प्यारे लगते हैं क्योंकि वे हमारी प्यासी जड़ों को पानी पिलाते हैं।'",
                "sat": "ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱵᱟᱦᱟ ᱟᱨ ᱜᱳᱞᱟᱯ ᱵᱟᱦᱟ ᱟᱥᱲᱟ ᱠᱟᱸᱛ ᱥᱩᱨ ᱨᱮ ᱨᱟᱹᱥᱠᱟᱹ ᱛᱮ ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ᱾ ᱩᱱᱠᱩ ᱠᱚ ᱢᱮᱱ ᱠᱮᱫᱟ, 'ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱟᱞᱮ ᱫᱟᱜ ᱠᱚ ᱮᱢᱟᱞᱮᱭᱟ᱾'",
                "ho": "ᱥᱤᱝᱜᱤ ᱵᱟᱦᱟ ᱟᱨ ᱜᱳᱞᱟᱯ ᱟᱥᱲᱟ ᱡᱟᱯᱟᱜ ᱨᱮ ᱪᱚᱨᱚᱠ ᱱᱮᱞᱚᱜ ᱛᱟᱱᱟ᱾ ᱱᱤᱠᱩ ᱠᱟᱡᱤ ᱠᱮᱫᱟ, 'ᱜᱤᱫᱤᱨ ᱠᱚ ᱟᱞᱮ ᱫᱟᱜ ᱮᱢᱟᱞᱮᱭᱟ᱾'",
                "unr": "सिंगी बाहा आर गुलाब आषड़ा जोपाः रे चोरोक नेलोः तना। निकु कजी केदा, 'होन्हार को अले दाः एमालेया।",
                "kru": "सूरजमुखी अरा गुलाब पूप मन स्कूल गही काँत नू अलखआ लग्गिया। आर बच्या, 'खद्दर नामन अम्म चीना।'",
                "khr": "सूरजमुखी अउर गुलाब के फूल स्कूल के देवाल लगे खिलल हल। ऊ कहलकै, 'छौआ सब हमनी के पानी पटावऽ हे।'",
                "sck": "सूरजमुखी अउर गुलाब के फूल स्कूल कर देवाल लगे लहलहाएला। ऊ मन छौवा मनके बहुत प्यार करेना।",
                "bn": "সূর্যমুখী ও গোলাপ ফুলেরা স্কুলের দেওয়ালের পাশে ফুটে ছিল। তারা বলল, 'শিশুরা আমাদের জল দেয় বলে আমরা তাদের ভালোবাসি।'",
                "or": "ସୂର୍ଯ୍ୟମୁଖୀ ଓ ଗୋଲାପ ଫୁଲ ସ୍କୁଲ କାନ୍ଥ ପାଖରେ ଫୁଟିଥିଲେ। ସେମାନେ କହିଲେ, 'ପିଲାମାନେ ଆମକୁ ପାଣି ଦିଅନ୍ତି।'"
            }
        ],
        "keywords": [
            {"concept": "garden", "en": "Garden", "hi": "बगीचा / उपवन (Bageecha)", "sat": "ᱵᱟᱜᱟᱱ (Bagan)", "meaning": "फूलों और पौधों का स्थान"},
            {"concept": "rose", "en": "Rose Flower", "hi": "गुलाब (Gulaab)", "sat": "ᱜᱳᱞᱟᱯ ᱵᱟᱦᱟ (Golap Baha)", "meaning": "सुगंधित लाल पुष्प"}
        ],
        "abhyas_questions": [
            {"q": "Why did the flowers love the children?", "hint": "Because children watered their roots (वे उन्हें पानी देते थे)"},
            {"q": "Name two flowers mentioned in the story.", "hint": "Sunflower and Rose (सूरजमुखी और गुलाब)"}
        ]
    },

    # =========================================================================
    # CLASS 4 (Grade 4)
    # =========================================================================
    {
        "id": "cl4_evs_ch1",
        "nipun_code": "E-FLN-03",
        "nipun_outcome": "यातायात के साधन एवं भौगोलिक विविधता (Transport & Geography)",
        "grade": 4,
        "grade_label": "कक्षा 4 (Class 4)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 1,
        "title_hi": "चलो, चलें स्कूल! (पगडंडियों से सेतु तक)",
        "title_en": "Going to School: Paths, Trolleys and Bridges",
        "concept_summary": "झारखंड के बच्चे जंगलों, पगडंडियों, नदियों और बाँस के पुलों को पार करके ज्ञान पाने स्कूल पहुँचते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Every child has the right to study. Children cross rocky hills, green forests, and river bridges holding hands with joy.",
                "hi": "हर बच्चे का पढ़ने का अधिकार है। बच्चे पथरीली पहाड़ियों, हरे जंगलों और नदी के पुलों को पार कर हँसते-गाते स्कूल जाते हैं।",
                "sat": "ᱡᱚᱛᱚ ᱜᱤᱫᱽᱨᱟᱹ ᱣᱟᱜ ᱯᱟᱲᱦᱟᱣ ᱨᱮᱱᱟᱜ ᱟᱹᱭᱫᱟᱹᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱫᱷᱤᱨᱤ ᱵᱩᱨᱩ, ᱦᱟᱹᱨᱭᱟᱹᱲ ᱵᱤᱨ ᱟᱨ ᱜᱟᱰᱟ ᱥᱟᱠᱷᱳ ᱯᱟᱨᱚᱢ ᱠᱟᱛᱮ ᱨᱟᱹᱥᱠᱟᱹ ᱛᱮ ᱟᱥᱲᱟ ᱠᱚ ᱥᱮᱱᱚᱜᱼᱟ᱾",
                "ho": "ᱥᱚᱵᱮᱱ ᱜᱤᱫᱤᱨ ᱠᱚᱣᱟᱜ ᱯᱟᱲᱦᱟᱣ ᱨᱮᱭᱟᱜ ᱟᱹᱭᱫᱟᱹᱨ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱜᱤᱫᱤᱨ ᱠᱚ ᱵᱩᱨᱩ, ᱵᱤᱨ ᱟᱨ ᱜᱟᱲᱟ ᱯᱟᱨᱚᱢ ᱠᱮᱛᱮ ᱟᱥᱲᱟ ᱠᱚ ᱥᱮᱱᱚᱜᱼᱟ᱾",
                "unr": "सोबेन होन्हार कोवाः पढ़व रेयाः आयदार मेनाः। होन्हार को बुरु, बीर आर गड़ा पारोम केते आषड़ा को सेनोआ।",
                "kru": "हूर्मर खद्दर गही पढा गही हक रई। खद्दर मन टेकड़ा, झंखड़ी अरा नदी गही सँको पार कमचस स्कूल काअना।",
                "khr": "सब छौआ के पढ़े के अधिकार हे। छौआ-पुता पहाड़, जंगल अउर नदी पार कर के खुश होके स्कूल जा हथिन।",
                "sck": "सभे छौवा मनक पढ़े-लिखेक अधिकार हेके। छौवा मन पहाड़, जंगल अउर नदी पार कइर के उमंग से स्कूल जावेना।",
                "bn": "প্রত্যেক শিশুর পড়াশোনার অধিকার আছে। শিশুরা পাথুরে পাহাড়, সবুজ জঙ্গল ও নদীর সাঁকো পেরিয়ে আনন্দ সহকারে স্কুলে যায়।",
                "or": "ପ୍ରତ୍ୟେକ ପିଲାର ପାଠ ପଢ଼ିବାର ଅଧିକାର ଅଛି। ପିଲାମାନେ ପଥୁରିଆ ପାହାଡ଼, ସବୁଜ ଜଙ୍ଗଲ ଏବଂ ନଦୀ ପୋଲ ପାର ହୋଇ ଆନନ୍ଦରେ ସ୍କୁଲ ଯାଆନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "school", "en": "School", "hi": "विद्यालय / स्कूल (School)", "sat": "ᱟᱥᱲᱟ (Asra)", "meaning": "ज्ञान और संस्कार का मंदिर"},
            {"concept": "bridge", "en": "Bridge", "hi": "पुल / सेतु (Setu)", "sat": "ᱥᱟᱠᱷᱳ (Sakho)", "meaning": "नदी पार करने का मार्ग"}
        ],
        "abhyas_questions": [
            {"q": "आप स्कूल कैसे पहुँचते हैं?", "hint": "पैदल, साइकिल या बस से"},
            {"q": "पहाड़ी इलाकों में स्कूल जाने में क्या कठिनाई आती है?", "hint": "ऊँचे-नीचे पथरीले रास्ते"}
        ]
    },
    {
        "id": "cl4_evs_ch2",
        "nipun_code": "E-FLN-01",
        "nipun_outcome": "पर्यावरण संरक्षण एवं चिपको इतिहास (Environmental Stewardship)",
        "grade": 4,
        "grade_label": "कक्षा 4 (Class 4)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 2,
        "title_hi": "अमृता की कहानी (वृक्ष रक्षा और चिपको)",
        "title_en": "The Story of Amrita: Forest Conservation",
        "concept_summary": "पेड़ हैं तो हम हैं! खेजड़ी के पेड़ों और वनों की रक्षा के लिए ग्रामीणों का साहसी त्याग।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Trees give us life, rain, and cool shade. If trees survive, only then animals and humans will survive.",
                "hi": "पेड़ हैं तो हम हैं! पेड़ हमें जीवन, वर्षा और शीतल छाया देते हैं। अगर पेड़ बचेंगे, तभी हम सब जीवित रहेंगे।",
                "sat": "ᱫᱟᱨᱮ ᱢᱮᱱᱟᱜᱼᱟ ᱢᱮᱱᱛᱮ ᱟᱵᱚ ᱢᱮᱱᱟᱜ ᱵᱚᱱᱟ! ᱫᱟᱨᱮ ᱟᱵᱚ ᱡᱤᱣᱤ, ᱫᱟᱜ ᱡᱟᱹᱲᱤ ᱟᱨ ᱨᱮᱭᱟᱲ ᱩᱢᱩᱞ ᱮ ᱮᱢᱟᱵᱚᱱᱟ᱾ ᱫᱟᱨᱮ ᱛᱟᱦᱮᱸᱱ ᱠᱷᱟᱱ ᱜᱮ ᱟᱵᱚ ᱵᱚᱱ ᱵᱟᱧᱪᱟᱣ ᱛᱟᱦᱮᱸᱱᱟ᱾",
                "ho": "ᱫᱟᱨᱩ ᱢᱮᱱᱟᱜᱼᱟ ᱛᱮ ᱟᱵᱩ ᱢᱮᱱᱟᱜ ᱵᱩᱣᱟ! ᱫᱟᱨᱩ ᱟᱵᱩ ᱡᱤᱣᱤ ᱟᱨ ᱡᱟᱹᱲᱤ ᱮᱢᱟᱵᱩᱣᱟ᱾",
                "unr": "दारू मेनाः ते अबु मेनाः बुया! दारू अबु जीवी आर जाड़ी एमाबुया।",
                "kru": "मन्न रई तले नाम रअत! मन्न नामन जिन्दगी, झरी अरा ठंडा छाँही चीई।",
                "khr": "गाछ हे तबे हमनी ही! गाछ हमनी के जिंदगी, पानी अउर शीतल छाया देवे हे।",
                "sck": "गाछ-बिरिछ आहे तबे हमरे आही! गाछ हमके जिनगी, बरखा अउर छांह देवेला।",
                "bn": "গাছ আছে বলেই আমরা আছি! গাছ আমাদের জীবন, বৃষ্টি এবং শীতল ছায়া দেয়। গাছ বাঁচলে তবেই মানবজাতি বাঁচবে।",
                "or": "ଗଛ ଅଛି ବୋଲି ଆମେ ଅଛୁ! ଗଛ ଆମକୁ ଜୀବନ, ବର୍ଷା ଏବଂ ଶୀତଳ ଛାଇ ଦିଏ। ଗଛ ବଞ୍ଚିଲେ ହିଁ ଆମେ ବଞ୍ଚିବା।"
            }
        ],
        "keywords": [
            {"concept": "forest", "en": "Forest", "hi": "जंगल / वन (Jangal)", "sat": "ᱵᱤᱨ (Bir)", "meaning": "वृक्षों और वन्यजीवों का घर"},
            {"concept": "protect", "en": "Protect / Save", "hi": "रक्षा करना (Raksha)", "sat": "ᱵᱟᱧᱪᱟᱣ (Banchao)", "meaning": "पेड़ों को कटने से बचाना"}
        ],
        "abhyas_questions": [
            {"q": "पेड़ हमारे पर्यावरण के लिए क्यों जरूरी हैं?", "hint": "वे प्रदूषण दूर करते हैं और वर्षा लाते हैं"},
            {"q": "झारखंड का राजकीय वृक्ष कौन-सा है?", "hint": "साल / सखुआ (Sal Tree)"}
        ]
    },
    {
        "id": "cl4_math_ch1",
        "nipun_code": "M-FLN-03",
        "nipun_outcome": "त्रिविमीय आकृतियाँ, पैटर्न एवं जाली (3D Shapes & Spatial Patterns)",
        "grade": 4,
        "grade_label": "कक्षा 4 (Class 4)",
        "subject": "math",
        "subject_name": "गणित का जादू (Math Magic)",
        "subject_icon": "🔢",
        "chapter_no": 1,
        "title_hi": "ईंटों से बनी इमारत (जाली और मेहराब)",
        "title_en": "Building with Bricks: Patterns and Shapes",
        "concept_summary": "ईंटों के सुंदर पैटर्न, जालीदार दीवारें, मेहराब और ईंट भट्ठे का गणितीय हिसाब।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "A brick has six flat faces. Masons arrange red bricks in beautiful patterns to build strong school classrooms.",
                "hi": "एक ईंट के छह समतल फलक होते हैं। राजमिस्त्री लाल ईंटों को सुंदर जाली पैटर्न में जोड़कर मजबूत स्कूल भवन बनाते हैं।",
                "sat": "ᱢᱤᱫᱴᱟᱹᱝ ᱤᱴᱟᱹ ᱨᱮᱱᱟᱜ ᱛᱩᱨᱩᱭ ᱪᱟᱯᱲᱟ ᱢᱮᱫᱦᱟᱸ ᱛᱟᱦᱮᱸᱱᱟ᱾ ᱨᱟᱡᱽᱢᱤᱥᱛᱨᱤ ᱟᱨᱟᱜ ᱤᱴᱟᱹ ᱛᱮ ᱪᱚᱨᱚᱠ ᱡᱟᱞᱤ ᱜᱚᱲᱦᱚᱱ ᱠᱟᱛᱮ ᱠᱮᱴᱮᱡ ᱟᱥᱲᱟ ᱠᱚ ᱵᱮᱱᱟᱣᱟ᱾",
                "ho": "ᱢᱤᱭᱟᱹᱫᱽ ᱤᱴᱟᱹ ᱨᱮ ᱛᱩᱨᱩᱭ ᱢᱩᱴᱷᱟᱹᱱ ᱢᱮᱱᱟᱜᱼᱟ᱾ ᱢᱤᱥᱛᱨᱤ ᱟᱨᱟᱜ ᱤᱴᱟᱹ ᱛᱮ ᱠᱮᱴᱮᱡ ᱟᱥᱲᱟ ᱵᱟᱭᱟ᱾",
                "unr": "मियद ईंटा रे तुरूय फलक मेनाः। मिस्त्री लाल ईंटा ते केतेज आषड़ा बाईया।",
                "kru": "ओन्द ईंटा नू सोय फलक मनी। मिस्त्री लाली ईंटा ती गद्दर स्कूल एड़पा कमअना।",
                "khr": "एगो ईंटा के छव गो मुँह (फलक) होवऽ हे। मिस्त्री लाल ईंटा जोड़ के मजबूत स्कूल बनावऽ हथिन।",
                "sck": "एगो ईंट कर छव गो मुँह होवेला। मिस्त्री लाल ईंट से सुंदर अउर मजबूत स्कूल घर बनावेला।",
                "bn": "একটি ইটের ছয়টি তল থাকে। রাজমিস্ত্রিরা শক্ত স্কুল ভবন গড়ে তুলতে সুন্দর বিন্যাসে ইট সাজান।",
                "or": "ଗୋଟିଏ ଇଟାର ଛଅଟି ପାର୍ଶ୍ୱ ଥାଏ। ରାଜମିସ୍ତ୍ରୀମାନେ ଲାଲ୍ ଇଟାକୁ ସୁନ୍ଦର ଭାବରେ ସଜାଇ ମଜବୁତ ସ୍କୁଲ ଘର ତିଆରି କରନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "brick", "en": "Brick", "hi": "ईंट (Eent)", "sat": "ᱤᱴᱟᱹ (Ita)", "meaning": "मिट्टी से पकी छह फलकों वाली निर्माण सामग्री"},
            {"concept": "pattern", "en": "Pattern", "hi": "पैटर्न / नमूना (Pattern)", "sat": "ᱜᱚᱲᱦᱚᱱ (Gadhon)", "meaning": "सजावट की क्रमबद्ध रचना"}
        ],
        "abhyas_questions": [
            {"q": "एक ईंट के कितने चेहरे (फलक) होते हैं?", "hint": "छह (6)"},
            {"q": "ईंट का आकार किस ज्यामितीय आकृति जैसा होता है?", "hint": "घनाभ (Cuboid)"}
        ]
    },
    {
        "id": "cl4_hindi_ch1",
        "nipun_code": "L-FLN-04",
        "nipun_outcome": "कल्पनाशीलता एवं काव्य अभिव्यक्ति (Poetic Imagery & Metaphors)",
        "grade": 4,
        "grade_label": "कक्षा 4 (Class 4)",
        "subject": "hindi",
        "subject_name": "रिमझिम / भाषा (Hindi)",
        "subject_icon": "📖",
        "chapter_no": 1,
        "title_hi": "मन के भोले-भाले बादल (Playful Clouds)",
        "title_en": "Playful Clouds - Monsoon Poetry",
        "concept_summary": "झब्बर-झब्बर बालों वाले, गुब्बारे से गालों वाले बादल आसमान में दौड़ते हैं और झर-झर पानी बरसाते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Dark playful clouds with puffy cheeks run across the monsoon sky. They tap their drums and bring joyous rain to fields.",
                "hi": "झब्बर-झब्बर बालों वाले, गुब्बारे से गालों वाले, लगे दौड़ने आसमान में झूम-झूम कर काले बादल! ढोल बजाते और खेतों में अमृत बरसाते हैं।",
                "sat": "ᱦᱮᱸᱫᱮ ᱨᱤᱢᱤᱞ ᱥᱮᱨᱢᱟ ᱨᱮ ᱫᱟᱹᱲ ᱟᱠᱟ ᱢᱮᱱᱟᱜᱼᱟ! ᱩᱱᱠᱩ ᱰᱷᱳᱞ ᱨᱩ ᱞᱮᱠᱟ ᱜᱟᱰᱨᱟᱣ ᱠᱟᱛᱮ ᱠᱷᱮᱛ ᱨᱮ ᱥᱤᱵᱤᱞ ᱫᱟᱜ ᱠᱚ ᱡᱟᱹᱲᱤᱭᱟ᱾",
                "ho": "ᱦᱮᱸᱫᱮ ᱨᱤᱢᱤᱞ ᱥᱮᱨᱢᱟ ᱨᱮ ᱫᱟᱹᱲ ᱛᱟᱱᱟ! ᱩᱱᱠᱩ ᱵᱟᱹᱫᱽ ᱨᱮ ᱡᱟᱹᱲᱤ ᱫᱟᱜ ᱮᱢᱟ᱾",
                "unr": "हेंदड़े रिमिल सेरमा रे दउड़ तन। निकु बद रे जाड़ी दाः एमा।",
                "kru": "कड़िया बादल अंबर नू कुदरआ लग्गिया। बादल ढोल ठोकआ अरा खड्ड नू झरी चीआ।",
                "khr": "घटाटोप कारी बदरी आसमान में गरज-गरज के खेत-खरिहान में पानी बरसावऽ हे।",
                "sck": "करिया-करिया बादल अकास में नाचेला अउर खेत-खरिहान में बरखा बरसावेला।",
                "bn": "কালো মেঘেরা আকাশে উড়ে বেড়ায় এবং মাঠে সোনালী বৃষ্টির ধারা ঝরায়।",
                "or": "କଳା ମେଘମାନେ ଆକାଶରେ ନାଚି ନାଚି ବିଲରେ ଅମୃତ ବର୍ଷା କରନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "cloud", "en": "Cloud", "hi": "बादल (Baadal)", "sat": "ᱨᱤᱢᱤᱞ (Rimil)", "meaning": "आकाश में तैरते जल-वाष्प के समूह"},
            {"concept": "thunder", "en": "Thunder / Lightning", "hi": "गरजना (Garajna)", "sat": "ᱜᱟᱰᱨᱟᱣ (Gadrao)", "meaning": "बिजली और मेघों की गंभीर गूँज"}
        ],
        "abhyas_questions": [
            {"q": "कविता में बादलों के गाल कैसे बताए गए हैं?", "hint": "गुब्बारे जैसे फूले हुए"},
            {"q": "काले बादल धरती पर क्या लाते हैं?", "hint": "रिमझिम बारिश और हरियाली"}
        ]
    },
    {
        "id": "cl4_eng_ch1",
        "nipun_code": "L-FLN-02",
        "nipun_outcome": "ध्वनि उच्चारण एवं दैनिक आदतें (Pronunciation & Morning Routines)",
        "grade": 4,
        "grade_label": "कक्षा 4 (Class 4)",
        "subject": "english",
        "subject_name": "Marigold (English)",
        "subject_icon": "🔤",
        "chapter_no": 1,
        "title_hi": "उठो, नया दिन आया! (Wake Up!)",
        "title_en": "Wake Up! - Morning Song",
        "concept_summary": "Wake up, wake up! It's a lovely day. Oh, please get up and come and play!",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Wake up! The birds are singing in the green trees, and the tiny yellow bees are buzzing with sweet honey.",
                "hi": "जागो, नया प्रभात हुआ! हरे पेड़ों पर चिड़ियाँ मीठे गीत गा रही हैं और मधुमक्खियाँ फूलों पर भिनभिना रही हैं।",
                "sat": "ᱵᱮᱨᱮᱫ ᱢᱮ! ᱦᱟᱹᱨᱭᱟᱹᱲ ᱫᱟᱨᱮ ᱨᱮ ᱪᱮᱬᱮ ᱠᱚ ᱥᱤᱵᱤᱞ ᱥᱮᱨᱮᱧ ᱮᱫᱟ ᱟᱨ ᱧᱮᱞᱮ ᱠᱚ ᱵᱟᱦᱟ ᱨᱮ ᱥᱤᱵᱤᱞ ᱨᱟᱥᱟ ᱠᱚ ᱥᱮᱸᱫᱽᱨᱟᱭᱮᱫᱟ᱾",
                "ho": "ᱵᱮᱨᱮᱫ ᱢᱮ! ᱪᱮᱬᱮ ᱠᱚ ᱫᱟᱨᱩ ᱨᱮ ᱫᱩᱨᱟᱝ ᱛᱟᱱᱟ ᱟᱨ ᱛᱮᱨᱚᱢ ᱠᱚ ᱵᱟᱦᱟ ᱨᱮ ᱨᱟᱥᱟ ᱠᱚ ᱦᱟᱨᱟᱣᱟ᱾",
                "unr": "बेरेद मे! चेणे को दारू रे दुरांग तन आर तेरोम को बाहा रे रसा साभावा।",
                "kru": "एठरा! मन्न नू ओड़ा मन पाड़आ लग्गिया अरा तीनी मन पूप नू महक एरआ लग्गिया।",
                "khr": "जागा! गाछ पर चिरई चहचहा रहल हे अउर मधुमक्खी फूल से रस चूस रहल हे।",
                "sck": "जागा भाई जागा! गाछ में चिरई गावेला अउर महुमक्खी रस खोजेला।",
                "bn": "জেগে ওঠো! গাছে পাখিরা মিষ্টি গান গাইছে এবং মৌমাছিরা ফুলের পরাগ সংগ্রহ করছে।",
                "or": "ଉଠିପଡ଼! ଗଛରେ ପକ୍ଷୀମାନେ ମିଠା ଗୀତ ଗାଉଛନ୍ତି ଏବଂ ମହୁମାଛିମାନେ ଉଡୁଛନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "bee", "en": "Honey Bee", "hi": "मधुमक्खी (Madhumakkhi)", "sat": "ᱧᱮᱞᱮ (Nyele)", "meaning": "शहद बनाने वाला कीट"},
            {"concept": "sing", "en": "Sing / Melody", "hi": "गाना (Gaana)", "sat": "ᱥᱮᱨᱮᱧ (Serenj)", "meaning": "मधुर ध्वनि में गीत गाना"}
        ],
        "abhyas_questions": [
            {"q": "What are the birds doing in the morning?", "hint": "They are singing sweet songs (वे गीत गा रही हैं)"},
            {"q": "Who makes sweet honey from flowers?", "hint": "Honey bees (मधुमक्खियाँ)"}
        ]
    },

    # =========================================================================
    # CLASS 5 (Grade 5)
    # =========================================================================
    {
        "id": "cl5_evs_ch1",
        "nipun_code": "E-FLN-01",
        "nipun_outcome": "संवेदी अंग एवं पशु-सूँघने की शक्ति (Animal Senses & Adaptations)",
        "grade": 5,
        "grade_label": "कक्षा 5 (Class 5)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 1,
        "title_hi": "कैसे पहचाना चींटी ने दोस्त को? (अद्भुत ज्ञानेंद्रियाँ)",
        "title_en": "Super Senses of Animals",
        "concept_summary": "चींटियाँ गंध सूंघकर कतार में चलती हैं। रेशम का कीड़ा कई किलोमीटर दूर से साथी की गंध पहचान लेता है।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Animals have amazing senses: eagles can see four times farther than humans, and dogs can smell tiny traces.",
                "hi": "जानवरों में अद्भुत ज्ञानेंद्रियाँ होती हैं: चील हमसे चार गुना दूर देख सकती है और कुत्ते बहुत हल्की गंध भी पहचान लेते हैं।",
                "sat": "ᱡᱤᱭᱟᱹᱞᱤ ᱠᱚᱣᱟᱜ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱟᱹᱭᱠᱟᱹᱣ ᱫᱟᱲᱮ ᱛᱟᱦᱮᱸᱱᱟ: ᱠᱩᱨᱤᱫ ᱟᱵᱚ ᱠᱷᱚᱱ ᱯᱩᱱ ᱜᱩᱬ ᱥᱟᱺᱜᱤᱧ ᱮ ᱧᱮᱞ ᱫᱟᱲᱮᱭᱟᱜᱼᱟ ᱟᱨ ᱥᱮᱛᱟ ᱠᱚ ᱡᱚᱛᱚ ᱠᱷᱚᱱ ᱦᱩᱰᱤᱧ ᱥᱚ ᱦᱚᱸ ᱠᱚ ᱥᱮᱸᱫᱽᱨᱟ ᱧᱟᱢᱟ᱾",
                "ho": "ᱡᱤᱣ ᱠᱚᱣᱟᱜ ᱟᱹᱰᱤ ᱪᱚᱨᱚᱠ ᱟᱹᱭᱠᱟᱹᱣ ᱢᱮᱱᱟᱜᱼᱟ: ᱠᱩᱨᱤᱫ ᱟᱵᱩ ᱠᱷᱚᱱ ᱯᱩᱱ ᱜᱩᱬ ᱥᱟᱺᱜᱤᱧ ᱱᱮᱞ ᱫᱟᱲᱮᱭᱟ ᱟᱨ ᱥᱮᱛᱟ ᱥᱚ ᱪᱤᱱᱦᱟᱹᱣ ᱫᱟᱲᱮᱭᱟ᱾",
                "unr": "जीव कोवाः अडी चोरोक आयकव मेनाः: कुरुद अबु खोन पुन गुण सांगीं नेल दाड़ेया आर सेता सो चिन्हाव दाड़ेया।",
                "kru": "जिया-जन्तु गही अक्कबक्क दव बुझावना शक्ति रई: गिद्ध नाम ती चार गुना दूर एरना सकोस अरा अल्ला महक ती चिन्ही।",
                "khr": "जानवर में अचरज भरल सूंघे अउर देखे के ताकत होवऽ हे: चील हमनी से चार गुना दूर देख सके हे अउर कुकुर गंध पहिचान ले हे।",
                "sck": "जीव-जन्तु मनक अदभुत सूंघेक अउर देखेक शक्ति होवेला: चील चार गुना दूर देखेला अउर कुकुर गंध से पहिचानेला।",
                "bn": "পশুদের চমৎকার ইন্দ্রিয় ক্ষমতা রয়েছে: ঈগল মানুষের চেয়ে চারগুণ দূরে দেখতে পায় এবং কুকুর অতি সামান্য গন্ধও টের পায়।",
                "or": "ପଶୁମାନଙ୍କର ଅଦ୍ଭୁତ ଇନ୍ଦ୍ରିୟ ଶକ୍ତି ଥାଏ: ଚିଲ ମଣିଷ ଠାରୁ ଚାରିଗୁଣ ଦୂର ଦେଖିପାରେ ଏବଂ କୁକୁର ଅତି ସାମାନ୍ୟ ଗନ୍ଧ ମଧ୍ୟ ଶୁଙ୍ଘିପାରେ।"
            }
        ],
        "keywords": [
            {"concept": "eagle", "en": "Eagle", "hi": "चील (Cheel)", "sat": "ᱠᱩᱨᱤᱫ (Kurid)", "meaning": "तेज नजर वाला शिकारी पक्षी"},
            {"concept": "ant", "en": "Ant", "hi": "चींटी (Cheenti)", "sat": "ᱢᱩᱡᱽ (Muj)", "meaning": "कतार में चलने वाला परिश्रमी कीट"}
        ],
        "abhyas_questions": [
            {"q": "चींटियाँ हमेशा एक सीधी कतार में क्यों चलती हैं?", "hint": "एक-दूसरे की गंध सूंघकर"},
            {"q": "रात में जागने वाले जीवों को कौन-से रंग दिखाई देते हैं?", "hint": "सफेद और काला (Black & White)"}
        ]
    },
    {
        "id": "cl5_evs_ch2",
        "nipun_code": "E-FLN-03",
        "nipun_outcome": "पारंपरिक ज्ञान एवं जनजातीय धरोहर (Indigenous Wisdom & Folklore)",
        "grade": 5,
        "grade_label": "कक्षा 5 (Class 5)",
        "subject": "evs",
        "subject_name": "आस-पास (EVS)",
        "subject_icon": "🌿",
        "chapter_no": 2,
        "title_hi": "कहानी सपेरों की (कालबेलिया धरोहर)",
        "title_en": "A Snake Charmer's Story: Kalbelia Heritage",
        "concept_summary": "सपेरे बीन की तान पर साँपों को नचाते हैं। साँप किसानों के मित्र होते हैं क्योंकि वे चूहों को खाकर फसल बचाते हैं।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "Snakes are farmers' friends. They eat mice in paddy fields and protect crops from damage. Snakes do not have external ears; they feel vibrations through the ground.",
                "hi": "साँप किसानों के सच्चे मित्र होते हैं। वे धान के खेतों में चूहों को खाकर फसल की रक्षा करते हैं। साँप के बाहरी कान नहीं होते, वे जमीन के कंपन को महसूस करते हैं।",
                "sat": "ᱵᱤᱧ ᱠᱚ ᱫᱚ ᱪᱟᱹᱥᱤ ᱨᱮᱱ ᱥᱟᱹᱨᱤ ᱜᱟᱛᱮ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱩᱱᱠᱩ ᱦᱳᱲᱳ ᱠᱷᱮᱛ ᱨᱮ ᱪᱩᱴᱤᱭᱟᱹ ᱡᱚᱢ ᱠᱟᱛᱮ ᱪᱟᱥ ᱠᱚ ᱵᱟᱧᱪᱟᱣᱟ᱾ ᱵᱤᱧ ᱨᱮᱱ ᱵᱟᱦᱨᱮ ᱞᱩᱛᱩᱨ ᱵᱟᱹᱱᱩᱜᱼᱟ, ᱩᱱᱠᱩ ᱚᱛ ᱨᱮᱱᱟᱜ ᱛᱷᱟᱨᱛᱷᱟᱨᱟᱣ ᱠᱚ ᱟᱹᱭᱠᱟᱹᱣᱟ᱾",
                "ho": "ᱵᱤᱧ ᱠᱚ ᱠᱤᱥᱟᱹᱱ ᱨᱮᱱ ᱡᱩᱲᱤ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱩᱱᱠᱩ ᱪᱩᱴᱤᱭᱟᱹ ᱡᱚᱢ ᱠᱮᱛᱮ ᱦᱳᱲᱳ ᱵᱟᱧᱪᱟᱣᱟ᱾",
                "unr": "बिं को चासी रेन जोड़ी तना। निकु चुटिया जोम केते होड़ो बंचाओवा।",
                "kru": "ईब्बो मन उइय्यार गही संगिया तली। आर खड्ड नू मूसा मन खना अरा फसल बचअना।",
                "khr": "साँप किसान के बेस संगी हे। उ खेत में मूस खा के धान के फसल बचावे हे।",
                "sck": "साँप किसान कर संगी हेके। ऊ खेत में मूसा के खाय के फसल बचावेला।",
                "bn": "সাপেরা কৃষকদের বন্ধু। তারা জমির ইঁদুর খেয়ে ফসল রক্ষা করে।",
                "or": "ସାପମାନେ କୃଷକମାନଙ୍କର ପ୍ରକୃତ ବନ୍ଧୁ। ସେମାନେ ବିଲରେ ମୂଷା ଖାଇ ଫସଲ ରକ୍ଷା କରନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "snake", "en": "Snake", "hi": "साँप / सर्प (Saanp)", "sat": "ᱵᱤᱧ (Bing)", "meaning": "जमीन पर रेंगने वाला जीव"},
            {"concept": "flute", "en": "Been / Musical Gourd", "hi": "बीन (Been)", "sat": "ᱵᱤᱱ (Bin)", "meaning": "सपेरे का वाद्य यंत्र"}
        ],
        "abhyas_questions": [
            {"q": "साँप को किसानों का मित्र क्यों कहा जाता है?", "hint": "क्योंकि वे चूहों को खाकर फसल बचाते हैं"},
            {"q": "साँप ध्वनि कैसे सुनते हैं?", "hint": "जमीन के कंपन (कंपन) को महसूस करके"}
        ]
    },
    {
        "id": "cl5_math_ch1",
        "nipun_code": "M-FLN-02",
        "nipun_outcome": "व्यावहारिक गणना, मुद्रा एवं वजन (Applied Mathematics & Market Math)",
        "grade": 5,
        "grade_label": "कक्षा 5 (Class 5)",
        "subject": "math",
        "subject_name": "गणित का जादू (Math Magic)",
        "subject_icon": "🔢",
        "chapter_no": 1,
        "title_hi": "मछली उछली (आकृतियाँ, वजन और हाट-बाजार)",
        "title_en": "The Fish Tale: Shapes, Weight and Weekly Haat",
        "concept_summary": "गाँव के साप्ताहिक हाट-बाजार में किलो, क्विंटल, नाव की गति और क्रय-विक्रय का गणितीय हिसाब।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "In the village weekly market, fisherwomen sell fresh fish by kilograms. Math helps them calculate prices and profits accurately.",
                "hi": "गाँव के साप्ताहिक हाट में मछुआरे किलो के हिसाब से ताजी मछलियाँ बेचते हैं। गणित उन्हें सही दाम और बचत गिनने में मदद करता है।",
                "sat": "ᱟᱹᱛᱩ ᱨᱮᱱᱟᱜ ᱦᱟᱯᱛᱟᱠᱤᱭᱟᱹ ᱦᱟᱴ ᱨᱮ ᱦᱟᱹᱠᱩ ᱟᱹᱠᱷᱨᱤᱧ ᱠᱚ ᱠᱤᱞᱳ ᱞᱮᱠᱟᱛᱮ ᱛᱟᱡᱟ ᱦᱟᱹᱠᱩ ᱠᱚ ᱟᱹᱠᱷᱨᱤᱧ ᱠᱚᱣᱟ᱾ ᱞᱮᱠᱷᱟ ᱫᱚ ᱩᱱᱠᱩ ᱴᱷᱤᱠ ᱜᱚᱱᱚᱝ ᱟᱨ ᱞᱟᱵᱷ ᱞᱮᱠᱷᱟ ᱨᱮ ᱜᱚᱲᱚ ᱟᱠᱚᱣᱟ᱾",
                "ho": "ᱦᱟᱛᱩ ᱦᱟᱴ ᱨᱮ ᱦᱟᱹᱠᱩ ᱠᱤᱨᱤᱧ-ᱟᱹᱠᱷᱨᱤᱧ ᱠᱚ ᱠᱤᱞᱳ ᱞᱮᱠᱟᱛᱮ ᱦᱟᱹᱠᱩ ᱟᱹᱠᱷᱨᱤᱧᱟ᱾ ᱞᱮᱠᱷᱟ ᱩᱱᱠᱩ ᱜᱚᱱᱚᱝ ᱦᱤᱥᱟᱹᱵᱽ ᱨᱮ ᱜᱚᱲᱚᱭᱟ᱾",
                "unr": "हतू हाट रे हाकु किरिं-आखरिं को किलो लेकाते हाकु आखरिंया। लेखा उनको गोनोंग हिसाब रे गोड़ोया।",
                "kru": "पद्धा गही पेठिया नू ईंजो बिच्चा गोठियार किलो ती ईंजो बिच्ची। हिसाब आरिन सही दाम गहि हिसाब नू मदत कमची।",
                "khr": "गाँव के हतिया (हाट) में मछरी किलो के हिसाब से बिका हे। गणित से सही हिसाब-किताब अउर फायदा पता चले हे।",
                "sck": "गाँव कर साप्ताहीक हाट में मछरी किलो कर हिसाब से बिकाएला। हिसाब-किताब से सही दाम अउर बचत बुझाएला।",
                "bn": "গ্রামের সাপ্তাহিক হাটে মৎস্যজীবীরা কেজি দরে টাটকা মাছ বিক্রি করেন। গণিত তাদের সঠিক দাম ও লাভ হিসাব করতে সাহায্য করে।",
                "or": "ଗାଁର ସାପ୍ତାହିକ ହାଟରେ ମାଛ ଧରାଳୀମାନେ କିଲୋ ହିସାବରେ ତାଜା ମାଛ ବିକ୍ରି କରନ୍ତି। ଗଣିତ ସେମାନଙ୍କୁ ସଠିକ୍ ଦର ଓ ଲାଭ ଗଣିବାରେ ସାହାଯ୍ୟ କରେ।"
            }
        ],
        "keywords": [
            {"concept": "fish", "en": "Fish", "hi": "मछली (Machhli)", "sat": "ᱦᱟᱹᱠᱩ (Haku)", "meaning": "जल में रहने वाला जीव"},
            {"concept": "market", "en": "Weekly Village Market", "hi": "साप्ताहिक हाट (Haat)", "sat": "ᱦᱟᱴ (Haat)", "meaning": "गाँव का खरीद-बिक्री बाजार"}
        ],
        "abhyas_questions": [
            {"q": "१ किलोग्राम में कितने ग्राम होते हैं?", "hint": "१००० ग्राम (1000g)"},
            {"q": "यदि १ किलो मछली की कीमत ₹150 है, तो २ किलो की कीमत क्या होगी?", "hint": "₹300"}
        ]
    },
    {
        "id": "cl5_hindi_ch1",
        "nipun_code": "L-FLN-04",
        "nipun_outcome": "लोककथा विश्लेषण एवं समस्या-समाधान (Folk Tale Analysis & Wisdom)",
        "grade": 5,
        "grade_label": "कक्षा 5 (Class 5)",
        "subject": "hindi",
        "subject_name": "रिमझिम / भाषा (Hindi)",
        "subject_icon": "📖",
        "chapter_no": 1,
        "title_hi": "राख की रस्सी (लोककथा व बुद्धिमानी)",
        "title_en": "Rope of Ashes - Folk Wisdom",
        "concept_summary": "तिब्बत के मंत्री लोनपो गार अपने सीधे-सादे बेटे के लिए चिंतित थे। लड़की ने अपनी सूझबूझ से राख की रस्सी बनाकर राजा की शर्त पूरी कर दी।",
        "paragraphs": [
            {
                "id": "p1",
                "en": "The clever girl burned a thick twisted rope on a flat stone. The rope burned completely to ashes, leaving a delicate rope shape of ash.",
                "hi": "होशियार लड़की ने पत्थर की सिल पर रस्सी को बड़े ध्यान से जलाया। रस्सी जलकर राख हो गई, पर राख की सुंदर रस्सी का आकार वैसा ही बना रहा।",
                "sat": "ᱪᱟᱞᱟᱠ ᱠᱩᱲᱤ ᱫᱚ ᱫᱷᱤᱨᱤ ᱪᱮᱛᱟᱱ ᱨᱮ ᱵᱟᱵᱮᱨ ᱮ ᱡᱩᱞ ᱠᱮᱫᱟ᱾ ᱵᱟᱵᱮᱨ ᱡᱩᱞ ᱠᱟᱛᱮ ᱛᱚᱨᱚᱡ ᱮᱱᱟ, ᱢᱮᱱᱠᱷᱟᱱ ᱛᱚᱨᱚᱡ ᱵᱟᱵᱮᱨ ᱨᱮᱱᱟᱜ ᱢᱩᱴᱷᱟᱹᱱ ᱚᱱᱠᱟ ᱜᱮ ᱛᱟᱦᱮᱸ ᱮᱱᱟ᱾",
                "ho": "ᱪᱟᱞᱟᱠ ᱠᱩᱲᱤ ᱫᱷᱤᱨᱤ ᱪᱮᱛᱟᱱ ᱨᱮ ᱵᱟᱭᱮᱨ ᱞᱚ ᱠᱮᱫᱟ᱾ ᱵᱟᱭᱮᱨ ᱛᱚᱨᱚᱭ ᱮᱱᱟ, ᱢᱮᱱᱫᱚ ᱛᱚᱨᱚᱭ ᱵᱟᱭᱮᱨ ᱨᱩᱯ ᱛᱟᱭᱠᱮᱱᱟ᱾",
                "unr": "चालाक कुड़ी धीरी चेतान रे बाएर लो केदा। बाएर तोरोय एना, मेनदो तोरोय बाएर रूप ताइकेना।",
                "kru": "चालक कुक्कड़ो धीरी मइया रस्सीन सड़ाआ चीआ। रस्सी सड़रआ तोड़ा मनी, पाहे तोड़ा गही रस्सी रअआ कालो।",
                "khr": "तेज लड़की सिल पर रस्सी रख के जरा देलकै। रस्सी जल के राख हो गेलै, बाकिर राख के रस्सी बनल रहलै।",
                "sck": "चालाक छौड़ी पथल में रस्सी जराए देलक। रस्सी जल के राख भेलक, मने राख कर रस्सी तैयार होय गेलक।",
                "bn": "বুদ্ধিমতী মেয়েটি পাথরের ওপর সাবধানে দড়ি পুড়িয়ে দিল। দড়িটি পুড়ে ছাইয়ের সুন্দর দড়ির আকার নিল।",
                "or": "ଚତୁର ଝିଅଟି ପଥର ଉପରେ ଦଉଡ଼ିକୁ ଜଳାଇଦେଲା। ଦଉଡ଼ିଟି ପୋଡ଼ି ପାଉଁଶର ଦଉଡ଼ି ହୋଇଗଲା।"
            }
        ],
        "keywords": [
            {"concept": "rope", "en": "Rope", "hi": "रस्सी (Rassi)", "sat": "ᱵᱟᱵᱮᱨ (Baber)", "meaning": "सन या जूट से बटी रस्सी"},
            {"concept": "ash", "en": "Ash", "hi": "राख / भस्म (Raakh)", "sat": "ᱛᱚᱨᱚᱡ (Toroj)", "meaning": "जलने के बाद बचा चूर्ण"}
        ],
        "abhyas_questions": [
            {"q": "लड़की ने राख की रस्सी कैसे तैयार की?", "hint": "पत्थर की सिल पर रस्सी रखकर जला दिया"},
            {"q": "इस लोककथा से हमें क्या सीख मिलती है?", "hint": "कठिन से कठिन समस्या का हल सूझबूझ और बुद्धि से निकाला जा सकता है"}
        ]
    },
    {
        "id": "cl5_eng_ch1",
        "nipun_code": "L-FLN-03",
        "nipun_outcome": "ऋतु चक्र एवं सामाजिक उत्सव (Seasons & Community Celebrations)",
        "grade": 5,
        "grade_label": "कक्षा 5 (Class 5)",
        "subject": "english",
        "subject_name": "Marigold (English)",
        "subject_icon": "🔤",
        "chapter_no": 1,
        "title_hi": "आइसक्रीम वाला (The Ice-Cream Man)",
        "title_en": "The Ice-Cream Man",
        "concept_summary": "When summer in the city brings hot heat, the Ice-cream Man comes rolling down the village lane with his cool cart.",
        "paragraphs": [
            {
                "id": "p1",
                "en": "In hot summer days, the Ice-cream Man comes with his round green umbrella. Children gather around like honeybees to taste sweet vanilla and mango cups.",
                "hi": "गर्मियों के दिनों में आइसक्रीम वाला अपनी गोल हरी छतरी लेकर आता है। बच्चे मधुमक्खियों की तरह उसके चारों ओर ठंडी-मीठी कुल्फी और आइसक्रीम खाने के लिए जमा हो जाते हैं।",
                "sat": "ᱥᱤᱛᱩᱝ ᱫᱤᱱ ᱨᱮ ᱟᱭᱤᱥᱠᱨᱤᱢ ᱟᱹᱠᱷᱨᱤᱧ ᱦᱚᱲ ᱟᱡᱟᱜ ᱦᱟᱹᱨᱭᱟᱹᱲ ᱪᱷᱟᱛᱟ ᱤᱫᱤ ᱠᱟᱛᱮ ᱦᱤᱡᱩᱜᱼᱟ᱾ ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱧᱮᱞᱮ ᱞᱮᱠᱟ ᱥᱤᱵᱤᱞ ᱠᱩᱞᱯᱷᱤ ᱡᱚᱢ ᱞᱟᱹᱜᱤᱫ ᱠᱚ ᱡᱟᱣᱨᱟᱜᱼᱟ᱾",
                "ho": "ᱥᱤᱛᱩᱝ ᱫᱤᱱ ᱨᱮ ᱟᱭᱤᱥᱠᱨᱤᱢ ᱟᱹᱠᱷᱨᱤᱧ ᱦᱚᱲ ᱦᱟᱹᱨᱭᱟᱹᱲ ᱪᱷᱟᱛᱟ ᱛᱮ ᱦᱩᱡᱩᱜᱼᱟ᱾ ᱜᱤᱫᱤᱨ ᱠᱚ ᱥᱤᱵᱤᱞ ᱟᱭᱤᱥᱠᱨᱤᱢ ᱡᱚᱢ ᱞᱟᱹᱜᱤᱱ ᱡᱩᱢᱟᱣᱟ᱾",
                "unr": "सितुंग दिन रे आइसक्रीम आखरिं होड़ हरियर छाता ते हिजूआ। होन्हार को सिबिल आइसक्रीम जोम लागिन जुमावा।",
                "kru": "रौद बीड़ी आइसक्रीम बिच्चा गही हरियर छाता नू बरदस। खद्दर मन तीनी लखे मिठा आइसक्रीम मोखआगे जमा मनी।",
                "khr": "गर्मी के दिन में आइसक्रीम वाला हरियर छतरी लेके आवे हे। सब छौआ महुमक्खी नियर ओकर लगे जुट जा हथिन।",
                "sck": "रौद के दिन में आइसक्रीम वाला हरियर छाता लेके आवेला। छौवा मन मीठा-ठंढा आइसक्रीम खाय ले जमा होवेना।",
                "bn": "তপ্ত গ্রীষ্মের দুপুরে আইসক্রিমওয়ালা তার সবুজ ছাতা মাথায় দিয়ে আসে। শিশুরা মৌমাছির মতো তাকে ঘিরে ধরে।",
                "or": "ଖରାଦିନେ ଆଇସକ୍ରିମ୍ ବାଲା ତା'ର ସବୁଜ ଛତା ଧରି ଆସେ। ପିଲାମାନେ ଖୁସିରେ ତା' ଚାରିପାଖେ ଜମା ହୋଇଯାଆନ୍ତି।"
            }
        ],
        "keywords": [
            {"concept": "summer", "en": "Summer", "hi": "गर्मी / ग्रीष्म ऋतु (Garmi)", "sat": "ᱥᱤᱛᱩᱝ (Situng)", "meaning": "धूप और गर्म मौसम"},
            {"concept": "umbrella", "en": "Umbrella", "hi": "छतरी / छाता (Chhata)", "sat": "ᱪᱷᱟᱛᱟ (Chhata)", "meaning": "धूप व वर्षा से बचाव का साधन"}
        ],
        "abhyas_questions": [
            {"q": "In which season does the Ice-cream Man come?", "hint": "In summer season (गर्मी के मौसम में)"},
            {"q": "What do children gather around the cart like?", "hint": "Like honeybees around sweet flowers (मधुमक्खियों की तरह)"}
        ]
    }
]

def get_all_books(grade: Optional[int] = None, subject: Optional[str] = None) -> List[Dict]:
    """Returns chapters filtered by grade and subject with metadata."""
    results = []
    for ch in CURRICULUM_CHAPTERS:
        if grade is not None and ch["grade"] != grade:
            continue
        if subject is not None and subject.lower() != "all" and ch["subject"] != subject.lower():
            continue
        results.append({
            "id": ch["id"],
            "grade": ch["grade"],
            "grade_label": ch["grade_label"],
            "subject": ch["subject"],
            "subject_name": ch["subject_name"],
            "subject_icon": ch["subject_icon"],
            "chapter_no": ch["chapter_no"],
            "title_hi": ch["title_hi"],
            "title_en": ch["title_en"],
            "nipun_code": ch.get("nipun_code", "L-FLN-01"),
            "nipun_outcome": ch.get("nipun_outcome", ""),
            "concept_summary": ch["concept_summary"],
            "total_paragraphs": len(ch["paragraphs"]),
            "keywords_count": len(ch["keywords"])
        })
    return results

def get_chapter_by_id(chapter_id: str, target_lang: str = "sat") -> Optional[Dict]:
    """Fetches full chapter content with dynamic mother tongue adaptation."""
    for ch in CURRICULUM_CHAPTERS:
        if ch["id"] == chapter_id:
            adapted_paragraphs = []
            for p in ch["paragraphs"]:
                text_vernacular = p.get(target_lang, p.get("hi", p.get("en")))
                adapted_paragraphs.append({
                    "id": p["id"],
                    "vernacular": text_vernacular,
                    "hindi": p.get("hi", ""),
                    "english": p.get("en", ""),
                    "sat": p.get("sat", ""),
                    "ho": p.get("ho", ""),
                    "unr": p.get("unr", ""),
                    "kru": p.get("kru", ""),
                    "khr": p.get("khr", ""),
                    "sck": p.get("sck", ""),
                    "bn": p.get("bn", ""),
                    "or": p.get("or", "")
                })

            adapted_keywords = []
            for kw in ch["keywords"]:
                adapted_keywords.append({
                    "concept": kw["concept"],
                    "word": kw.get(target_lang, kw.get("hi")),
                    "hindi": kw["hi"],
                    "english": kw["en"],
                    "meaning": kw["meaning"]
                })

            return {
                "id": ch["id"],
                "grade": ch["grade"],
                "grade_label": ch["grade_label"],
                "subject": ch["subject"],
                "subject_name": ch["subject_name"],
                "subject_icon": ch["subject_icon"],
                "chapter_no": ch["chapter_no"],
                "title_hi": ch["title_hi"],
                "title_en": ch["title_en"],
                "nipun_code": ch.get("nipun_code", "L-FLN-01"),
                "nipun_outcome": ch.get("nipun_outcome", ""),
                "concept_summary": ch["concept_summary"],
                "target_lang": target_lang,
                "paragraphs": adapted_paragraphs,
                "keywords": adapted_keywords,
                "abhyas_questions": ch["abhyas_questions"]
            }
    return None

def get_offline_grade_bundle(grade: Optional[int] = None) -> List[Dict]:
    """Returns the complete curriculum package for offline caching in client IndexedDB."""
    if grade is None:
        return CURRICULUM_CHAPTERS
    return [ch for ch in CURRICULUM_CHAPTERS if ch["grade"] == grade]

def lookup_word_translation(word: str, target_lang: str = "sat", chapter_id: Optional[str] = None) -> Dict:
    """
    Intelligent word-to-word translation lookup for interactive reader.
    Finds exact native script word, roman phonetic pronunciation, Hindi, English, and meaning.
    """
    clean = word.strip(",.!?()[]{}'\"“”‘’।-:;/\n\t ").lower()
    
    # 1. Check direct match in global dictionary
    if clean in GLOBAL_WORD_DICTIONARY:
        entry = GLOBAL_WORD_DICTIONARY[clean]
        return {
            "found": True,
            "original": word,
            "cleaned": clean,
            "translation": entry.get(target_lang, entry.get("hi", word)),
            "phonetic": entry.get("phonetic", ""),
            "hindi": entry.get("hi", ""),
            "english": entry.get("en", ""),
            "meaning": entry.get("meaning", ""),
            "lang": target_lang
        }

    # 2. Check by matching Hindi or English values in global dictionary
    for k, entry in GLOBAL_WORD_DICTIONARY.items():
        if clean == entry.get("hi", "").lower() or clean == entry.get("en", "").lower():
            return {
                "found": True,
                "original": word,
                "cleaned": clean,
                "translation": entry.get(target_lang, entry.get("hi", word)),
                "phonetic": entry.get("phonetic", ""),
                "hindi": entry.get("hi", ""),
                "english": entry.get("en", ""),
                "meaning": entry.get("meaning", ""),
                "lang": target_lang
            }

    # 3. Check chapter keywords if chapter_id supplied
    if chapter_id:
        for ch in CURRICULUM_CHAPTERS:
            if ch["id"] == chapter_id:
                for kw in ch["keywords"]:
                    if clean in kw["concept"].lower() or clean in kw["en"].lower() or clean in kw["hi"].lower():
                        return {
                            "found": True,
                            "original": word,
                            "cleaned": clean,
                            "translation": kw.get(target_lang, kw.get("hi", word)),
                            "phonetic": kw.get("concept", "").title(),
                            "hindi": kw["hi"],
                            "english": kw["en"],
                            "meaning": kw["meaning"],
                            "lang": target_lang
                        }

    # 4. Fallback for tribal scripts or phonetic echo
    return {
        "found": False,
        "original": word,
        "cleaned": clean,
        "translation": word,
        "phonetic": clean,
        "hindi": word,
        "english": word,
        "meaning": "शब्दावली संदर्भ (Vocabulary Reference)",
        "lang": target_lang
    }
