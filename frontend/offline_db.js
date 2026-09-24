// Offline IndexedDB & Edge Storage for Matrubhasa AI
const DB_NAME = 'MatrubhasaOfflineDB';
const DB_VERSION = 2;

class MatrubhasaStorage {
  constructor() {
    this.db = null;
    this.initPromise = this.init();
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('lesson_packs')) {
          db.createObjectStore('lesson_packs', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('student_scores')) {
          db.createObjectStore('student_scores', { keyPath: 'id', autoIncrement: true });
        }
        if (!db.objectStoreNames.contains('offline_stories')) {
          db.createObjectStore('offline_stories', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('ncert_notebooks')) {
          db.createObjectStore('ncert_notebooks', { keyPath: 'id' });
        }
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        this.seedInitialLessons();
        this.seedInitialNotebooks();
        resolve(this.db);
      };

      request.onerror = (event) => {
        console.error('IndexedDB init error:', event.target.error);
        resolve(null); // graceful fallback to localStorage
      };
    });
  }

  async seedInitialLessons() {
    const defaultLessons = [
      {
        id: 'lesson_plants_gr2',
        title_en: 'How Plants Grow (Grade 2)',
        title_hi: 'पौधे कैसे बढ़ते हैं (कक्षा 2)',
        category: 'Science',
        english: 'Plants need sunlight and water to make food.',
        hindi: 'पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।',
        santali: 'ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾',
        ho: 'ᱫᱟᱨᱩ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾',
        bengali: 'গাছের খাদ্য তৈরির জন্য সূর্যের আলো এবং জলের প্রয়োজন।',
        odia: 'ଗଛକୁ ଖାଦ୍ୟ ତିଆରି କରିବା ପାଇଁ ସୂର୍ଯ୍ୟାଲୋକ ଓ ପାଣି ଦରକାର।',
        keywords: ['Suraj (धूप)', 'Paani (जल)', 'Dare (গাছ/पेड़)']
      },
      {
        id: 'lesson_rain_gr1',
        title_en: 'The Rainy Day (Grade 1)',
        title_hi: 'बारिश का दिन (कक्षा 1)',
        category: 'Nature',
        english: 'Dark clouds bring cool rain to the green fields.',
        hindi: 'काले बादल हरे-भरे खेतों में ठंडी बारिश लाते हैं।',
        santali: 'ᱦᱮᱸᱫᱮ ᱨᱤᱢᱤᱞ ᱦᱟᱹᱨᱭᱟᱹᱲ ᱠᱷᱮᱛ ᱛᱮ ᱨᱮᱭᱟᱲ ᱫᱟᱜ ᱡᱟᱹᱲᱤ ᱟᱹᱜᱩᱭᱟ᱾',
        ho: 'ᱦᱮᱸᱫᱮ ᱨᱤᱢᱤᱞ ᱦᱟᱹᱨᱭᱟᱹᱲ ᱵᱟᱹᱫᱽ ᱨᱮ ᱨᱮᱭᱟᱲ ᱡᱟᱹᱲᱤ ᱟᱹᱜᱩᱭᱟ᱾',
        bengali: 'কালো মেঘ সবুজ মাঠে ঠান্ডা বৃষ্টি নিয়ে আসে।',
        odia: 'କଳା ବାଦଲ ସବୁଜ କ୍ଷେତକୁ ଥଣ୍ଡା ବର୍ଷା ଆଣିଥାଏ।',
        keywords: ['Baadal (মেঘ)', 'Baarish (বৃষ্টি/ᱫᱟᱜ)', 'Khet (ᱠᱷᱮᱛ)']
      },
      {
        id: 'lesson_friendship_gr3',
        title_en: 'Helping Our Friends (Grade 3)',
        title_hi: 'दोस्तों की मदद (कक्षा 3)',
        category: 'Moral / Social',
        english: 'Good friends share their books and play happily together.',
        hindi: 'सच्चे दोस्त अपनी किताबें बांटते हैं और मिलकर खुश रहते हैं।',
        santali: 'ᱥᱟᱹᱨᱤ ᱜᱟᱛᱮ ᱟᱠᱚᱣᱟᱜ ᱯᱩᱛᱷᱤ ᱠᱚ ᱦᱟᱹᱴᱤᱧᱟ ᱟᱨ ᱢᱤᱫ ᱛᱮ ᱨᱟᱹᱥᱠᱟᱹ ᱛᱮ ᱠᱚ ᱮᱱᱮᱡᱼᱟ᱾',
        ho: 'ᱥᱟᱹᱨᱤ ᱡᱩᱲᱤ ᱟᱠᱚᱣᱟᱜ ᱯᱩᱛᱷᱤ ᱠᱚ ᱦᱟᱹᱴᱤᱧᱟ ᱟᱨ ᱢᱤᱫ ᱛᱮ ᱨᱟᱹᱥᱠᱟᱹ ᱛᱮ ᱠᱚ ᱤᱱᱩᱝᱼᱟ᱾',
        bengali: 'ভালো বন্ধুরা তাদের বই ভাগ করে এবং একসঙ্গে খুশি থাকে।',
        odia: 'ଭଲ ସାଙ୍ଗମାନେ ସେମାନଙ୍କ ବହି ବାଣ୍ଟନ୍ତି ଏବଂ ଏକାଠି ଖୁସି ରୁହନ୍ତି।',
        keywords: ['Gate (Dost/সখা)', 'Puthi (Kitaab)', 'Ened (Khel/খেলা)']
      }
    ];

    for (const l of defaultLessons) {
      await this.saveLesson(l);
    }
  }

  async saveLesson(lesson) {
    if (!this.db) return;
    return new Promise((resolve) => {
      const tx = this.db.transaction('lesson_packs', 'readwrite');
      const store = tx.objectStore('lesson_packs');
      store.put(lesson);
      tx.oncomplete = () => resolve(true);
    });
  }

  async getLessons() {
    if (!this.db) return [];
    return new Promise((resolve) => {
      const tx = this.db.transaction('lesson_packs', 'readonly');
      const store = tx.objectStore('lesson_packs');
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve([]);
    });
  }

  async recordStudentScore(data) {
    const entry = {
      timestamp: new Date().toISOString(),
      studentName: data.studentName || 'Chhatra',
      lessonId: data.lessonId,
      accuracyPct: data.accuracyPct,
      stars: data.stars,
      lang: data.lang,
      synced: navigator.onLine
    };

    if (this.db) {
      const tx = this.db.transaction('student_scores', 'readwrite');
      tx.objectStore('student_scores').add(entry);
    }

    // Save in local list
    const scores = JSON.parse(localStorage.getItem('fln_scores') || '[]');
    scores.unshift(entry);
    localStorage.setItem('fln_scores', JSON.stringify(scores.slice(0, 50)));
    return entry;
  }

  getRecentScores() {
    return JSON.parse(localStorage.getItem('fln_scores') || '[]');
  }

  // =========================================================================
  // JCERT / NCERT OFFLINE NOTEBOOKS & CHAPTERS STORE
  // =========================================================================
  async seedInitialNotebooks() {
    // Seed initial Class 1 and Class 2 chapters so village students have instant offline reading
    const sampleChapters = [
      {
        id: 'cl1_evs_ch1',
        grade: 1,
        grade_label: 'कक्षा 1 (Class 1)',
        subject: 'evs',
        subject_name: 'पर्यावरण एवं परिवेश (EVS)',
        subject_icon: '🌿',
        chapter_no: 1,
        title_hi: 'हमारा प्यारा परिवार और घर',
        title_en: 'Our Loving Family and Home',
        concept_summary: 'परिवार में माता-पिता, दादा-दादी और भाई-बहन मिलकर प्यार से रहते हैं और एक-दूसरे की मदद करते हैं।',
        downloadedAt: new Date().toISOString(),
        isDownloaded: true,
        paragraphs: [
          {
            id: 'p1',
            en: 'Our home is where our family lives together with love and care.',
            hi: 'हमारा घर वह प्यारी जगह है जहाँ हमारा परिवार मिलकर प्यार और स्नेह से रहता है।',
            sat: 'ᱟᱵᱚᱣᱟᱜ ᱚᱲᱟᱜ ᱫᱚ ᱚᱱᱟ ᱡᱟᱭᱜᱟ ᱠᱟᱱᱟ ᱡᱟᱦᱟᱸ ᱨᱮ ᱟᱵᱚ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱢᱤᱫ ᱛᱮ ᱫᱩᱞᱟᱹᱲ ᱛᱮ ᱵᱚᱱ ᱛᱟᱦᱮᱸᱱᱟ᱾',
            ho: 'ᱟᱵᱩᱣᱟᱜ ᱚᱲᱟᱜ ᱫᱚ ᱱᱮᱱ ᱡᱟᱭᱜᱟ ᱠᱟᱱᱟ ᱡᱟᱦᱟᱸ ᱨᱮ ᱟᱵᱩ ᱦᱟᱛᱩ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱫᱩᱞᱟᱹᱲ ᱛᱮ ᱵᱚᱱ ᱛᱟᱦᱮᱸᱱᱟ᱾',
            khr: 'हमर घर उहे सुंदर जगह हे जहाँ हमर पूरा परिवार मिल-जुल के प्यार से रहे हे।',
            sck: 'हमर घर उहे बेस जगह हे जहाँ हमर परिवार संगे मया-दुलार से रहेला।'
          },
          {
            id: 'p2',
            en: 'Grandmother tells us sweet folk stories at night, and grandfather takes us to the village field.',
            hi: 'दादी माँ रात को हमें मीठी लोक-कहानियाँ सुनाती हैं, और दादा जी हमें गाँव के खेतों में घुमाने ले जाते हैं।',
            sat: 'ᱟᱹᱭᱩᱵ ᱵᱮᱲᱟ ᱵᱩᱰᱷᱤ ᱟᱭᱳ ᱥᱤᱵᱤᱞ ᱠᱟᱹᱦᱱᱤ ᱞᱟᱹᱭ ᱟᱵᱚᱱᱟ, ᱟᱨ ᱦᱟᱲᱟᱢ ᱵᱟᱵᱟ ᱟᱹᱛᱩ ᱠᱷᱮᱛ ᱥᱮᱫ ᱫᱟᱬᱟᱸᱭ ᱤᱫᱤ ᱵᱚᱱᱟ᱾',
            ho: 'ᱟᱹᱭᱩᱵ ᱵᱩᱰᱷᱤ ᱟᱭᱳ ᱥᱤᱵᱤᱞ ᱠᱟᱹᱦᱱᱤ ᱠᱟᱡᱤᱭᱟ, ᱟᱨ ᱦᱟᱲᱟᱢ ᱵᱟᱵᱟ ᱦᱟᱛᱩ ᱵᱟᱹᱫᱽ ᱛᱮ ᱫᱟᱬᱟᱸᱭ ᱤᱫᱤ ᱵᱚᱱᱟ᱾',
            khr: 'दादी रात के हमनी के मीठ-मीठ कहानी सुनावऽ हथिन, अउर दादा जी खेत घुमावे ले जा हथिन।',
            sck: 'आजी रात के हमके बेस-बेस कहानी सुनावेला, अउर आजा गाँव के खेत-खरिहान घुमावेला।'
          }
        ],
        keywords: [
          { concept: 'family', en: 'Family', hi: 'परिवार (Parivar)', sat: 'ᱜᱷᱟᱨᱚᱸᱡᱽ (Gharonj)', meaning: 'माता-पिता, दादा-दादी और बच्चे' },
          { concept: 'home', en: 'Home', hi: 'घर (Ghar)', sat: 'ᱚᱲᱟᱜ (Orak)', meaning: 'सुरक्षित और प्यारा बसेरा' }
        ],
        abhyas_questions: [
          { q: 'आपके घर में कौन-कौन रहते हैं?', hint: 'माता, पिता, भाई, बहन, दादा, दादी' },
          { q: 'रात को आपको कौन कहानी सुनाता है?', hint: 'दादी माँ या नानी माँ' }
        ]
      },
      {
        id: 'cl1_evs_ch2',
        grade: 1,
        grade_label: 'कक्षा 1 (Class 1)',
        subject: 'evs',
        subject_name: 'पर्यावरण एवं परिवेश (EVS)',
        subject_icon: '🌿',
        chapter_no: 2,
        title_hi: 'पेड़-पौधे और फल-फूल',
        title_en: 'Plants, Trees and Flowers',
        concept_summary: 'हरे पेड़ हमारे सच्चे मित्र हैं। वे हमें मीठे फल, सुंदर फूल, छाया और ताजी हवा देते हैं।',
        downloadedAt: new Date().toISOString(),
        isDownloaded: true,
        paragraphs: [
          {
            id: 'p1',
            en: 'Green trees are our best friends. They give us sweet mangoes, shade, and clean air.',
            hi: 'हरे-भरे पेड़ हमारे सबसे सच्चे दोस्त हैं। वे हमें मीठे आम, ठंडी छाया और ताजी हवा देते हैं।',
            sat: 'ᱦᱟᱹᱨᱭᱟᱹᱲ ᱫᱟᱨᱮ ᱠᱚ ᱫᱚ ᱟᱵᱚᱣᱟᱜ ᱥᱟᱹᱨᱤ ᱜᱟᱛᱮ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱩᱱᱠᱩ ᱟᱵᱚ ᱥᱤᱵᱤᱞ ᱩᱞ, ᱩᱢᱩᱞ ᱟᱨ ᱥᱟᱯᱷᱟ ᱦᱚᱭ ᱠᱚ ᱮᱢᱟᱵᱚᱱᱟ᱾',
            ho: 'ᱦᱟᱹᱨᱭᱟᱹᱲ ᱫᱟᱨᱩ ᱠᱚ ᱟᱵᱩᱣᱟᱜ ᱥᱟᱹᱨᱤ ᱡᱩᱲᱤ ᱠᱟᱱᱟ ᱠᱚ᱾ ᱱᱤᱠᱩ ᱥᱤᱵᱤᱞ ᱩᱞ ᱟᱨ ᱥᱟᱯᱷᱟ ᱦᱚᱭ ᱮᱢᱟᱵᱩᱣᱟ᱾',
            khr: 'हरियर-हरियर गाछ हमर सबले बेस संगी हे। उ हमनी के मीठ आम, छाया अउर शुद्ध हवा देवे हे।',
            sck: 'हरियर गाछ-बिरिछ हमर सच्चा संगी हेकें। ऊ मन हमके मीठा आंबा, छांह अउर साफ हवा देवेला।'
          }
        ],
        keywords: [
          { concept: 'tree', en: 'Tree', hi: 'पेड़ (Ped)', sat: 'ᱫᱟᱨᱮ (Dare)', meaning: 'फल और छाया देने वाला पौधा' },
          { concept: 'flower', en: 'Flower', hi: 'फूल (Phool)', sat: 'ᱵᱟᱦᱟ (Baha)', meaning: 'सुंदर खुशबूदार पुष्प' }
        ],
        abhyas_questions: [
          { q: 'पेड़ हमें क्या-क्या देते हैं?', hint: 'फल, फूल, लकड़ी, छाया और ताजी हवा' }
        ]
      }
    ];

    for (const ch of sampleChapters) {
      await this.saveChapter(ch);
    }
  }

  async saveChapter(chapter) {
    if (!this.db) {
      const local = JSON.parse(localStorage.getItem('ncert_offline_chapters') || '{}');
      local[chapter.id] = { ...chapter, isDownloaded: true, downloadedAt: new Date().toISOString() };
      localStorage.setItem('ncert_offline_chapters', JSON.stringify(local));
      return true;
    }
    return new Promise((resolve) => {
      const tx = this.db.transaction('ncert_notebooks', 'readwrite');
      const store = tx.objectStore('ncert_notebooks');
      chapter.isDownloaded = true;
      chapter.downloadedAt = new Date().toISOString();
      store.put(chapter);
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => resolve(false);
    });
  }

  async getChapter(chapterId) {
    if (!this.db) {
      const local = JSON.parse(localStorage.getItem('ncert_offline_chapters') || '{}');
      return local[chapterId] || null;
    }
    return new Promise((resolve) => {
      const tx = this.db.transaction('ncert_notebooks', 'readonly');
      const store = tx.objectStore('ncert_notebooks');
      const req = store.get(chapterId);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    });
  }

  async getAllDownloadedChapters(grade = null) {
    if (!this.db) {
      const local = JSON.parse(localStorage.getItem('ncert_offline_chapters') || '{}');
      const all = Object.values(local);
      if (grade) return all.filter((c) => c.grade === Number(grade));
      return all;
    }
    return new Promise((resolve) => {
      const tx = this.db.transaction('ncert_notebooks', 'readonly');
      const store = tx.objectStore('ncert_notebooks');
      const req = store.getAll();
      req.onsuccess = () => {
        const res = req.result || [];
        if (grade) {
          resolve(res.filter((c) => c.grade === Number(grade)));
        } else {
          resolve(res);
        }
      };
      req.onerror = () => resolve([]);
    });
  }

  async deleteDownloadedChapter(chapterId) {
    if (!this.db) {
      const local = JSON.parse(localStorage.getItem('ncert_offline_chapters') || '{}');
      delete local[chapterId];
      localStorage.setItem('ncert_offline_chapters', JSON.stringify(local));
      return true;
    }
    return new Promise((resolve) => {
      const tx = this.db.transaction('ncert_notebooks', 'readwrite');
      const store = tx.objectStore('ncert_notebooks');
      store.delete(chapterId);
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => resolve(false);
    });
  }

  async isChapterOffline(chapterId) {
    const ch = await this.getChapter(chapterId);
    return Boolean(ch);
  }

  async saveGradeBundle(grade, chapters) {
    for (const ch of chapters) {
      await this.saveChapter(ch);
    }
    return true;
  }
}

// =========================================================================
// OFFLINE TRIBAL GLOSSARY & PHRASEBANK (PRD Section 4 / FR-6 Gaon Mode)
// =========================================================================
window.OFFLINE_TRIBAL_VOCABULARY = [
  { concept: 'sun', en: 'Sun', hi: 'सूरज', sat: 'ᱥᱤᱧ ᱪᱟᱸᱫᱚ', ho: 'ᱥᱤᱝᱜᱤ', unr: 'सिंगी', kru: 'बिड़ी', khr: 'रोइद', sck: 'सूरज', bn: 'সূর্য', or: 'ସୂର୍ଯ୍ୟ', meaning: 'दैनिक धूप व ऊर्जा' },
  { concept: 'water', en: 'Water', hi: 'पानी', sat: 'ᱫᱟᱜ', ho: 'ᱫᱟᱜ', unr: 'दाः', kru: 'अम्म', khr: 'पानी', sck: 'पानी', bn: 'জল', or: 'ପାଣି', meaning: 'जीवनदायिनी जल' },
  { concept: 'tree', en: 'Tree', hi: 'पेड़', sat: 'ᱫᱟᱨᱮ', ho: 'ᱫᱟᱨᱩ', unr: 'दारू', kru: 'मन्न', khr: 'गाछ', sck: 'गाछ', bn: 'গাছ', or: 'ଗଛ', meaning: 'फल व छाया देने वाला' },
  { concept: 'rain', en: 'Rain', hi: 'बारिश', sat: 'ᱫᱟᱜ ᱡᱟᱹᱲᱤ', ho: 'ᱡᱟᱹᱲᱤ', unr: 'जाड़ी', kru: 'झड़ी', khr: 'बरखा', sck: 'बरखा', bn: 'বৃষ্টি', or: 'ବର୍ଷା', meaning: 'आसमान से गिरती बूंदें' },
  { concept: 'book', en: 'Book', hi: 'किताब', sat: 'ᱯᱩᱛᱷᱤ', ho: 'ᱯᱩᱛᱷᱤ', unr: 'पुथी', kru: 'पुथी', khr: 'किताब', sck: 'पोथी', bn: 'বই', or: 'ବହି', meaning: 'ज्ञान व कहानी की पोथी' },
  { concept: 'school', en: 'School', hi: 'विद्यालय / स्कूल', sat: 'ᱟᱥᱲᱟ', ho: 'ᱤᱛᱩᱱ ᱟᱥᱲᱟ', unr: 'इतुन आषड़ा', kru: 'पढ़ना अखाड़ा', khr: 'पाठशाला', sck: 'स्कूल', bn: 'বিদ্যালয়', or: 'ବିଦ୍ୟାଳୟ', meaning: 'सीखने की पाठशाला' },
  { concept: 'teacher', en: 'Teacher', hi: 'शिक्षक / गुरुजी', sat: 'ᱢᱟᱪᱮᱫ', ho: 'ᱢᱟᱪᱮᱫ', unr: 'माचेत', kru: 'गुरु', khr: 'मास्टर जी', sck: 'गुरुजी', bn: 'শিক্ষক', or: 'ଶିକ୍ଷକ', meaning: 'ज्ञान सिखाने वाले गुरु' },
  { concept: 'friend', en: 'Friend', hi: 'दोस्त', sat: 'ᱜᱟᱛᱮ', ho: 'ᱡᱩᱲᱤ', unr: 'जोड़ी', kru: 'संगिया', khr: 'संगी', sck: 'संगी', bn: 'বন্ধু', or: 'ସାଙ୍ଗ', meaning: 'साथी जिसके साथ खेलते हैं' },
  { concept: 'greetings', en: 'Hello / Greetings', hi: 'नमस्ते / जोहार', sat: 'ᱡᱚᱦᱟᱨ', ho: 'ᱡᱚᱦᱟᱨ', unr: 'जोहार', kru: 'जय जोहार', khr: 'प्रणाम', sck: 'जोहार', bn: 'নমস্কার', or: 'ନମସ୍କାର', meaning: 'आदरपूर्वक अभिवादन' },
  { concept: 'elephant', en: 'Elephant', hi: 'हाथी (गज्जू)', sat: 'ᱦᱟᱹᱛᱤ', ho: 'ᱦᱟᱹᱛᱤ', unr: 'हाथी', kru: 'हाथी', khr: 'हाथी', sck: 'हाथी', bn: 'হাতি', or: 'ହାତୀ', meaning: 'प्यारा दोस्त गज्जू भाई' },
  { concept: 'tiger', en: 'Tiger', hi: 'बाघ', sat: 'ᱠᱩᱞ', ho: 'ᱠᱩᱞ', unr: 'कुल / बाघ', kru: 'लकरा', khr: 'बाघ', sck: 'बाघ', bn: 'বাঘ', or: 'ବାଘ', meaning: 'जंगल का राजा' },
  { concept: 'bird', en: 'Bird', hi: 'चिड़िया', sat: 'ᱪᱮᱬᱮ', ho: 'ᱪᱮᱬᱮ', unr: 'चेणे', kru: 'उजगो', khr: 'चिरई', sck: 'चिरई', bn: 'পাখি', or: 'ଚଢ଼େଇ', meaning: 'पंखों से उड़ने वाली' },
  { concept: 'earth', en: 'Earth', hi: 'धरती', sat: 'ᱫᱷᱟᱹᱨᱛᱤ', ho: 'ᱫᱷᱟᱹᱨᱛᱤ', unr: 'धरती', kru: 'धरती', khr: 'धरती', sck: 'भुइयां', bn: 'পৃথিবী', or: 'ପୃଥିବୀ', meaning: 'हमारा प्यारा संसार' },
  { concept: 'flower', en: 'Flower', hi: 'फूल', sat: 'ᱵᱟᱦᱟ', ho: 'ᱵᱟᱦᱟ', unr: 'बाहा', kru: 'पुप्प', khr: 'फूल', sck: 'फूल', bn: 'ফুল', or: 'ଫୁଲ', meaning: 'खुशबूदार पुष्प' }
];

window.OFFLINE_CLASSROOM_PHRASES = [
  {
    patterns: ['welcome', 'स्वागत', 'hello', 'गुड मॉर्निंग', 'good morning', 'नमस्ते'],
    hi: 'बच्चों स्कूल में आपका स्वागत है! नमस्ते!',
    sat: 'ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱟᱥᱲᱟ ᱛᱮ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ! ᱡᱚᱦᱟᱨ!',
    ho: 'ᱜᱤᱫᱤᱨ ᱠᱚ ᱟᱥᱲᱟ ᱨᱮ ᱡᱚᱦᱟᱨ! ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ!',
    unr: 'होन्हार को आषड़ा रे जोहार! अबु मियद नवा काजी चेदोआ।',
    kru: 'खद्दर मन स्कूल नू जय जोहार! इन्ना नाम दव कत्था सिकभो।',
    khr: 'छौआ सभ, स्कूल में तोहीन के सुवागत हे! जोहार!',
    sck: 'छौवा मनके स्कूल में जोहार! आज हमरे नवा चीज सीखब।',
    bn: 'বাচ্চারা স্কুলে তোমাদের স্বাগতম! নমস্কার!',
    or: 'ପିଲାମାନେ ବିଦ୍ୟାଳୟକୁ ସ୍ୱାଗତ! ନମସ୍କାର!',
    simplified: 'प्यारे बच्चों, आपकी कक्षा में आपका बहुत-बहुत स्वागत है!'
  },
  {
    patterns: ['plants', 'पौध', 'धूप', 'पानी', 'sunlight', 'water', 'leaf', 'food'],
    hi: 'पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।',
    sat: 'ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾',
    ho: 'ᱫᱟᱨᱩ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾',
    unr: 'दारू को जोमा बाई लागिन सिंगी मारसाल आर दाः लाकतीया।',
    kru: 'मन्न मनके खना कमआगे बिड़ी रौद अरा अम्म चाहि।',
    khr: 'गाछ-बिरिछ के आपन खाना बनावे ले घाम (रौद) अउर पानी के जरूरत होवऽ हे।',
    sck: 'गाछ मनके आपन भोजन बनाएक ले रौद अउर पानी चाही।',
    bn: 'গাছের খাদ্য তৈরির জন্য সূর্যের আলো এবং জলের প্রয়োজন।',
    or: 'ଗଛକୁ ଖାଦ୍ୟ ତିଆରି କରିବା ପାଇଁ ସୂର୍ଯ୍ୟାଲୋକ ଓ ପାଣି ଦରକାର।',
    simplified: 'छोटे पौधे सूरज की मीठी धूप और जल पीकर बड़े और मजबूत बनते हैं।'
  },
  {
    patterns: ['book', 'कहानी', 'story', 'पढ़', 'read', 'open'],
    hi: 'अपनी किताब खोलो और आओ मिलकर यह कहानी पढ़ें।',
    sat: 'ᱟᱢᱟᱜ ᱯᱩᱛᱷᱤ ᱡᱷᱤᱡᱽ ᱢᱮ ᱟᱨ ᱫᱮᱞᱟ ᱵᱚᱱ ᱱᱚᱶᱟ ᱠᱟᱹᱦᱱᱤ ᱢᱤᱫ ᱛᱮ ᱵᱚᱱ ᱯᱟᱲᱦᱟᱣᱼᱟ᱾',
    ho: 'ᱟᱢᱟᱜ ᱯᱩᱛᱷᱤ ᱠᱩᱞᱤ ᱢᱮ ᱟᱨ ᱫᱮᱞᱟ ᱱᱮᱱ ᱠᱟᱹᱦᱱᱤ ᱯᱟᱲᱦᱟᱣ ᱢᱮ᱾',
    unr: 'आमाः पुथी झिज मे आर देला नेन कहानी मिद ते पढ़वआ।',
    kru: 'तांग्है पुथी उथरा अरा बरा नाम संगे ई खीरी पढा।',
    khr: 'आपन किताब खोला अउर आवा मिल के ई कहानी पढ़ल जाय।',
    sck: 'आपन किताब खोलू अउर आवा संगे ई कहानी पढ़ब।',
    bn: 'তোমার বই খোলো এবং এসো আমরা একসঙ্গে এই গল্পটি পড়ি।',
    or: 'ତୁମ ବହି ଖୋଲ ଏବଂ ଆସ ଆମେ ଏକାଠି ଏହି ଗଳ୍ପ ପଢ଼ିବା।',
    simplified: 'चलो अपनी सुंदर किताब खोलें और गज्जू भाई संग मजेदार कहानी पढ़ें!'
  },
  {
    patterns: ['name', 'नाम', 'what is your name', 'आपका नाम'],
    hi: 'नमस्ते बच्चों! आपका नाम क्या है?',
    sat: 'ᱡᱚᱦᱟᱨ ᱜᱤᱫᱽᱨᱟᱹ! ᱟᱯᱮᱭᱟᱜ ᱧᱩᱛᱩᱢ ᱪᱮᱫ?',
    ho: 'ᱡᱚᱦᱟᱨ ᱜᱤᱫᱤᱨ! ᱟᱢᱟᱜ ᱧᱩᱛᱩᱢ ᱪᱮᱱᱟᱜ?',
    unr: 'जोहार होन्हार! आमाः नुतूम चिनाः?',
    kru: 'जय जोहार खद्दर! निंग्है नामे इन्दिरिके?',
    khr: 'जोहार छौआ सभ! तोहर नाम की हे?',
    sck: 'जोहार छौवा मन! राउर नांव का हेकें?',
    bn: 'নমস্কার বাচ্চারা! তোমাদের নাম কি?',
    or: 'ନମସ୍କାର ପିଲାମାନେ! ତୁମ ନାମ କ’ଣ?',
    simplified: 'प्यारे बच्चे, मुझे अपना प्यारा सा नाम बताओ!'
  }
];

MatrubhasaStorage.prototype.translateOffline = function(text, targetLang = 'sat') {
  if (!text) return { translated: '', simplified: '', confidence: 0.95 };
  const lower = text.toLowerCase().trim();

  // 1. Phrase match
  for (const p of window.OFFLINE_CLASSROOM_PHRASES) {
    for (const pat of p.patterns) {
      if (lower.includes(pat.toLowerCase())) {
        return {
          translated: p[targetLang] || p.hi,
          simplified: p.simplified,
          confidence: 0.98,
          isExactPhrase: true
        };
      }
    }
  }

  // 2. Vocabulary match
  for (const v of window.OFFLINE_TRIBAL_VOCABULARY) {
    if (lower.includes(v.en.toLowerCase()) || lower.includes(v.hi.toLowerCase()) || lower.includes(v.concept)) {
      const trans = v[targetLang] || v.hi;
      return {
        translated: trans,
        simplified: `${v.hi} (${v.meaning})`,
        confidence: 0.94,
        isWord: true
      };
    }
  }

  // 3. Fallback: preserve text with localized wrapper
  return {
    translated: text,
    simplified: text,
    confidence: 0.88,
    isFallback: true
  };
};

// Global offline storage instance
window.matrubhasaDB = new MatrubhasaStorage();

