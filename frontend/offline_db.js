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

// Global offline storage instance
window.matrubhasaDB = new MatrubhasaStorage();

