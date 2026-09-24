/**
 * Matrubhasa AI — Comprehensive Multilingual Mother Tongue & i18n Localization Engine
 * Supports 10 Vernacular & Indigenous Languages:
 *   - sat: ᱥᱟᱱᱛᱟᱲᱤ (Santali - Ol Chiki)
 *   - ho:  ᱦᱳ / हो (Ho - Warang Citi / Devanagari)
 *   - unr: मुंडारी (Mundari)
 *   - kru: कुड़ुख़ (Kurukh - Oraon)
 *   - khr: खोरठा (Khortha)
 *   - sck: नागपुरी (Nagpuri - Sadri)
 *   - hi:  हिन्दी (Hindi)
 *   - bn:  বাংলা (Bengali)
 *   - or:  ଓଡ଼ିଆ (Odia)
 *   - en:  English
 */

const MOTHER_TONGUES = {
  sat: {
    code: 'sat',
    name_en: 'Santali',
    name_native: 'ᱥᱟᱱᱛᱟᱲᱤ',
    script: 'Ol Chiki (ᱚᱞ ᱪᱤᱠᱤ)',
    region: 'Santhal Pargana, Dumka, Jamtara',
    flag: '🌿',
    audioGreeting: 'ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ! ᱟᱭᱳ ᱟᱲᱟᱝ ᱥᱟᱱᱛᱟᱲᱤ ᱵᱟᱪᱷᱟᱣ ᱮᱱᱟ᱾',
    shortLabel: 'ᱥᱟᱱᱛᱟᱲᱤ (Santali)'
  },
  ho: {
    code: 'ho',
    name_en: 'Ho',
    name_native: 'ᱦᱳ / हो',
    script: 'Warang Citi / Devanagari',
    region: 'Kolhan Division, West Singhbhum, Chaibasa',
    flag: '🏹',
    audioGreeting: 'ᱡᱚᱦᱟᱨ! ᱦᱳ ᱠᱟᱡᱤ ᱵᱟᱪᱷᱟᱣ ᱮᱱᱟ᱾',
    shortLabel: 'ᱦᱳ (Ho)'
  },
  unr: {
    code: 'unr',
    name_en: 'Mundari',
    name_native: 'मुंडारी / मुण्डारी',
    script: 'Devanagari / Ol Onol',
    region: 'Ranchi, Khunti, Torpa',
    flag: '🌾',
    audioGreeting: 'जोहार! अयंग काजी मुंडारी बाछाव एना।',
    shortLabel: 'मुंडारी (Mundari)'
  },
  kru: {
    code: 'kru',
    name_en: 'Kurukh (Oraon)',
    name_native: 'कुड़ुख़',
    script: 'Tolong Siki / Devanagari',
    region: 'Chota Nagpur, Gumla, Lohardaga',
    flag: '🍃',
    audioGreeting: 'जय जोहार! कुड़ुख़ कत्था चुनरा।',
    shortLabel: 'कुड़ुख़ (Kurukh)'
  },
  khr: {
    code: 'khr',
    name_en: 'Khortha',
    name_native: 'खोरठा',
    script: 'Devanagari',
    region: 'Dhanbad, Bokaro, Hazaribagh, Giridih',
    flag: '🌄',
    audioGreeting: 'जोहार! आपन मायकोर भाषा खोरठा चुनली।',
    shortLabel: 'खोरठा (Khortha)'
  },
  sck: {
    code: 'sck',
    name_en: 'Nagpuri (Sadri)',
    name_native: 'नागपुरी (सादरी)',
    script: 'Devanagari',
    region: 'Ranchi, Simdega, Gumla, Khunti',
    flag: '🌺',
    audioGreeting: 'जोहार! नागपुरी भाषा चुनल गेलक।',
    shortLabel: 'नागपुरी (Nagpuri)'
  },
  hi: {
    code: 'hi',
    name_en: 'Hindi',
    name_native: 'हिन्दी',
    script: 'Devanagari',
    region: 'Pan-India & Jharkhand',
    flag: '🇮🇳',
    audioGreeting: 'नमस्ते! मातृभाषा हिन्दी चुनी गई।',
    shortLabel: 'हिन्दी (Hindi)'
  },
  bn: {
    code: 'bn',
    name_en: 'Bengali',
    name_native: 'বাংলা',
    script: 'Bengali',
    region: 'East Singhbhum, Jamtara, Pakur',
    flag: '🌸',
    audioGreeting: 'নমস্কার! মাতৃভাষা বাংলা নির্বাচন করা হয়েছে।',
    shortLabel: 'বাংলা (Bengali)'
  },
  or: {
    code: 'or',
    name_en: 'Odia',
    name_native: 'ଓଡ଼ିଆ',
    script: 'Odia',
    region: 'Saraikela-Kharsawan, East Singhbhum',
    flag: '☀️',
    audioGreeting: 'ନମସ୍କାର! ମାତୃଭାଷା ଓଡ଼ିଆ ଚୟନ କରାଗଲା।',
    shortLabel: 'ଓଡ଼ିଆ (Odia)'
  },
  en: {
    code: 'en',
    name_en: 'English',
    name_native: 'English',
    script: 'Latin',
    region: 'Curriculum Associate',
    flag: '🌐',
    audioGreeting: 'Welcome! Mother tongue set to English.',
    shortLabel: 'English'
  }
};

const UI_TRANSLATIONS = {
  // Global & Header
  gov_authority: {
    sat: '🇮🇳 ᱥᱢᱟᱨᱴ ᱤᱱᱰᱤᱭᱟ ᱦᱮᱠᱟᱛᱷᱚᱱ ᱒᱐᱒᱖ • SIH26042 • ᱡᱷᱟᱨᱠᱷᱚᱸᱰ ᱥᱚᱨᱠᱟᱨ',
    ho: '🇮🇳 ᱥᱢᱟᱨᱴ ᱤᱱᱰᱤᱭᱟ ᱦᱮᱠᱟᱛᱷᱚᱱ ᱒᱐᱒᱖ • SIH26042 • ᱡᱷᱟᱨᱠᱷᱚᱸᱰ ᱥᱚᱨᱠᱟᱨ',
    unr: '🇮🇳 स्मार्ट इंडिया हैकाथॉन 2026 • SIH26042 • झारखण्ड सरकार',
    kru: '🇮🇳 स्मार्ट इंडिया हैकाथॉन 2026 • SIH26042 • झारखण्ड सरकार',
    khr: '🇮🇳 स्मार्ट इंडिया हैकाथॉन 2026 • SIH26042 • झारखंड सरकार',
    sck: '🇮🇳 स्मार्ट इंडिया हैकाथॉन 2026 • SIH26042 • झारखंड सरकार',
    hi: '🇮🇳 स्मार्ट इंडिया हैकाथॉन 2026 • SIH26042 • झारखण्ड सरकार — स्कूली शिक्षा विभाग',
    bn: '🇮🇳 স্মার্ট ইন্ডিয়া হ্যাকাথন ২০২৬ • SIH26042 • ঝাড়খণ্ড সরকার',
    or: '🇮🇳 ସ୍ମାର୍ଟ ଇଣ୍ଡିଆ ହ୍ୟାକାଥନ୍ ୨୦୨୬ • SIH26042 • ଝାଡ଼ଖଣ୍ଡ ସରକାର',
    en: '🇮🇳 Smart India Hackathon 2026 • SIH26042 • Govt. of Jharkhand — Dept. of School Education'
  },
  nep_aligned: {
    sat: 'NEP ᱒᱐᱒᱐ ᱟᱨ ᱱᱤᱯᱩᱱ ᱵᱷᱟᱨᱚᱛ ᱥᱟᱶ ᱡᱚᱲᱟᱣ',
    ho: 'NEP ᱒᱐᱒᱐ ᱟᱨ ᱱᱤᱯᱩᱱ ᱵᱷᱟᱨᱚᱛ ᱥᱟᱶ ᱡᱚᱲᱟᱣ',
    unr: 'NEP 2020 आर निपुण भारत संगे जुड़ल',
    kru: 'NEP 2020 अरा निपुण भारत संगे',
    khr: 'NEP 2020 अउर निपुण भारत के संग',
    sck: 'NEP 2020 अउर निपुण भारत संगे जुड़ल',
    hi: 'राष्ट्रीय शिक्षा नीति NEP 2020 एवं निपुण भारत संरेखित',
    bn: 'NEP ২০২০ ও নিপুণ ভারত সংলগ্ন',
    or: 'NEP ୨୦୨୦ ଏବଂ ନିପୁଣ ଭାରତ ସଂଯୁକ୍ତ',
    en: 'NEP 2020 & NIPUN Bharat Aligned'
  },
  bhashini_powered: {
    sat: 'ᱵᱷᱟᱥᱤᱬᱤ (NLTM) ᱫᱟᱲᱮ',
    ho: 'ᱵᱷᱟᱥᱤᱬᱤ (NLTM) ᱫᱟᱲᱮ',
    unr: 'भाषिणी (NLTM) शक्ति',
    kru: 'भाषिणी (NLTM) शक्ति',
    khr: 'भाषिणी (NLTM) समर्थित',
    sck: 'भाषिणी (NLTM) शक्ति',
    hi: 'भाषिणी (NLTM) समर्थित',
    bn: 'ভাষিণী (NLTM) চালিত',
    or: 'ଭାଷିଣୀ (NLTM) ସମର୍ଥିତ',
    en: 'Bhashini (NLTM) Powered'
  },
  network_online: {
    sat: '🟢 ᱵᱷᱟᱥᱤᱬᱤ ᱠᱞᱟᱣᱩᱰ ᱡᱚᱲᱟᱣ',
    ho: '🟢 ᱵᱷᱟᱥᱤᱬᱤ ᱠᱞᱟᱣᱩᱰ ᱡᱚᱲᱟᱣ',
    unr: '🟢 भाषिणी क्लाउड जुड़ल',
    kru: '🟢 भाषिणी क्लाउड जुड़ल',
    khr: '🟢 भाषिणी क्लाउड जुड़ल हे',
    sck: '🟢 भाषिणी क्लाउड एक्टिव',
    hi: '🟢 भाषिणी क्लाउड सक्रिय',
    bn: '🟢 ভাষিণী ক্লাউড সংযুক্ত',
    or: '🟢 ଭାଷିଣୀ କ୍ଲାଉଡ୍ ସକ୍ରିୟ',
    en: '🟢 Bhashini Cloud Connected'
  },
  network_offline: {
    sat: '🟡 ᱟᱹᱛᱩ ᱚᱯᱷᱞᱟᱭᱤᱱ ᱢᱚᱰ',
    ho: '🟡 ᱦᱟᱛᱩ ᱚᱯᱷᱞᱟᱭᱤᱱ ᱢᱚᱰ',
    unr: '🟡 गाँव ऑफलाइन मोड (कैश)',
    kru: '🟡 गाँव ऑफलाइन मोड',
    khr: '🟡 गाँव ऑफलाइन मोड (लोकल)',
    sck: '🟡 गाँव ऑफलाइन मोड',
    hi: '🟡 गाँव ऑफलाइन मोड (लोकल कैश)',
    bn: '🟡 গ্রাম অফলাইন মোড (ক্যাশ)',
    or: '🟡 ଗ୍ରାମ ଅଫଲାଇନ୍ ମୋଡ୍ (କ୍ୟାଶ୍)',
    en: '🟡 Gaon Offline Mode (Edge Cache)'
  },
  hero_title: {
    sat: 'ᱢᱟᱛᱨᱩᱵᱷᱟᱥᱟ AI <span>• Matrubhasa</span>',
    ho: 'ᱢᱟᱛᱨᱩᱵᱷᱟᱥᱟ AI <span>• Matrubhasa</span>',
    unr: 'मातृभाषा AI <span>• Matrubhasa</span>',
    kru: 'मातृभाषा AI <span>• Matrubhasa</span>',
    khr: 'मातृभाषा AI <span>• Matrubhasa</span>',
    sck: 'मातृभाषा AI <span>• Matrubhasa</span>',
    hi: 'मातृभाषा AI <span>• Matrubhasa</span>',
    bn: 'মাতৃভাষা AI <span>• Matrubhasa</span>',
    or: 'ମାତୃଭାଷା AI <span>• Matrubhasa</span>',
    en: 'Matrubhasa AI <span>• Vernacular Bridge</span>'
  },
  hero_subtitle: {
    sat: 'ᱟᱭᱳ ᱟᱲᱟᱝ ᱛᱮ ᱯᱩᱭᱞᱩ ᱥᱮᱪᱮᱫ ᱞᱟᱹᱜᱤᱫ AI ᱥᱮᱛᱩ ᱟᱨ ᱪᱟᱱᱟᱪ ᱨᱚᱲ ᱛᱚᱨᱡᱚᱢᱟ',
    ho: 'ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱛᱮ ᱤᱛᱩᱱ ᱞᱟᱹᱜᱤᱱ AI ᱥᱮᱛᱩ ᱟᱨ ᱪᱟᱱᱟᱪ ᱠᱟᱡᱤ ᱛᱚᱨᱡᱚᱢᱟ',
    unr: 'अयंग काजी ते प्राथमिक शिक्षा लागिन AI सेतु आर कक्षा अनुवाद',
    kru: 'मातृभाषा नू प्राथमिक पढ़ाई ले AI सेतु अरा कक्षा अनुवाद',
    khr: 'आपन मायकोर भाषा में प्राथमिक पढ़ाई ले AI सेतु अउर तुरंते अनुवाद',
    sck: 'माय-कर बोली में प्राथमिक शिक्षा ले AI सेतु अउर कक्षा अनुवाद',
    hi: 'मातृभाषा आधारित प्राथमिक शिक्षा हेतु AI-संचालित कक्षा सेतु एवं तात्कालिक अनुवाद',
    bn: 'মাতৃভাষা ভিত্তিক প্রাথমিক শিক্ষার জন্য AI চালিত ক্লাসরুম সেতু ও রিয়েল-টাইম অনুবাদ',
    or: 'ମାତୃଭାଷା ଆଧାରିତ ପ୍ରାଥମିକ ଶିକ୍ଷା ପାଇଁ AI ଚାଳିତ ଶ୍ରେଣୀଗୃହ ସେତୁ ଓ ଅନୁବାଦ',
    en: 'AI-Powered Vernacular Pedagogy & Real-Time Classroom Voice Bridge for Primary Education'
  },
  mascot_speech: {
    sat: 'ᱟᱢᱟᱜ ᱜᱤᱫᱽᱨᱟᱹ ᱜᱟᱛᱮ ᱟᱨ ᱯᱟᱹᱨᱥᱤ ᱡᱩᱲᱤ!',
    ho: 'ᱟᱢᱟᱜ ᱜᱤᱫᱤᱨ ᱡᱩᱲᱤ ᱟᱨ ᱠᱟᱡᱤ ᱥᱟᱸᱜᱟᱛ!',
    unr: 'आमाः बाल मित्र आर अयंग काजी संगी!',
    kru: 'निग्है बाल मित्र अरा कत्था संगिया!',
    khr: 'तोहीन कर बाल मित्र अउर भाषा संगी!',
    sck: 'रउरे कर बाल मित्र अउर भाषा संगी!',
    hi: 'आपका बाल मित्र एवं भाषा साथी!',
    bn: 'আপনার শিশু বন্ধু ও ভাষা সাথী!',
    or: 'ଆପଣଙ୍କର ଶିଶୁ ବନ୍ଧୁ ଏବଂ ଭାଷା ସାଥୀ!',
    en: 'Your Friendly Vernacular Learning Mascot!'
  },

  // Navigation Tabs
  tab_dashboard: {
    sat: 'ᱢᱩᱲᱩᱫ ᱛᱟᱞᱢᱟ (Dashboard)',
    ho: 'ᱢᱩᱲᱩᱫ ᱛᱟᱞᱢᱟ (Dashboard)',
    unr: 'डैशबोर्ड (Dashboard)',
    kru: 'मुख्य अखाड़ा (Dashboard)',
    khr: 'डैशबोर्ड (Dashboard)',
    sck: 'मुख्य मंच (Dashboard)',
    hi: 'डैशबोर्ड (Dashboard)',
    bn: 'ড্যাশবোর্ড (Dashboard)',
    or: 'ଡ୍ୟାସବୋର୍ଡ (Dashboard)',
    en: 'Dashboard (Home)'
  },
  tab_live: {
    sat: 'ᱪᱟᱱᱟᱪ ᱥᱮᱛᱩ (Live Bridge)',
    ho: 'ᱪᱟᱱᱟᱪ ᱥᱮᱛᱩ (Live Bridge)',
    unr: 'कक्षा सेतु (Live Bridge)',
    kru: 'क्लासरूम सेतु (Live Bridge)',
    khr: 'क्लासरूम सेतु (Live Mic)',
    sck: 'कक्षा सेतु (Live Bridge)',
    hi: 'कक्षा सेतु (Classroom Live Bridge)',
    bn: 'ক্লাসরুম সেতু (Live Bridge)',
    or: 'ଶ୍ରେଣୀଗୃହ ସେତୁ (Live Bridge)',
    en: 'Classroom Live Bridge (Mic)'
  },
  tab_pathshala: {
    sat: 'ᱯᱟᱲᱦᱟᱣ ᱞᱮᱱᱥ (Pathshala Lens)',
    ho: 'ᱤᱛᱩᱱ ᱞᱮᱱᱥ (Pathshala Lens)',
    unr: 'पाठशाला लेन्स (Pathshala)',
    kru: 'पाठशाला लेन्स (Pathshala)',
    khr: 'पाठशाला लेन्स (Desi Kahani)',
    sck: 'पाठशाला लेन्स (Folk Story)',
    hi: 'पाठशाला लेन्स (देशी कहानी व पत्रक)',
    bn: 'পাঠশালা লেন্স (Pathshala Lens)',
    or: 'ପାଠଶାଳା ଲେନ୍ସ (Pathshala Lens)',
    en: 'Pathshala Lens (Folk Story & PDF)'
  },
  tab_balvatika: {
    sat: 'ᱯᱟᱹᱨᱥᱤ ᱜᱟᱛᱮ (Bhasha Mitr FLN)',
    ho: 'ᱠᱟᱡᱤ ᱡᱩᱲᱤ (Bhasha Mitr FLN)',
    unr: 'भाषा मित्र (Bhasha Mitr FLN)',
    kru: 'कत्था संगिया (Bhasha Mitr FLN)',
    khr: 'भाषा संगी (निपुण बाल वाटिका)',
    sck: 'भाषा संगी (बाल वाटिका FLN)',
    hi: 'भाषा मित्र (बाल वाटिका FLN)',
    bn: 'ভাষা মিত্র (বাল বাটিকা FLN)',
    or: 'ଭାଷା ମିତ୍ର (ବାଳ ବାଟିକା FLN)',
    en: 'Bhasha Mitr (NIPUN FLN Coach)'
  },
  tab_books: {
    sat: 'ᱯᱩᱛᱷᱤ ᱢᱟᱞᱟ (JCERT/NCERT)',
    ho: 'ᱯᱩᱛᱷᱤ ᱟᱠᱷᱲᱟ (JCERT/NCERT)',
    unr: 'पुथी माला (ई-किताबें)',
    kru: 'पुथी भंडार (ई-पुस्तकालय)',
    khr: 'ई-किताब घर (कक्षा 1-5)',
    sck: 'किताब घर (JCERT/NCERT)',
    hi: 'JCERT/NCERT Books (ई-पुस्तकालय)',
    bn: 'ই-পুস্তকালয় (JCERT/NCERT)',
    or: 'ଇ-ପାଠାଗାର (JCERT/NCERT)',
    en: 'JCERT/NCERT Digital Books'
  },
  tab_akshar: {
    sat: 'ᱚᱞ ᱪᱤᱠᱤ ᱟᱨ ᱟᱲᱟᱝ (Akshar Mala)',
    ho: 'ᱣᱟᱨᱟᱝ ᱪᱤᱛᱤ ᱟᱲᱟᱝ (Akshar Mala)',
    unr: 'आखर ध्वनि (Akshar Mala)',
    kru: 'तोलोंग सिकि व ध्वनि (Akshar Mala)',
    khr: 'आखर अउर आवाज (Akshar Mala)',
    sck: 'आखर ध्वनि (Akshar Mala)',
    hi: 'अक्षर व ध्वनि (Akshar Mala)',
    bn: 'বর্ণমালা ও ধ্বনি (Akshar Mala)',
    or: 'ଅକ୍ଷରମାଳା ଓ ଧ୍ୱନି (Akshar Mala)',
    en: 'Akshar Mala (Soundboard & Phonics)'
  },
  tab_hub: {
    sat: 'ᱢᱟᱪᱮᱫ ᱟᱨ ᱟᱭᱳ-ᱵᱟᱵᱟ ᱟᱠᱷᱲᱟ (Teacher & Parent Hub)',
    ho: 'ᱢᱟᱪᱮᱫ ᱟᱨ ᱮᱸᱜᱟ-ᱟᱯᱩ ᱢᱚᱸᱪ (Teacher & Parent Hub)',
    unr: 'माचेत आर अयंग-अपूम मंच (Teacher & Parent Hub)',
    kru: 'गुरु अरा तंगियो-तम्बंग मंच (Teacher & Parent Hub)',
    khr: 'मास्टर अउर माय-बाप मंच (Teacher & Parent Hub)',
    sck: 'गुरुजी अउर अभिभावक मंच (Teacher & Parent Hub)',
    hi: 'शिक्षक व अभिभावक मंच (Teacher & Parent Hub)',
    bn: 'শিক্ষক ও অভিভাবক কেন্দ্র (Teacher & Parent Hub)',
    or: 'ଶିକ୍ଷକ ଓ ଅଭିଭାବକ ମଞ୍ଚ (Teacher & Parent Hub)',
    en: 'Sikshak & Parent Hub (Voice SMS)'
  },

  // Auth Screen / Modal
  auth_choose_lang_title: {
    sat: '🌐 ᱟᱢᱟᱜ ᱟᱭᱳ ᱟᱲᱟᱝ ᱵᱟᱪᱷᱟᱣ ᱢᱮ / Select Mother Tongue:',
    ho: '🌐 ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱵᱟᱪᱷᱟᱣ ᱢᱮ / Select Mother Tongue:',
    unr: '🌐 अयंग काजी बाछाव में / Select Mother Tongue:',
    kru: '🌐 तंग्है मातृभाषा चुनरा / Select Mother Tongue:',
    khr: '🌐 आपन मायकोर भाषा चुना / Select Mother Tongue:',
    sck: '🌐 आपन मातृभाषा चुनू / Select Mother Tongue:',
    hi: '🌐 अपनी मातृभाषा चुनें / Select Your Mother Tongue:',
    bn: '🌐 আপনার মাতৃভাষা বেছে নিন / Select Mother Tongue:',
    or: '🌐 ନିଜ ମାତୃଭାଷା ଚୟନ କରନ୍ତୁ / Select Mother Tongue:',
    en: '🌐 Choose Your Mother Tongue / अपनी मातृभाषा चुनें:'
  },
  auth_choose_lang_sub: {
    sat: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    ho: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    unr: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    kru: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    khr: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    sck: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ᱤଆ • English',
    hi: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    bn: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    or: 'ᱥᱟᱱᱛᱟᱲᱤ • ᱦᱳ • मुंडारी • कुड़ुख़ • खोरठा • नागपुरी • हिन्दी • বাংলা • ଓଡ଼ିଆ • English',
    en: 'Santali • Ho • Mundari • Kurukh • Khortha • Nagpuri • Hindi • Bengali • Odia • English'
  },
  role_teacher: {
    sat: '👨‍🏫 ᱢᱟᱪᱮᱫ (Teacher)',
    ho: '👨‍🏫 ᱢᱟᱪᱮᱫ (Teacher)',
    unr: '👨‍🏫 माचेत (Teacher)',
    kru: '👨‍🏫 मास्टर (Teacher)',
    khr: '👨‍🏫 मास्टर जी (Teacher)',
    sck: '👨‍🏫 गुरुजी (Teacher)',
    hi: '👨‍🏫 शिक्षक (Teacher)',
    bn: '👨‍🏫 শিক্ষক (Teacher)',
    or: '👨‍🏫 ଶିକ୍ଷକ (Teacher)',
    en: '👨‍🏫 Teacher'
  },
  role_student: {
    sat: '🎒 ᱪᱮᱛᱮᱫᱤᱭᱟᱹ (Student)',
    ho: '🎒 ᱤᱛᱩᱱ ᱜᱤᱫᱤᱨ (Student)',
    unr: '🎒 चेड़ा / होन्हार (Student)',
    kru: '🎒 खद्दर (Student)',
    khr: '🎒 पढ़वइया छौआ (Student)',
    sck: '🎒 छौवा / पढ़वइया (Student)',
    hi: '🎒 विद्यार्थी (Student)',
    bn: '🎒 শিক্ষার্থী (Student)',
    or: '🎒 ଛାତ୍ରଛାତ୍ରୀ (Student)',
    en: '🎒 Student'
  },
  role_parent: {
    sat: '👨‍👩‍👦 ᱟᱭᱳ-ᱵᱟᱵᱟ (Parent)',
    ho: '👨‍👩‍👦 ᱮᱸᱜᱟ-ᱟᱯᱩ (Parent)',
    unr: '👨‍👩‍👦 अयंग-अपूम (Parent)',
    kru: '👨‍👩‍👦 तंगियो-तम्बंग (Parent)',
    khr: '👨‍👩‍👦 माय-बाप (Parent)',
    sck: '👨‍👩‍👦 माय-बाप (Parent)',
    hi: '👨‍👩‍👦 अभिभावक (Parent)',
    bn: '👨‍👩‍👦 অভিভাবক (Parent)',
    or: '👨‍👩‍👦 ଅଭିଭାବକ (Parent)',
    en: '👨‍👩‍👦 Parent'
  },
  auth_name_label: {
    sat: 'ᱯᱩᱨᱟᱹ ᱧᱩᱛᱩᱢ (Full Name):',
    ho: 'ᱯᱩᱨᱟᱹ ᱧᱩᱛᱩᱢ (Full Name):',
    unr: 'पूरा नाम (Full Name):',
    kru: 'पूरा नाम (Full Name):',
    khr: 'पूरा नाम (Full Name):',
    sck: 'पूरा नाम (Full Name):',
    hi: 'पूरा नाम (Full Name):',
    bn: 'সম্পূর্ণ নাম (Full Name):',
    or: 'ସମ୍ପୂର୍ଣ୍ଣ ନାମ (Full Name):',
    en: 'Full Name:'
  },
  auth_email_label: {
    sat: 'ᱥᱚᱨᱠᱟᱨᱤ / ᱯᱟᱨᱥᱟᱞ ᱤᱢᱮᱞ (Official Email):',
    ho: 'ᱤᱢᱮᱞ ᱴᱷᱤᱠᱟᱹᱱᱟ (Official Email):',
    unr: 'ईमेल पता (Email Address):',
    kru: 'ईमेल पता (Email Address):',
    khr: 'ईमेल पता (Email Address):',
    sck: 'ईमेल पता (Email Address):',
    hi: 'आधिकारिक ईमेल पता (Official Email):',
    bn: 'অফিসিয়াল ইমেল ঠিকানা (Official Email):',
    or: 'ଅଫିସିଆଲ୍ ଇମେଲ୍ ଠିକଣା (Official Email):',
    en: 'Official Email Address:'
  },
  auth_send_otp: {
    sat: 'OTP ᱵᱷᱮᱡᱟᱭ ᱢᱮ 📨',
    ho: 'OTP ᱠᱩᱞ ᱢᱮ 📨',
    unr: 'OTP भेजो 📨',
    kru: 'OTP तैयबा 📨',
    khr: 'OTP भेजऽ 📨',
    sck: 'OTP भेजू 📨',
    hi: 'OTP भेजें 📨',
    bn: 'OTP পাঠান 📨',
    or: 'OTP ପଠାନ୍ତୁ 📨',
    en: 'Send OTP 📨'
  },
  auth_enter_otp_label: {
    sat: '᱔-ᱮᱞ ᱨᱤᱭᱟᱞ-ᱴᱟᱭᱤᱢ OTP ᱚᱞ ᱢᱮ:',
    ho: '᱔-ᱮᱞ OTP ᱚᱞ ᱢᱮ:',
    unr: '4-अंक OTP कोड दर्ज करू:',
    kru: '4-अंक OTP कोड तइंका:',
    khr: '4-अंक OTP कोड दर्ज करा:',
    sck: '4-अंक OTP कोड लिखू:',
    hi: '4-अंक रीयल-टाइम OTP दर्ज करें:',
    bn: '৪-সংখ্যার রিয়েল-টাইম OTP দিন:',
    or: '୪-ଅଙ୍କ ବିଶିଷ୍ଟ OTP ଦାଖଲ କରନ୍ତୁ:',
    en: 'Enter 4-Digit Real-Time OTP:'
  },
  auth_verify_btn: {
    sat: '🔐 ᱯᱚᱨᱢᱟᱬ ᱟᱨ ᱢᱟᱛᱨᱩᱵᱷᱟᱥᱟ ᱨᱮ ᱵᱚᱞᱚᱱ ᱢᱮ',
    ho: '🔐 ᱯᱚᱨᱢᱟᱬ ᱟᱨ ᱢᱟᱛᱨᱩᱵᱷᱟᱥᱟ ᱨᱮ ᱵᱚᱞᱚ ᱢᱮ',
    unr: '🔐 सत्यापित करू आर मातृभाषा में प्रवेश करू',
    kru: '🔐 प्रमाणित अरा मातृभाषा नू बरा',
    khr: '🔐 सत्यापित करा अउर मातृभाषा में प्रवेश करा',
    sck: '🔐 सत्यापित करू अउर मातृभाषा में प्रवेश करू',
    hi: '🔐 सत्यापित करें एवं मातृभाषा में प्रवेश करें',
    bn: '🔐 যাচাই করুন ও মাতৃভাষায় প্রবেশ করুন',
    or: '🔐 ଯାଞ୍ଚ କରନ୍ତୁ ଏବଂ ମାତୃଭାଷାରେ ପ୍ରବେଶ କରନ୍ତୁ',
    en: '🔐 Verify & Enter Matrubhasa'
  },
  demo_divider: {
    sat: '⚡ ᱟᱨᱵᱟᱝ ᱑-ᱴᱮᱯ ᱰᱮᱢᱳ ᱵᱚᱞᱚᱱ (QUICK 1-TAP DEMO ACCESS)',
    ho: '⚡ ᱟᱨᱵᱟᱝ ᱑-ᱴᱮᱯ ᱰᱮᱢᱳ ᱵᱚᱞᱚᱱ (QUICK 1-TAP DEMO ACCESS)',
    unr: '⚡ अथवा 1-टैप डेमो प्रवेश (QUICK 1-TAP DEMO ACCESS)',
    kru: '⚡ 1-टैप डेमो प्रवेश (QUICK 1-TAP DEMO ACCESS)',
    khr: '⚡ या 1-टैप तुरंत डेमो प्रवेश (QUICK 1-TAP DEMO ACCESS)',
    sck: '⚡ या 1-टैप डेमो प्रवेश (QUICK 1-TAP DEMO ACCESS)',
    hi: '⚡ अथवा त्वरित 1-टैप डेमो प्रवेश (QUICK 1-TAP DEMO ACCESS)',
    bn: '⚡ অথবা দ্রুত ১-ট্যাপ ডেমো অ্যাক্সেস (QUICK DEMO ACCESS)',
    or: '⚡ କିମ୍ବା ୧-ଟ୍ୟାପ୍ ଡେମୋ ପ୍ରବେଶ (QUICK 1-TAP DEMO ACCESS)',
    en: '⚡ OR QUICK 1-TAP DEMO ACCESS'
  },
  demo_teacher_title: {
    sat: 'ᱢᱟᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Teacher)',
    ho: 'ᱢᱟᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Teacher)',
    unr: 'माचेत रूप रे डेमो (Teacher)',
    kru: 'मास्टर रूप नू डेमो (Teacher)',
    khr: 'मास्टर जी के रूप में डेमो (Teacher)',
    sck: 'गुरुजी रूप में डेमो (Teacher)',
    hi: 'शिक्षक के रूप में डेमो (Teacher)',
    bn: 'শিক্ষক হিসেবে ডেমো (Teacher)',
    or: 'ଶିକ୍ଷକ ଭାବେ ଡେମୋ (Teacher)',
    en: 'Demo as Teacher'
  },
  demo_student_title: {
    sat: 'ᱪᱮᱛᱮᱫᱤᱭᱟᱹ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Student)',
    ho: 'ᱤᱛᱩᱱ ᱜᱤᱫᱤᱨ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Student)',
    unr: 'चेड़ा रूप रे डेमो (Student)',
    kru: 'खद्दर रूप नू डेमो (Student)',
    khr: 'पढ़वइया छौआ के रूप में डेमो (Student)',
    sck: 'छौवा रूप में डेमो (Student)',
    hi: 'विद्यार्थी के रूप में डेमो (Student)',
    bn: 'শিক্ষার্থী হিসেবে ডেমো (Student)',
    or: 'ଛାତ୍ରଛାତ୍ରୀ ଭାବେ ଡେମୋ (Student)',
    en: 'Demo as Student'
  },
  demo_parent_title: {
    sat: 'ᱟᱭᱳ-ᱵᱟᱵᱟ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Parent)',
    ho: 'ᱮᱸᱜᱟ-ᱟᱯᱩ ᱞᱮᱠᱟᱛᱮ ᱰᱮᱢᱳ (Parent)',
    unr: 'अयंग-अपूम रूप रे डेमो (Parent)',
    kru: 'तंगियो-तम्बंग रूप नू डेमो (Parent)',
    khr: 'माय-बाप के रूप में डेमो (Parent)',
    sck: 'माय-बाप रूप में डेमो (Parent)',
    hi: 'अभिभावक के रूप में डेमो (Parent)',
    bn: 'অভিভাবক হিসেবে ডেমো (Parent)',
    or: 'ଅଭିଭାବକ ଭାବେ ଡେମୋ (Parent)',
    en: 'Demo as Parent'
  },
  demo_parent_sub: {
    sat: 'ᱥᱨᱤᱢᱚᱛᱤ ᱢᱟᱞᱛᱤ ᱫᱮᱵᱤ • ᱪᱟᱱᱟᱪ ᱓ ᱨᱤᱱ ᱟᱭᱳ • ᱥᱟᱱᱛᱟᱲᱤ/ᱢᱩᱱᱰᱟᱨᱤ',
    ho: 'ᱥᱨᱤᱢᱚᱛᱤ ᱢᱟᱞᱛᱤ ᱫᱮᱵᱤ • ᱪᱟᱱᱟᱪ ᱓ ᱮᱸᱜᱟ • ᱦᱳ/ᱢᱩᱱᱰᱟᱨᱤ',
    unr: 'श्रीमती मालती देवी • कक्षा 3 अयंग • मुंडारी/संताली',
    kru: 'श्रीमती मालती देवी • कक्षा 3 तंगियो • कुड़ुख़/सादरी',
    khr: 'श्रीमती मालती देवी • कक्षा 3 माय • खोरठा',
    sck: 'श्रीमती मालती देवी • कक्षा 3 माय • नागपुरी',
    hi: 'श्रीमती मालती देवी • कक्षा 3 अभिभावक • संताली/मुंडारी',
    bn: 'শ্রীমতী মালতী দেবী • তৃতীয় শ্রেণীর অভিভাবক • সাঁওতালি/বাংলা',
    or: 'ଶ୍ରୀମତୀ ମାଳତୀ ଦେବୀ • ତୃତୀୟ ଶ୍ରେଣୀ ଅଭିଭାବକ • ସାନ୍ତାଳୀ/ଓଡ଼ିଆ',
    en: 'Smt. Malti Devi • Class 3 Parent • Santali/Mundari'
  },

  // Dashboard Section
  dash_switch_role: {
    sat: '🔄 ᱨᱚᱞ ᱵᱚᱫᱚᱞ ᱢᱮ (ᱢᱟᱪᱮᱫ / ᱪᱮᱛᱮᱫᱤᱭᱟᱹ / ᱟᱭᱳ-ᱵᱟᱵᱟ)',
    ho: '🔄 ᱨᱚᱞ ᱵᱚᱫᱚᱞ ᱢᱮ (ᱢᱟᱪᱮᱫ / ᱤᱛᱩᱱ ᱜᱤᱫᱤᱨ / ᱮᱸᱜᱟ-ᱟᱯᱩ)',
    unr: '🔄 रोल बदलो (माचेत / होन्हार / अयंग-अपूम)',
    kru: '🔄 रोल बदलो (मास्टर / खद्दर / तंगियो-तम्बंग)',
    khr: '🔄 रोल बदलऽ (मास्टर / छौआ / माय-बाप)',
    sck: '🔄 रोल बदलू (गुरुजी / छौवा / माय-बाप)',
    hi: '🔄 भूमिका बदलें (शिक्षक / विद्यार्थी / अभिभावक)',
    bn: '🔄 ভূমিকা পরিবর্তন (শিক্ষক / শিক্ষার্থী / অভিভাবক)',
    or: '🔄 ଭୂମିକା ପରିବର୍ତ୍ତନ (ଶିକ୍ଷକ / ଛାତ୍ର / ଅଭିଭାବକ)',
    en: '🔄 Switch Mode (Teacher / Student / Parent)'
  },
  dash_change_lang: {
    sat: '🌐 ᱟᱭᱳ ᱟᱲᱟᱝ ᱵᱚᱫᱚᱞ ᱢᱮ (Change Language)',
    ho: '🌐 ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱵᱚᱫᱚᱞ ᱢᱮ (Change Language)',
    unr: '🌐 मातृभाषा बदलो (Change Language)',
    kru: '🌐 मातृभाषा बदलो (Change Language)',
    khr: '🌐 मायकोर भाषा बदलऽ (Change Language)',
    sck: '🌐 मातृभाषा बदलू (Change Language)',
    hi: '🌐 मातृभाषा बदलें (Change Mother Tongue)',
    bn: '🌐 মাতৃভাষা পরিবর্তন করুন (Change Language)',
    or: '🌐 ମାତୃଭାଷା ପରିବର୍ତ୍ତନ କରନ୍ତୁ (Change Language)',
    en: '🌐 Change Mother Tongue (Language)'
  },
  dash_quick_modules: {
    sat: '🚀 ᱢᱩᱲᱩᱫ ᱥᱮᱪᱮᱫ ᱟᱨ ᱯᱟᱲᱦᱟᱣ ᱛᱟᱞᱢᱟ (Quick Access Modules)',
    ho: '🚀 ᱢᱩᱲᱩᱫ ᱤᱛᱩᱱ ᱛᱟᱞᱢᱟ (Quick Access Modules)',
    unr: '🚀 मुख्य शिक्षण व अध्ययन केंद्र (Quick Access Modules)',
    kru: '🚀 मुख्य पढ़ाई अखाड़ा (Quick Access Modules)',
    khr: '🚀 मुख्य पढ़ाई अउर सिखई केंद्र (Quick Access Modules)',
    sck: '🚀 मुख्य शिक्षण व अध्ययन केंद्र (Quick Access Modules)',
    hi: '🚀 मुख्य शिक्षण व अध्ययन केंद्र (Quick Access Modules)',
    bn: '🚀 প্রধান শিক্ষণ ও অধ্যয়ন কেন্দ্র (Quick Access Modules)',
    or: '🚀 ମୁଖ୍ୟ ଶିକ୍ଷଣ ଓ ଅଧ୍ୟୟନ କେନ୍ଦ୍ର (Quick Access Modules)',
    en: '🚀 Quick Access Modules (Core Learning & Pedagogy)'
  },

  // Parent Specific Portal Texts
  parent_portal_title: {
    sat: '📱 ᱢᱟᱛᱨᱩ-ᱥᱟᱱᱫᱮᱥ • ᱟᱭᱳ-ᱵᱟᱵᱟ ᱟᱲᱟᱝ ᱠᱷᱚᱵᱚᱨ (Parent Vernacular Connect)',
    ho: '📱 ᱢᱟᱛᱨᱩ-ᱥᱟᱱᱫᱮᱥ • ᱮᱸᱜᱟ-ᱟᱯᱩ ᱠᱟᱡᱤ ᱠᱷᱚᱵᱚᱨ (Parent Vernacular Connect)',
    unr: '📱 मातृ-संदेश • अयंग-अपूम दैनिक आवाज संदेश (Parent Connect)',
    kru: '📱 मातृ-संदेश • तंगियो-तम्बंग कत्था संदेश (Parent Connect)',
    khr: '📱 मातृ-संदेश • माय-बाप खातिर आवाज संदेश (Parent Connect)',
    sck: '📱 मातृ-संदेश • माय-बाप खातिर आवाज संदेश (Parent Connect)',
    hi: '📱 मातृ-संदेश: अभिभावक दैनिक वाक् संदेश (Parent Vernacular Connect)',
    bn: '📱 মাতৃ-বার্তা: অভিভাবকদের জন্য দৈনিক অডিও বার্তা (Parent Connect)',
    or: '📱 ମାତୃ-ସନ୍ଦେଶ: ଅଭିଭାବକ ଦୈନିକ ଭଏସ୍ ବାର୍ତ୍ତା (Parent Connect)',
    en: '📱 Matru-Sandesh: Daily Vernacular Voice Briefing for Parents'
  },
  parent_portal_desc: {
    sat: 'ᱟᱹᱛᱩ ᱨᱤᱱ ᱟᱭᱳ-ᱵᱟᱵᱟ ᱠᱚ ᱞᱟᱹᱜᱤᱫ ᱥᱠᱩᱞ ᱨᱮᱱᱟᱜ ᱠᱷᱚᱵᱚᱨ ᱟᱯᱱᱟᱨ ᱟᱭᱳ ᱟᱲᱟᱝ ᱛᱮ ᱟᱸᱡᱚᱢ ᱢᱮ᱾ ᱜᱤᱫᱽᱨᱟᱹ ᱪᱮᱫ ᱮ ᱪᱮᱫᱚᱜ ᱠᱟᱱᱟ ᱚᱱᱟ ᱵᱟᱰᱟᱭ ᱢᱮ᱾',
    ho: 'ᱦᱟᱛᱩ ᱨᱮ ᱮᱸᱜᱟ-ᱟᱯᱩ ᱞᱟᱹᱜᱤᱱ ᱤᱛᱩᱱ ᱟᱥᱲᱟ ᱠᱟᱡᱤ ᱟᱯᱱᱟᱨ ᱠᱟᱡᱤ ᱛᱮ ᱟᱸᱡᱚᱢ ᱢᱮ᱾',
    unr: 'गाँव के अयंग-अपूम लागिन स्कूल के दैनिक समाचार आपन अयंग काजी में सुनू आर होन्हार के पढ़ाव में मदद करू।',
    kru: 'गाँव नू तंगियो-तम्बंग ले स्कूल गही दैनिक कत्था आपन मातृभाषा नू मेना अरा खद्दर गही मदद करा।',
    khr: 'गाँव के माय-बाप खातिर स्कूल के दैनिक समाचार आपन मायकोर भाषा में सुना अउर छौआ के पढ़ाई में मदद करा।',
    sck: 'गाँव कर माय-बाप खातिर स्कूल कर दैनिक संदेश आपन माय-कर बोली में सुनू अउर छौवा के आगे बढ़ाबू।',
    hi: 'गाँव के अभिभावक अपने बच्चे की दैनिक स्कूल प्रगति व गृहकार्य 30-सेकंड की मातृभाषा ऑडियो में सुनें और बच्चे का मार्गदर्शन करें।',
    bn: 'গ্রামের অভিভাবকরা নিজেদের মাতৃভাষায় দৈনিক স্কুলের পড়া ও অডিও শুনুন এবং সন্তানের পাশে থাকুন।',
    or: 'ଗ୍ରାମାଞ୍ଚଳ ଅଭିଭାବକମାନେ ନିଜ ମାତୃଭାଷାରେ ଦୈନିକ ଶିକ୍ଷା ବାର୍ତ୍ତା ଶୁଣନ୍ତୁ ଏବଂ ପିଲାଙ୍କୁ ଉତ୍ସାହିତ କରନ୍ତୁ।',
    en: 'Listen to 30-second daily school briefings in your native mother tongue so parents can guide their child with pride.'
  },
  parent_listen_audio_btn: {
    sat: '🔊 ᱛᱮᱦᱮᱧᱟᱜ ᱟᱭᱳ ᱟᱲᱟᱝ ᱥᱟᱱᱫᱮᱥ ᱟᱸᱡᱚᱢ ᱢᱮ (Play Briefing)',
    ho: '🔊 ᱛᱤᱥᱤᱝ ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱥᱟᱱᱫᱮᱥ ᱟᱸᱡᱚᱢ ᱢᱮ (Play Briefing)',
    unr: '🔊 तिशिंग आ अयंग काजी संदेश सुनू (Play Briefing)',
    kru: '🔊 इन्ना गही मातृभाषा संदेश मेना (Play Briefing)',
    khr: '🔊 आज के मायकोर भाषा संदेश सुना (Play Briefing)',
    sck: '🔊 आज कर मातृभाषा संदेश सुनू (Play Briefing)',
    hi: '🔊 आज का 30-सेकंड मातृभाषा संदेश सुनें (Play Daily Voice Note)',
    bn: '🔊 আজকের ৩০-সেকেন্ড মাতৃভাষা অডিও শুনুন (Play Daily Voice)',
    or: '🔊 ଆଜିର ୩୦-ସେକେଣ୍ଡ ମାତୃଭାଷା ବାର୍ତ୍ତା ଶୁଣନ୍ତୁ (Play Voice Note)',
    en: '🔊 Play Today\'s Vernacular Briefing (30-Sec Audio)'
  },
  parent_ask_teacher_btn: {
    sat: '🎙️ ᱢᱟᱪᱮᱫ ᱴᱷᱮᱱ ᱟᱭᱳ ᱟᱲᱟᱝ ᱛᱮ ᱠᱩᱞᱤ ᱢᱮ (Voice Message)',
    ho: '🎙️ ᱢᱟᱪᱮᱫ ᱴᱷᱮᱱ ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱛᱮ ᱠᱩᱞᱤ ᱢᱮ (Voice Message)',
    unr: '🎙️ माचेत के अयंग काजी में सवाल पूछू (Voice Message)',
    kru: '🎙️ मास्टर संगे मातृभाषा नू कत्था मेना (Voice Message)',
    khr: '🎙️ मास्टर जी से आपन भाषा में सवाल पूछा (Voice Message)',
    sck: '🎙️ गुरुजी से आपन बोली में सवाल पूछू (Voice Message)',
    hi: '🎙️ शिक्षक को अपनी मातृभाषा में संदेश भेजें (Voice Question)',
    bn: '🎙️ শিক্ষককে নিজের মাতৃভাষায় বার্তা পাঠান (Voice Question)',
    or: '🎙️ ଶିକ୍ଷକଙ୍କୁ ନିଜ ମାତୃଭାଷାରେ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ (Voice Question)',
    en: '🎙️ Record Voice Question for Teacher in Mother Tongue'
  },
  parent_stars_title: {
    sat: '⭐ ᱟᱢᱟᱜ ᱜᱤᱫᱽᱨᱟᱹ ᱟᱜ ᱥᱮᱪᱮᱫ ᱥᱤᱛᱟᱹᱨᱟ (Child Reading Stars):',
    ho: '⭐ ᱟᱢᱟᱜ ᱜᱤᱫᱤᱨ ᱤᱛᱩᱱ ᱤᱯᱤᱞ (Child Reading Stars):',
    unr: '⭐ आमाः होन्हार के पढ़ाई सितारे (Reading Stars):',
    kru: '⭐ निग्है खद्दर गही पढ़ाई सितारे (Reading Stars):',
    khr: '⭐ तोहर छौआ के पढ़ाई सितारे (Reading Stars):',
    sck: '⭐ रउरे छौवा कर पढ़ाई सितारे (Reading Stars):',
    hi: '⭐ आपके बच्चे के अध्ययन सितारे (Child FLN Reading Stars):',
    bn: '⭐ আপনার সন্তানের পড়াশোনার তারা (Child Reading Stars):',
    or: '⭐ ଆପଣଙ୍କ ପିଲାର ଅଧ୍ୟୟନ ତାରକା (Child Reading Stars):',
    en: '⭐ Your Child\'s Learning Progress (FLN Stars & Mastery):'
  },

  // Floating Language Trigger
  floating_trigger_title: {
    sat: 'ᱟᱭᱳ ᱟᱲᱟᱝ',
    ho: 'ᱮᱸᱜᱟ ᱠᱟᱡᱤ',
    unr: 'अयंग काजी',
    kru: 'मातृभाषा',
    khr: 'मायकोर भाषा',
    sck: 'माय-कर बोली',
    hi: 'मातृभाषा',
    bn: 'মাতৃভাষা',
    or: 'ମାତୃଭାଷା',
    en: 'Mother Tongue'
  },
  modal_lang_title: {
    sat: '🌐 ᱟᱢᱟᱜ ᱟᱭᱳ ᱟᱲᱟᱝ ᱵᱟᱪᱷᱟᱣ ᱢᱮ • CHOOSE YOUR MOTHER TONGUE',
    ho: '🌐 ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱵᱟᱪᱷᱟᱣ ᱢᱮ • CHOOSE YOUR MOTHER TONGUE',
    unr: '🌐 अयंग काजी बाछाव में • CHOOSE YOUR MOTHER TONGUE',
    kru: '🌐 मातृभाषा चुनरा • CHOOSE YOUR MOTHER TONGUE',
    khr: '🌐 आपन मायकोर भाषा चुना • CHOOSE YOUR MOTHER TONGUE',
    sck: '🌐 आपन मातृभाषा चुनू • CHOOSE YOUR MOTHER TONGUE',
    hi: '🌐 अपनी मातृभाषा चुनें • CHOOSE YOUR MOTHER TONGUE',
    bn: '🌐 আপনার মাতৃভাষা নির্বাচন করুন • CHOOSE MOTHER TONGUE',
    or: '🌐 ନିଜ ମାତୃଭାଷା ଚୟନ କରନ୍ତୁ • CHOOSE MOTHER TONGUE',
    en: '🌐 CHOOSE YOUR MOTHER TONGUE • अपनी मातृभाषा चुनें'
  },
  modal_lang_subtitle: {
    sat: 'ᱱᱚᱶᱟ ᱮᱯ ᱫᱚ ᱢᱟᱪᱮᱫ, ᱪᱮᱛᱮᱫᱤᱭᱟᱹ ᱟᱨ ᱟᱭᱳ-ᱵᱟᱵᱟ ᱡᱚᱛᱚ ᱦᱚᱲ ᱞᱟᱹᱜᱤᱫ ᱯᱩᱨᱟᱹ ᱟᱭᱳ ᱟᱲᱟᱝ ᱛᱮ ᱠᱟᱹᱢᱤᱭᱟ᱾ ᱡᱟᱦᱟᱸ ᱚᱠᱛᱚ ᱨᱮᱦᱚᱸ ᱵᱚᱫᱚᱞ ᱫᱟᱲᱮᱭᱟᱜᱼᱟ᱾',
    ho: 'ᱱᱮᱱ ᱮᱯ ᱫᱚ ᱢᱟᱪᱮᱫ, ᱤᱛᱩᱱ ᱜᱤᱫᱤᱨ ᱟᱨ ᱮᱸᱜᱟ-ᱟᱯᱩ ᱡᱚᱛᱚ ᱦᱚᱲ ᱞᱟᱹᱜᱤᱱ ᱮᱸᱜᱟ ᱠᱟᱡᱤ ᱛᱮ ᱪᱟᱞᱟᱣᱚᱜᱼᱟ᱾',
    unr: 'नेन ऐप माचेत, होन्हार आर अयंग-अपूम सबे लागिन पूरा अयंग काजी में चली। जेतेखन बदलो सकूआ।',
    kru: 'ई ऐप मास्टर, खद्दर अरा तंगियो-तम्बंग सबे ले मातृभाषा नू कामी करबो।',
    khr: 'ई ऐप मास्टर, छौआ अउर माय-बाप सबे खातिर पूरा आपन मायकोर भाषा में काम करतउ।',
    sck: 'ई ऐप गुरुजी, छौवा अउर माय-बाप सबे खातिर पूरा मातृभाषा में काम करी। कभी भी बदलू।',
    hi: 'यह ऐप शिक्षक, विद्यार्थी और अभिभावक सभी के लिए पूर्णतः आपकी मातृभाषा में संचालित होता है। आप इसे किसी भी समय बदल सकते हैं।',
    bn: 'এই অ্যাপটি শিক্ষক, শিক্ষার্থী এবং অভিভাবকদের জন্য সম্পূর্ণ মাতৃভাষায় পরিচালিত হয়। যেকোনো সময় পরিবর্তনযোগ্য।',
    or: 'ଏହି ଆପ୍ ଶିକ୍ଷକ, ଛାତ୍ରଛାତ୍ରୀ ଏବଂ ଅଭିଭାବକ ସମସ୍ତଙ୍କ ପାଇଁ ସମ୍ପୂର୍ଣ୍ଣ ମାତୃଭାଷାରେ ଚାଲିବ। ଯେକୌଣସି ସମୟରେ ବଦଳାଇ ପାରିବେ।',
    en: 'This application fully adapts to your mother tongue for Teachers, Students, and Parents at any phase.'
  }
};

class I18nManager {
  constructor() {
    this.currentLang = this.getSavedLang();
    this.languages = MOTHER_TONGUES;
  }

  getSavedLang() {
    try {
      const saved = localStorage.getItem('matrubhasa_mother_tongue') || localStorage.getItem('matrubhasa_ui_lang');
      if (saved && MOTHER_TONGUES[saved]) return saved;
    } catch (e) { }
    return 'sat'; // Default to Santali (8th Schedule tribal mother tongue of Jharkhand)
  }

  setLanguage(langCode, announceVoice = true) {
    if (!MOTHER_TONGUES[langCode]) return;
    this.currentLang = langCode;
    try {
      localStorage.setItem('matrubhasa_mother_tongue', langCode);
      localStorage.setItem('matrubhasa_ui_lang', langCode);
    } catch (e) { }

    // Synchronize global application state if available
    if (typeof state !== 'undefined') {
      state.currentLang = langCode;
    }

    this.applyAllTranslations();
    this.updateLanguagePickersUI();
    this.syncToolDropdowns(langCode);

    // Announce with voice feedback for illiterate parents and tribal learners
    if (announceVoice && typeof playVernacularSpeech === 'function') {
      const meta = MOTHER_TONGUES[langCode];
      if (meta && meta.audioGreeting) {
        playVernacularSpeech(meta.audioGreeting, langCode);
      }
    }
  }

  t(key, lang = null) {
    const l = lang || this.currentLang;
    if (UI_TRANSLATIONS[key]) {
      return UI_TRANSLATIONS[key][l] || UI_TRANSLATIONS[key]['hi'] || UI_TRANSLATIONS[key]['en'] || '';
    }
    return '';
  }

  applyAllTranslations() {
    const lang = this.currentLang;

    // Elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key, lang);
      if (translation) {
        // If element has icon children, preserve first span if needed or replace text
        if (el.dataset.i18nPreserveIcon) {
          const icon = el.querySelector('.tab-icon, .role-icon, .demo-icon, .btn-arrow');
          if (icon) {
            el.innerHTML = '';
            el.appendChild(icon);
            el.append(' ' + translation);
          } else {
            el.textContent = translation;
          }
        } else {
          el.innerHTML = translation;
        }
      }
    });

    // Elements with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const translation = this.t(key, lang);
      if (translation) el.setAttribute('placeholder', translation);
    });

    // Elements with data-i18n-title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      const translation = this.t(key, lang);
      if (translation) el.setAttribute('title', translation);
    });

    // Update document HTML lang attribute
    document.documentElement.lang = lang;

    // Dispatch custom event for dynamic components
    window.dispatchEvent(new CustomEvent('matrubhasa:languageChanged', { detail: { lang } }));
  }

  updateLanguagePickersUI() {
    const meta = MOTHER_TONGUES[this.currentLang];
    if (!meta) return;

    // Top gov ribbon badge
    const govBadge = document.getElementById('govCurrentLangTag');
    if (govBadge) {
      govBadge.textContent = `${meta.name_native} (${meta.name_en})`;
    }

    // Floating pill label
    const floatingName = document.getElementById('floatingCurrentLangName');
    if (floatingName) {
      floatingName.textContent = `${meta.name_native} (${meta.name_en})`;
    }

    // Auth screen chips
    document.querySelectorAll('.auth-lang-chip').forEach(chip => {
      if (chip.getAttribute('data-lang') === this.currentLang) {
        chip.classList.add('active');
      } else {
        chip.classList.remove('active');
      }
    });

    // Modal cards active state
    document.querySelectorAll('.lang-choice-card').forEach(card => {
      if (card.getAttribute('data-lang') === this.currentLang) {
        card.classList.add('selected');
        const badge = card.querySelector('.lang-active-indicator');
        if (badge) badge.style.display = 'inline-flex';
      } else {
        card.classList.remove('selected');
        const badge = card.querySelector('.lang-active-indicator');
        if (badge) badge.style.display = 'none';
      }
    });
  }

  syncToolDropdowns(langCode) {
    const dropdownIds = [
      'liveTargetLang',
      'storyTargetLang',
      'flnLangSelect',
      'parentLangSelect',
      'readerLangSelect'
    ];

    dropdownIds.forEach(id => {
      const sel = document.getElementById(id);
      if (sel) {
        // Check if langCode exists in options
        const optionExists = Array.from(sel.options).some(opt => opt.value === langCode);
        if (optionExists) {
          sel.value = langCode;
          // Trigger change event to reload sentences/books if needed
          sel.dispatchEvent(new Event('change'));
        }
      }
    });

    // Update live output badge if present
    const outputBadge = document.getElementById('outputLangBadge');
    if (outputBadge && MOTHER_TONGUES[langCode]) {
      outputBadge.textContent = `${MOTHER_TONGUES[langCode].name_native} (${MOTHER_TONGUES[langCode].name_en})`;
    }
  }
}

// Global I18N Instance
const I18N = new I18nManager();
window.I18N = I18N;
window.MOTHER_TONGUES = MOTHER_TONGUES;
