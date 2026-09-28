/**
 * =============================================================================
 * MATRUBHASA AI -- FIREBASE AUTHENTICATION & FIRESTORE DATABASE
 * =============================================================================
 * Official Authentication System:
 *   - Email/Password Login & Registration
 *   - Google OAuth (One-tap Sign-In)
 *   - Role-based access: teacher / student / parent / coordinator
 *
 * Database (Firestore):
 *   - Real-time cloud sync for ALL data
 *   - Automatic offline persistence (works without internet)
 *   - Auto-sync when back online
 *   - Stores: student_scores, teacher_uploads, lesson_progress, analytics
 *
 * HOW TO SET UP (One-time):
 *   1. Go to https://console.firebase.google.com
 *   2. Create project "matrubhasa-ai"
 *   3. Enable Authentication -> Email/Password + Google
 *   4. Enable Firestore Database
 *   5. Replace the firebaseConfig below with YOUR project config
 * =============================================================================
 */

// =============================================================================
// FIREBASE CONFIGURATION -- Replace with your Firebase project config
// =============================================================================
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyCNDIBqdraKspKTCkrqwgX_bE272-4KxvY",
  authDomain: "matrubhasa-13239.firebaseapp.com",
  projectId: "matrubhasa-13239",
  storageBucket: "matrubhasa-13239.firebasestorage.app",
  messagingSenderId: "662941218050",
  appId: "1:662941218050:web:957eb66a02693220153e1b",
  measurementId: "G-0BNMWZ1WS0"
};

// Set to true after you configure your Firebase project above
const FIREBASE_ENABLED = true;

// =============================================================================
// FIREBASE SDK LOADER
// =============================================================================
async function loadFirebaseSDK() {
  if (!FIREBASE_ENABLED) return false;
  if (window._firebaseLoaded) return true;

  try {
    const { initializeApp } = await import('https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js');
    const {
      getAuth, onAuthStateChanged, signInWithEmailAndPassword,
      createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider,
      signOut, updateProfile
    } = await import('https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js');
    const {
      getFirestore, doc, setDoc, getDoc, addDoc, collection,
      query, where, orderBy, limit, getDocs, onSnapshot,
      enableIndexedDbPersistence, serverTimestamp
    } = await import('https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js');

    const app = initializeApp(FIREBASE_CONFIG);
    const auth = getAuth(app);
    const db = getFirestore(app);

    try {
      await enableIndexedDbPersistence(db);
      console.log('Firestore offline persistence enabled');
    } catch (err) {
      console.warn('Offline persistence issue:', err.code);
    }

    window._firebase = {
      app, auth, db,
      signInWithEmailAndPassword: (email, pass) => signInWithEmailAndPassword(auth, email, pass),
      createUserWithEmailAndPassword: (email, pass) => createUserWithEmailAndPassword(auth, email, pass),
      signInWithGoogle: () => signInWithPopup(auth, new GoogleAuthProvider()),
      signOut: () => signOut(auth),
      updateProfile: (user, data) => updateProfile(user, data),
      onAuthStateChanged: (cb) => onAuthStateChanged(auth, cb),
      doc: (path, ...segments) => doc(db, path, ...segments),
      setDoc, getDoc, addDoc,
      collection: (path) => collection(db, path),
      query, where, orderBy, limit, getDocs, onSnapshot, serverTimestamp
    };

    window._firebaseLoaded = true;
    console.log('Firebase SDK loaded');
    return true;
  } catch (err) {
    console.error('Firebase SDK load error:', err);
    return false;
  }
}

// =============================================================================
// MATRUBHASA AUTH MANAGER
// =============================================================================
class MatrubhasaAuthManager {
  constructor() {
    this.firebaseReady = false;
    this.currentFirebaseUser = null;
    this._authStateCallbacks = [];
    this.init();
  }

  async init() {
    this.firebaseReady = await loadFirebaseSDK();

    if (this.firebaseReady && window._firebase) {
      window._firebase.onAuthStateChanged(async (fbUser) => {
        this.currentFirebaseUser = fbUser;

        if (fbUser) {
          try {
            const profileDoc = await window._firebase.getDoc(
              window._firebase.doc('users', fbUser.uid)
            );

            let userProfile;
            if (profileDoc.exists()) {
              userProfile = { uid: fbUser.uid, ...profileDoc.data() };
            } else {
              userProfile = {
                uid: fbUser.uid,
                name: fbUser.displayName || fbUser.email.split('@')[0],
                email: fbUser.email,
                role: 'teacher',
                lang: 'sat',
                createdAt: new Date().toISOString()
              };
              await window._firebase.setDoc(
                window._firebase.doc('users', fbUser.uid),
                userProfile
              );
            }
            this._onUserSignedIn(userProfile);
          } catch (err) {
            console.error('Error loading user profile:', err);
            const cached = this._getCachedProfile(fbUser.uid);
            if (cached) this._onUserSignedIn(cached);
          }
        } else {
          this._onUserSignedOut();
        }
      });
    }
  }

  async signUp({ name, email, password, role = 'teacher', lang = 'sat', schoolName = '', grade = null }) {
    if (!this.firebaseReady) {
      return this._localSignIn({ name, email, role, lang });
    }
    try {
      this._setAuthLoading(true);
      const credential = await window._firebase.createUserWithEmailAndPassword(email, password);
      const fbUser = credential.user;
      await window._firebase.updateProfile(fbUser, { displayName: name });
      const userProfile = {
        uid: fbUser.uid, name, email, role, lang,
        schoolName: schoolName || '', grade: grade || null,
        createdAt: window._firebase.serverTimestamp(),
        lastLogin: window._firebase.serverTimestamp(),
        totalSessions: 0, totalLessons: 0
      };
      await window._firebase.setDoc(window._firebase.doc('users', fbUser.uid), userProfile);
      this._cacheProfile(fbUser.uid, { ...userProfile, createdAt: new Date().toISOString(), lastLogin: new Date().toISOString() });
      return { success: true, user: userProfile };
    } catch (err) {
      return { success: false, error: this._getErrorMessage(err.code) };
    } finally {
      this._setAuthLoading(false);
    }
  }

  async signIn({ email, password }) {
    if (!this.firebaseReady) {
      return this._localSignIn({ name: email.split('@')[0], email, role: 'teacher', lang: 'sat' });
    }
    try {
      this._setAuthLoading(true);
      const credential = await window._firebase.signInWithEmailAndPassword(email, password);
      try {
        await window._firebase.setDoc(
          window._firebase.doc('users', credential.user.uid),
          { lastLogin: window._firebase.serverTimestamp() },
          { merge: true }
        );
      } catch (e) { /* offline -- ok */ }
      return { success: true };
    } catch (err) {
      return { success: false, error: this._getErrorMessage(err.code) };
    } finally {
      this._setAuthLoading(false);
    }
  }

  async signInWithGoogle(role = 'teacher') {
    if (!this.firebaseReady) {
      return this._localSignIn({ name: 'Google User', email: 'google@matrubhasa.in', role, lang: 'sat' });
    }
    try {
      this._setAuthLoading(true);
      const result = await window._firebase.signInWithGoogle();
      const fbUser = result.user;
      const profileDoc = await window._firebase.getDoc(window._firebase.doc('users', fbUser.uid));
      if (!profileDoc.exists()) {
        await window._firebase.setDoc(window._firebase.doc('users', fbUser.uid), {
          uid: fbUser.uid,
          name: fbUser.displayName || 'Educator',
          email: fbUser.email,
          role, lang: 'sat',
          createdAt: window._firebase.serverTimestamp(),
          lastLogin: window._firebase.serverTimestamp(),
          totalSessions: 0
        });
      } else {
        await window._firebase.setDoc(
          window._firebase.doc('users', fbUser.uid),
          { lastLogin: window._firebase.serverTimestamp() },
          { merge: true }
        );
      }
      return { success: true };
    } catch (err) {
      if (err.code === 'auth/popup-closed-by-user') return { success: false, error: null };
      return { success: false, error: this._getErrorMessage(err.code) };
    } finally {
      this._setAuthLoading(false);
    }
  }

  async signOut() {
    if (this.firebaseReady) {
      try { await window._firebase.signOut(); } catch (err) { console.error('Sign out error:', err); }
    }
    this._onUserSignedOut();
  }

  _localSignIn(user) {
    const localUser = { ...user, uid: 'local_' + Date.now(), isLocal: true };
    this._onUserSignedIn(localUser);
    return { success: true, user: localUser };
  }

  _onUserSignedIn(userProfile) {
    if (window.state) window.state.currentUser = userProfile;
    localStorage.setItem('matrubhasa_current_user', JSON.stringify(userProfile));

    if (userProfile.lang && window.I18N) window.I18N.setLang(userProfile.lang);

    const authModal = document.getElementById('authModal');
    if (authModal) authModal.style.display = 'none';

    if (typeof updateUserProfileUI === 'function') updateUserProfileUI(userProfile);

    const lastSession = localStorage.getItem('mb_last_session');
    const now = Date.now();
    if (!lastSession || (now - parseInt(lastSession)) > 3600000) {
      localStorage.setItem('mb_last_session', now.toString());
      if (typeof playCinematicWelcome === 'function') playCinematicWelcome(userProfile);
    }

    this._syncPendingData(userProfile);
    this._authStateCallbacks.forEach(cb => cb(userProfile));
    window.dispatchEvent(new CustomEvent('matrubhasa:userSignedIn', { detail: userProfile }));
    console.log('User signed in: ' + userProfile.name + ' (' + userProfile.role + ')');
  }

  _onUserSignedOut() {
    if (window.state) window.state.currentUser = null;
    localStorage.removeItem('matrubhasa_current_user');

    const authModal = document.getElementById('authModal');
    if (authModal) authModal.style.display = 'flex';

    const profilePill = document.getElementById('userProfilePill');
    if (profilePill) profilePill.style.display = 'none';

    this._authStateCallbacks.forEach(cb => cb(null));
    window.dispatchEvent(new CustomEvent('matrubhasa:userSignedOut'));
    console.log('User signed out');
  }

  _setAuthLoading(loading) {
    const submitBtn = document.getElementById('authSubmitBtn');
    const googleBtn = document.getElementById('googleSignInBtn');
    if (submitBtn) {
      submitBtn.disabled = loading;
      if (loading) {
        submitBtn.textContent = 'Authenticating...';
      }
    }
    if (googleBtn) googleBtn.disabled = loading;
  }

  _cacheProfile(uid, profile) {
    try {
      const cache = JSON.parse(localStorage.getItem('mb_profile_cache') || '{}');
      cache[uid] = profile;
      localStorage.setItem('mb_profile_cache', JSON.stringify(cache));
    } catch (e) {}
  }

  _getCachedProfile(uid) {
    try {
      const cache = JSON.parse(localStorage.getItem('mb_profile_cache') || '{}');
      return cache[uid] || null;
    } catch (e) { return null; }
  }

  _getErrorMessage(code) {
    const messages = {
      'auth/user-not-found': 'Koi account nahi mila is email se. Pehle Register karein.',
      'auth/wrong-password': 'Password galat hai. Phir se try karein.',
      'auth/email-already-in-use': 'Yeh email pehle se registered hai. Login karein.',
      'auth/weak-password': 'Password kam se kam 6 characters ka hona chahiye.',
      'auth/invalid-email': 'Valid email address enter karein.',
      'auth/network-request-failed': 'Network error. Internet connection check karein.',
      'auth/too-many-requests': 'Bahut zyada attempts. Kuch der baad try karein.',
    };
    return messages[code] || ('Error: ' + code);
  }

  // ========================
  // FIRESTORE DATA OPERATIONS
  // ========================
  async saveStudentScore(data) {
    const user = this.getCurrentUser();
    if (!user) return false;

    const entry = {
      userId: user.uid || 'local',
      studentName: user.name,
      studentEmail: user.email,
      role: user.role,
      lang: user.lang || data.lang || 'sat',
      lessonId: data.lessonId,
      lessonTitle: data.lessonTitle || '',
      accuracyPct: data.accuracyPct,
      stars: data.stars,
      timestamp: new Date().toISOString(),
      deviceOnline: navigator.onLine,
      schoolName: user.schoolName || '',
      grade: user.grade || null,
      synced: false
    };

    if (window.matrubhasaDB) {
      await window.matrubhasaDB.recordStudentScore(entry);
    }

    if (this.firebaseReady && navigator.onLine && window._firebase) {
      try {
        await window._firebase.addDoc(
          window._firebase.collection('student_scores'),
          { ...entry, synced: true, timestamp: window._firebase.serverTimestamp() }
        );
        entry.synced = true;
      } catch (err) {
        this._queueForSync('student_scores', entry);
      }
    } else {
      this._queueForSync('student_scores', entry);
    }
    return entry;
  }

  async saveTeacherUpload(data) {
    const user = this.getCurrentUser();
    if (!user || user.role !== 'teacher') return false;

    const upload = {
      teacherId: user.uid || 'local',
      teacherName: user.name,
      teacherEmail: user.email,
      title: data.title,
      content: data.content || '',
      contentType: data.contentType || 'lesson',
      targetGrade: data.targetGrade || null,
      targetLang: data.targetLang || user.lang || 'sat',
      schoolName: user.schoolName || '',
      timestamp: new Date().toISOString(),
      status: 'draft',
      attachmentUrl: data.attachmentUrl || null,
      nipunCode: data.nipunCode || null
    };

    if (this.firebaseReady && navigator.onLine && window._firebase) {
      try {
        const ref = await window._firebase.addDoc(
          window._firebase.collection('teacher_uploads'),
          { ...upload, timestamp: window._firebase.serverTimestamp() }
        );
        upload.id = ref.id;
        return { success: true, id: ref.id, data: upload };
      } catch (err) {
        console.warn('Upload queued for sync:', err.message);
      }
    }
    this._queueForSync('teacher_uploads', upload);
    return { success: true, queued: true, data: upload };
  }

  async logEvent(eventType, data) {
    if (!data) data = {};
    const user = this.getCurrentUser();
    const event = {
      userId: (user && user.uid) ? user.uid : 'anonymous',
      userName: (user && user.name) ? user.name : 'Unknown',
      role: (user && user.role) ? user.role : 'unknown',
      eventType,
      lang: (user && user.lang) ? user.lang : 'sat',
      timestamp: new Date().toISOString(),
      deviceOnline: navigator.onLine
    };
    Object.assign(event, data);
    this._queueForSync('analytics_events', event);

    if (this.firebaseReady && navigator.onLine && window._firebase) {
      try {
        await window._firebase.addDoc(
          window._firebase.collection('analytics_events'),
          { ...event, timestamp: window._firebase.serverTimestamp() }
        );
      } catch (e) { /* silent */ }
    }
  }

  async getStudentScores(limitCount) {
    if (!limitCount) limitCount = 50;
    if (!this.firebaseReady || !navigator.onLine || !window._firebase) {
      if (window.matrubhasaDB) return window.matrubhasaDB.getRecentScores();
      return [];
    }
    const user = this.getCurrentUser();
    if (!user) return [];
    try {
      let q;
      if (user.role === 'teacher') {
        q = window._firebase.query(
          window._firebase.collection('student_scores'),
          window._firebase.where('schoolName', '==', user.schoolName || ''),
          window._firebase.orderBy('timestamp', 'desc'),
          window._firebase.limit(limitCount)
        );
      } else {
        q = window._firebase.query(
          window._firebase.collection('student_scores'),
          window._firebase.where('userId', '==', user.uid),
          window._firebase.orderBy('timestamp', 'desc'),
          window._firebase.limit(limitCount)
        );
      }
      const snapshot = await window._firebase.getDocs(q);
      return snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (err) {
      return window.matrubhasaDB ? window.matrubhasaDB.getRecentScores() : [];
    }
  }

  async updateProfile(updates) {
    const user = this.getCurrentUser();
    if (!user) return false;
    const updated = Object.assign({}, user, updates);
    localStorage.setItem('matrubhasa_current_user', JSON.stringify(updated));
    if (window.state) window.state.currentUser = updated;
    if (this.firebaseReady && navigator.onLine && window._firebase && user.uid) {
      try {
        await window._firebase.setDoc(window._firebase.doc('users', user.uid), updates, { merge: true });
      } catch (err) { /* queued */ }
    }
    return updated;
  }

  // ========================
  // OFFLINE SYNC QUEUE
  // ========================
  _queueForSync(col, data) {
    try {
      const queue = JSON.parse(localStorage.getItem('mb_sync_queue') || '[]');
      queue.push({ collection: col, data: data, queuedAt: new Date().toISOString() });
      localStorage.setItem('mb_sync_queue', JSON.stringify(queue));
    } catch (e) {}
  }

  async _syncPendingData(user) {
    if (!this.firebaseReady || !navigator.onLine || !window._firebase) return;
    try {
      const queue = JSON.parse(localStorage.getItem('mb_sync_queue') || '[]');
      if (!queue.length) return;
      const failed = [];
      for (const item of queue) {
        try {
          await window._firebase.addDoc(
            window._firebase.collection(item.collection),
            { ...item.data, syncedAt: window._firebase.serverTimestamp() }
          );
        } catch (err) {
          failed.push(item);
        }
      }
      localStorage.setItem('mb_sync_queue', JSON.stringify(failed));
      const synced = queue.length - failed.length;
      if (synced > 0) this._showSyncNotification(synced);
    } catch (e) {}
  }

  _showSyncNotification(count) {
    const toast = document.createElement('div');
    toast.className = 'mb-sync-toast';
    toast.innerHTML = '<span>??</span> <strong>' + count + ' record' + (count > 1 ? 's' : '') + '</strong> synced to cloud database';
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('visible'), 100);
    setTimeout(() => {
      toast.classList.remove('visible');
      setTimeout(() => toast.remove(), 400);
    }, 3000);
  }

  // ========================
  // UTILITY
  // ========================
  getCurrentUser() {
    if (window.state && window.state.currentUser) return window.state.currentUser;
    try {
      return JSON.parse(localStorage.getItem('matrubhasa_current_user') || 'null');
    } catch (e) { return null; }
  }

  isSignedIn() {
    return !!this.getCurrentUser();
  }

  onAuthStateChanged(callback) {
    this._authStateCallbacks.push(callback);
    const user = this.getCurrentUser();
    if (user) callback(user);
  }
}

// =============================================================================
// ENHANCED AUTH UI
// =============================================================================
class MatrubhasaAuthUI {
  constructor(authManager) {
    this.auth = authManager;
    this.mode = 'login';
    this.selectedRole = 'teacher';
    this._init();
  }

  _init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this._setupUI());
    } else {
      this._setupUI();
    }
  }

  _setupUI() {
    this._injectUI();
    this._bindEvents();
    this._checkExistingSession();
  }

  _injectUI() {
    // Inject styles for sync toast and error messages if needed
    if (!document.getElementById('mbAuthStyles')) {
      const style = document.createElement('style');
      style.id = 'mbAuthStyles';
      style.textContent = [
        '.mb-sync-toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:linear-gradient(135deg,#1a2744,#0d4f3c);color:#fff;padding:12px 24px;border-radius:50px;font-size:14px;font-weight:600;display:flex;align-items:center;gap:10px;box-shadow:0 8px 32px rgba(0,0,0,.3);z-index:99999;transition:transform .4s cubic-bezier(.34,1.56,.64,1);border:1px solid rgba(255,255,255,.1);}',
        '.mb-sync-toast.visible{transform:translateX(-50%) translateY(0);}',
        '.btn-google-signin{width:100%;display:flex;align-items:center;justify-content:center;gap:4px;padding:14px 20px;background:#fff;color:#333;border:2px solid #e0e0e0;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;transition:all .2s ease;margin-bottom:16px;margin-top:8px;}',
        '.btn-google-signin:hover{background:#f8f8f8;border-color:#4285F4;box-shadow:0 4px 12px rgba(66,133,244,.2);transform:translateY(-1px);}',
        '.btn-google-signin:disabled{opacity:.6;cursor:not-allowed;}'
      ].join('');
      document.head.appendChild(style);
    }
  }

  _bindEvents() {
    // Bind Google Sign In button
    const googleBtn = document.getElementById('googleSignInBtn');
    if (googleBtn) {
      const newBtn = googleBtn.cloneNode(true);
      googleBtn.parentNode.replaceChild(newBtn, googleBtn);
      newBtn.addEventListener('click', () => this._handleGoogleSignIn());
    }

    // Role tabs (Keep role selection for Google Auth)
    document.querySelectorAll('.role-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this.selectedRole = tab.getAttribute('data-role');
      });
    });

    // Logout button
    const authTriggerBtn = document.getElementById('authTriggerBtn');
    if (authTriggerBtn) {
      const newBtn = authTriggerBtn.cloneNode(true);
      authTriggerBtn.parentNode.replaceChild(newBtn, authTriggerBtn);
      newBtn.addEventListener('click', () => this.auth.signOut());
    }

    // Online sync trigger
    window.addEventListener('online', () => {
      const user = this.auth.getCurrentUser();
      if (user) this.auth._syncPendingData(user);
    });
  }

  async _handleGoogleSignIn() {
    this._clearError();
    const result = await this.auth.signInWithGoogle(this.selectedRole);
    if (result && !result.success && result.error) this._showError(result.error);
  }

  _showError(msg) {
    let errEl = document.getElementById('authErrorMsg');
    if (errEl) {
      errEl.textContent = msg;
      errEl.style.display = 'block';
      const pwGroup = document.getElementById('passwordGroup');
      if (pwGroup) pwGroup.style.display = 'block';
    } else {
      const status = document.getElementById('otpTimerStatus');
      if (status) {
        status.textContent = msg;
        status.style.color = '#ff6b6b';
      }
    }
  }

  _clearError() {
    const errEl = document.getElementById('authErrorMsg');
    if (errEl) errEl.style.display = 'none';
    const status = document.getElementById('otpTimerStatus');
    if (status) status.style.color = '';
  }

  _checkExistingSession() {
    const savedUser = localStorage.getItem('matrubhasa_current_user');
    if (savedUser) {
      try {
        const user = JSON.parse(savedUser);
        this.auth._onUserSignedIn(user);
      } catch (e) {}
    } else {
      const authModal = document.getElementById('authModal');
      if (authModal) authModal.style.display = 'flex';
    }
  }
}

// =============================================================================
// INITIALIZE
// =============================================================================
window.MatrubhasaAuth = new MatrubhasaAuthManager();
window.MatrubhasaAuthUI = new MatrubhasaAuthUI(window.MatrubhasaAuth);
window.mbAuth = window.MatrubhasaAuth;

// Override existing functions
window.completeAuthentication = function(user) {
  window.MatrubhasaAuth._localSignIn(user);
};
window.logoutUser = function() {
  window.MatrubhasaAuth.signOut();
};
window.mbLogEvent = function(eventType, data) {
  return window.MatrubhasaAuth.logEvent(eventType, data);
};
window.mbSaveScore = function(data) {
  return window.MatrubhasaAuth.saveStudentScore(data);
};

console.log('Matrubhasa Firebase Auth & Firestore ready');
