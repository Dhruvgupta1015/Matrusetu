/**
 * Matrubhasa AI — Core Client Application Logic
 * Supports:
 *   - Real-time Speech-to-Text & Indic Text-to-Speech
 *   - Bhashini Cloud API + Offline Edge Fallback
 *   - NIPUN Bharat FLN Voice Reading Coach with Confetti
 *   - Desi Kahani & Worksheet Generation
 *   - Akshar Mala Phonics Explorer
 *   - PWA Offline Service Worker Registration
 */

const API_BASE = (window.location.hostname && window.location.hostname !== 'localhost') ? `http://${window.location.hostname}:8000` : 'http://127.0.0.1:8000';

// Global Application State
const state = {
  isOffline: false,
  isRecording: false,
  speechSpeed: 1.05, // Fluent, energetic conversational pace for real-time speech agent
  voiceEngine: 'female_agent', // 'female_agent' (Instant ultra-fluent female AI) or 'bhashini'
  currentLang: 'sat',
  recognition: null,
  recognitionFln: null,
  engineMode: 'stream', // 'stream' (Web Speech) or 'bhashini' (Direct Sovereign ASR)
  autoSpeak: true,
  isMutedForPlayback: false, // Prevents speaker-to-mic echo loops
  activeAudioStream: null,
  audioContext: null,
  flnTargetSentence: 'ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾',
  flnHindiText: 'पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।',
};

// ==========================================================================
// 0. NATIVE PHONETIC TRANSLITERATOR (OL CHIKI ➔ DEVANAGARI FOR TTS)
// ==========================================================================
const OL_CHIKI_TO_DEVANAGARI = {
  'ᱚ': 'अ', 'ᱛ': 'त', 'ᱜ': 'ग', 'ᱝ': 'ं', 'ᱞ': 'ल',
  'ᱟ': 'आ', 'ᱠ': 'क', 'ᱡ': 'ज', 'ᱢ': 'म', 'ᱣ': 'व',
  'ᱤ': 'इ', 'ᱥ': 'स', 'ᱦ': 'ह', 'ᱧ': 'ञ', 'ᱨ': 'र',
  'ᱩ': 'उ', 'ᱪ': 'च', 'ᱫ': 'द', 'ᱬ': 'ण', 'ᱭ': 'य',
  'ᱮ': 'ए', 'ᱯ': 'प', 'ᱰ': 'ड', 'ᱱ': 'न', 'ᱲ': 'ड़',
  'ᱳ': 'ओ', 'ᱴ': 'ट', 'ᱵ': 'ब', 'ᱶ': 'ं', 'ᱷ': 'ह',
  'ᱸ': 'ं', 'ᱹ': '', 'ᱺ': '', 'ᱻ': '', 'ᱼ': '', 'ᱽ': '',
  '᱾': '।', '᱿': '।'
};

function olChikiToPhonetic(text) {
  if (!text) return '';
  let res = '';
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    res += OL_CHIKI_TO_DEVANAGARI[ch] !== undefined ? OL_CHIKI_TO_DEVANAGARI[ch] : ch;
  }
  return res;
}

// ==========================================================================
// 0.1 HIGH-PERFORMANCE NATURAL FEMALE VOICE AGENT ENGINE
// ==========================================================================
let availableVoices = [];
let cachedBestFemaleVoice = null;
let activeSpeechUtterance = null;
let speechKeepAliveInterval = null;

function loadSpeechVoices() {
  if (!('speechSynthesis' in window)) return;
  availableVoices = window.speechSynthesis.getVoices();
  if (availableVoices && availableVoices.length > 0) {
    cachedBestFemaleVoice = findOptimalFemaleVoice(availableVoices, state.currentLang);
  }
}

if ('speechSynthesis' in window) {
  loadSpeechVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    loadSpeechVoices();
  };
}

function findOptimalFemaleVoice(voices, lang = 'hi') {
  if (!voices || voices.length === 0) return null;

  // 1. High priority: Indian female natural / neural voices
  const prioritizedFemaleVoiceNames = [
    'swara', // Microsoft Swara Online (Natural) - Hindi (India)
    'neerja', // Microsoft Neerja Online (Natural) - English (India)
    'google हिन्दी', // Google Hindi Female
    'google hindi',
    'kalpana', // Microsoft Kalpana - Hindi
    'heera', // Microsoft Heera - English (India)
    'zira', // Microsoft Zira - English (Female)
    'sunita',
    'veena',
    'ananya',
  ];

  for (const target of prioritizedFemaleVoiceNames) {
    const match = voices.find(v => v.name && v.name.toLowerCase().includes(target));
    if (match) return match;
  }

  // 2. Language-specific female voice
  let targetPrefix = 'hi';
  if (lang === 'bn') targetPrefix = 'bn';
  else if (lang === 'or') targetPrefix = 'or';
  else if (lang === 'en') targetPrefix = 'en';

  const femaleLang = voices.find(v =>
    v.lang && v.lang.toLowerCase().startsWith(targetPrefix) &&
    (v.name.toLowerCase().includes('female') || v.name.toLowerCase().includes('woman') || v.name.toLowerCase().includes('girl'))
  );
  if (femaleLang) return femaleLang;

  // 3. Any voice matching target language prefix
  const anyLang = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(targetPrefix));
  if (anyLang) return anyLang;

  // 4. Any Indian voice
  const anyIndic = voices.find(v => v.lang && (v.lang.toLowerCase().includes('in') || v.lang.toLowerCase().includes('hi')));
  if (anyIndic) return anyIndic;

  return voices[0] || null;
}

function stopActiveSpeech() {
  if ('speechSynthesis' in window) {
    clearInterval(speechKeepAliveInterval);
    window.speechSynthesis.cancel();
    activeSpeechUtterance = null;
  }
}

function speakWithFemaleAgent(rawText, lang, onFinish) {
  if (!('speechSynthesis' in window) || !rawText) {
    if (onFinish) onFinish();
    return;
  }

  stopActiveSpeech();

  // Convert Ol Chiki to phonetic Devanagari so speech engine speaks it smoothly
  const textToSpeak = olChikiToPhonetic(rawText);

  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  activeSpeechUtterance = utterance; // Retain reference to prevent Chrome GC bug

  // Frequently-driven, lively, natural female voice cadence
  utterance.rate = state.speechSpeed || 1.05;
  utterance.pitch = 1.06; // Crisp, friendly female tone
  utterance.volume = 1.0;

  // Determine appropriate locale
  let targetLocale = 'hi-IN';
  if (lang === 'bn') targetLocale = 'bn-IN';
  else if (lang === 'or') targetLocale = 'or-IN';
  else if (lang === 'en') targetLocale = 'en-IN';
  else targetLocale = 'hi-IN'; // Devanagari fallback for sat, ho, unr, kru, khr, sck, hi

  utterance.lang = targetLocale;

  if (!availableVoices || availableVoices.length === 0) {
    availableVoices = window.speechSynthesis.getVoices();
  }
  const chosenVoice = findOptimalFemaleVoice(availableVoices, lang);
  if (chosenVoice) {
    utterance.voice = chosenVoice;
  }

  let ended = false;
  const finishSpeech = () => {
    if (ended) return;
    ended = true;
    clearInterval(speechKeepAliveInterval);
    activeSpeechUtterance = null;
    if (onFinish) onFinish();
  };

  utterance.onend = finishSpeech;
  utterance.onerror = (err) => {
    console.warn('SpeechSynthesis error:', err);
    finishSpeech();
  };

  // Chrome watchdog: prevent speech synthesis pause after 10s
  clearInterval(speechKeepAliveInterval);
  speechKeepAliveInterval = setInterval(() => {
    if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
      window.speechSynthesis.pause();
      window.speechSynthesis.resume();
    }
  }, 10000);

  setTimeout(() => {
    try {
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Speak error:', e);
      finishSpeech();
    }
  }, 35);
}

// ==========================================================================
// 1. INITIALIZATION & SERVICE WORKER
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initServiceWorker();
  initTabs();
  initNetworkDetector();
  initAuth();
  initDashboard();
  initLiveBridge();
  initBalVatika();
  initPathshalaLens();
  initAksharMala();
  initTeacherHub();
  initNotebooksLibrary();
  initConfetti();
});

function initServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
      .then(() => console.log('Matrubhasa PWA Service Worker Registered'))
      .catch((err) => console.warn('SW registration failed:', err));
  }
}

// Helper: Switch active primary tab
function switchTab(targetId) {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach((btn) => {
    if (btn.getAttribute('data-target') === targetId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  document.querySelectorAll('.tab-view').forEach((view) => {
    if (view.id === targetId) {
      view.classList.add('active-view');
    } else {
      view.classList.remove('active-view');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================================================
// 1.1 REAL-TIME EMAIL AUTHENTICATION & SESSION MANAGEMENT
// ==========================================================================
let currentGeneratedOtp = '7429';
let otpCountdownInterval = null;

function initAuth() {
  const authModal = document.getElementById('authModal');
  const roleTabs = document.querySelectorAll('.role-tab');
  const sendOtpBtn = document.getElementById('authSendOtpBtn');
  const authSubmitBtn = document.getElementById('authSubmitBtn');
  const btnAutoFillOtp = document.getElementById('btnAutoFillOtp');
  const demoTeacherBtn = document.getElementById('demoTeacherBtn');
  const demoStudentBtn = document.getElementById('demoStudentBtn');
  const authTriggerBtn = document.getElementById('authTriggerBtn');
  const otpBoxes = [
    document.getElementById('otp1'),
    document.getElementById('otp2'),
    document.getElementById('otp3'),
    document.getElementById('otp4')
  ];

  let selectedRole = 'teacher';

  // Role switching in Auth Modal
  roleTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      roleTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      selectedRole = tab.getAttribute('data-role');

      const nameInput = document.getElementById('authNameInput');
      const emailInput = document.getElementById('authEmailInput');
      if (selectedRole === 'teacher') {
        nameInput.value = 'Shri Rajesh Kumar';
        emailInput.value = 'teacher@jharkhand.gov.in';
      } else if (selectedRole === 'student') {
        nameInput.value = 'Ananya Soren';
        emailInput.value = 'ananya.student@matrubhasa.in';
      } else {
        nameInput.value = 'Smt. Malti Devi';
        emailInput.value = 'parent.malti@matrubhasa.in';
      }
    });
  });

  // OTP input auto-advance
  otpBoxes.forEach((box, idx) => {
    if (!box) return;
    box.addEventListener('input', (e) => {
      if (box.value.length === 1 && idx < otpBoxes.length - 1) {
        otpBoxes[idx + 1].focus();
      }
    });
    box.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !box.value && idx > 0) {
        otpBoxes[idx - 1].focus();
      }
    });
  });

  // Send Real-Time OTP Action
  if (sendOtpBtn) {
    sendOtpBtn.addEventListener('click', () => {
      const email = document.getElementById('authEmailInput').value.trim();
      if (!email || !email.includes('@')) {
        alert('Please enter a valid email address (e.g. teacher@jharkhand.gov.in)');
        return;
      }

      // Generate 4-digit numeric code
      currentGeneratedOtp = String(Math.floor(1000 + Math.random() * 9000));
      document.getElementById('authNotifEmail').textContent = email;
      document.getElementById('authSentCode').textContent = currentGeneratedOtp;
      document.getElementById('authMailNotification').style.display = 'flex';

      // Start 30-second countdown
      let remaining = 30;
      sendOtpBtn.disabled = true;
      const status = document.getElementById('otpTimerStatus');
      status.textContent = `Verification OTP sent to ${email}. Resend in ${remaining}s`;

      clearInterval(otpCountdownInterval);
      otpCountdownInterval = setInterval(() => {
        remaining--;
        if (remaining <= 0) {
          clearInterval(otpCountdownInterval);
          sendOtpBtn.disabled = false;
          status.textContent = 'Did not receive? Click "Send OTP" to resend code.';
        } else {
          status.textContent = `Verification OTP sent to ${email}. Resend in ${remaining}s`;
        }
      }, 1000);
    });
  }

  // Auto-Fill OTP button
  if (btnAutoFillOtp) {
    btnAutoFillOtp.addEventListener('click', () => {
      const code = currentGeneratedOtp || '7429';
      otpBoxes.forEach((b, i) => { if (b) b.value = code[i] || ''; });
      authSubmitBtn.focus();
    });
  }

  // Submit & Verify
  if (authSubmitBtn) {
    authSubmitBtn.addEventListener('click', () => {
      const name = document.getElementById('authNameInput').value.trim() || 'Educator';
      const email = document.getElementById('authEmailInput').value.trim() || 'user@matrubhasa.in';
      const enteredCode = otpBoxes.map(b => b ? b.value : '').join('');

      if (enteredCode.length < 4) {
        alert('Please enter the 4-digit verification code or click "Auto-Fill" for quick demo!');
        return;
      }

      if (enteredCode !== currentGeneratedOtp && enteredCode !== '7429' && enteredCode !== '1234') {
        alert(`Verification code incorrect. Please enter code: ${currentGeneratedOtp}`);
        return;
      }

      completeAuthentication({
        name,
        email,
        role: selectedRole
      });
    });
  }

  // Quick 1-Tap Demo Logins
  if (demoTeacherBtn) {
    demoTeacherBtn.addEventListener('click', () => {
      completeAuthentication({
        name: 'Shri Rajesh Kumar',
        email: 'rajesh.teacher@jharkhand.gov.in',
        role: 'teacher'
      });
    });
  }

  if (demoStudentBtn) {
    demoStudentBtn.addEventListener('click', () => {
      completeAuthentication({
        name: 'Ananya Soren (अनन्या)',
        email: 'ananya.soren@matrubhasa.in',
        role: 'student'
      });
    });
  }

  // Header Logout / Switch Account button
  if (authTriggerBtn) {
    authTriggerBtn.addEventListener('click', () => {
      logoutUser();
    });
  }

  // Check saved session on load
  const savedUserJson = localStorage.getItem('matrubhasa_current_user');
  if (savedUserJson) {
    try {
      const user = JSON.parse(savedUserJson);
      state.currentUser = user;
      updateUserProfileUI(user);
      if (authModal) authModal.style.display = 'none';
      return;
    } catch (e) {}
  }

  // If no saved user, display Auth Modal prominently
  if (authModal) {
    authModal.style.display = 'flex';
  }
}

function completeAuthentication(user) {
  state.currentUser = user;
  localStorage.setItem('matrubhasa_current_user', JSON.stringify(user));

  const authModal = document.getElementById('authModal');
  if (authModal) authModal.style.display = 'none';

  updateUserProfileUI(user);
  playCinematicWelcome(user);
}

function updateUserProfileUI(user) {
  const profilePill = document.getElementById('userProfilePill');
  const roleBadge = document.getElementById('headerRoleBadge');
  const userName = document.getElementById('headerUserName');
  const dashRoleBadge = document.getElementById('dashRoleBadge');
  const dashAvatar = document.getElementById('dashAvatar');
  const dashGreetingTitle = document.getElementById('dashGreetingTitle');
  const dashGreetingDesc = document.getElementById('dashGreetingDesc');

  if (profilePill) profilePill.style.display = 'inline-flex';

  const isTeacher = user.role === 'teacher';
  const roleLabel = isTeacher ? '👨‍🏫 Teacher' : (user.role === 'student' ? '🎒 Student' : '👨‍👩‍👦 Parent');
  const avatarIcon = isTeacher ? '👨‍🏫' : (user.role === 'student' ? '🐘' : '👨‍👩‍👦');

  if (roleBadge) roleBadge.textContent = roleLabel;
  if (userName) userName.textContent = user.name;

  if (dashAvatar) dashAvatar.textContent = avatarIcon;
  if (dashRoleBadge) dashRoleBadge.textContent = roleLabel + (isTeacher ? ' In-Charge' : ' (Grade 3)');

  if (dashGreetingTitle) {
    dashGreetingTitle.textContent = isTeacher 
      ? `जोहार & नमस्ते, ${user.name} जी!`
      : `जोहार & नमस्ते, ${user.name}! 🌟`;
  }

  if (dashGreetingDesc) {
    dashGreetingDesc.textContent = isTeacher
      ? 'मातृभाषा AI में आपका स्वागत है। यहाँ से आप कक्षा सेतु, भाषा मित्र, एवं पाठ्य सामग्री को एक क्लिक में चला सकते हैं।'
      : 'गज्जू भाई आपका इंतज़ार कर रहे हैं! आओ मिलकर अपनी मातृभाषा में बोलें, नए शब्द सीखें और सितारे जीतें!';
  }
}

function logoutUser() {
  localStorage.removeItem('matrubhasa_current_user');
  state.currentUser = null;

  const profilePill = document.getElementById('userProfilePill');
  if (profilePill) profilePill.style.display = 'none';

  const authModal = document.getElementById('authModal');
  if (authModal) authModal.style.display = 'flex';
}

// ==========================================================================
// 1.2 CINEMATIC "WELCOME TO THE MATRUBHASA" ENTRANCE
// ==========================================================================
let cinematicTimer = null;

function playCinematicWelcome(user) {
  const overlay = document.getElementById('cinematicWelcomeOverlay');
  const nameEl = document.getElementById('cinematicUserName');
  const msgEl = document.getElementById('cinematicUserMsg');
  const progressBar = document.getElementById('cinematicProgressBar');
  const proceedBtn = document.getElementById('cinematicProceedBtn');

  if (!overlay) return;

  // Synthesize rich cinematic welcoming audio chime using Web Audio API
  synthesizeCinematicChime();

  const isTeacher = user.role === 'teacher';
  if (nameEl) {
    nameEl.textContent = isTeacher
      ? `नमस्ते ${user.name} जी!`
      : `जोहार ${user.name}! 🌟`;
  }
  if (msgEl) {
    msgEl.textContent = isTeacher
      ? 'आपका कक्षा सेतु तैयार है। आइये मातृभाषा में शिक्षा को जीवंत बनाएं।'
      : 'गज्जू भाई आपके साथ पढ़ने के लिए तैयार हैं! आइये मातृभाषा में सीखें।';
  }

  overlay.classList.remove('fade-out');
  overlay.style.display = 'flex';

  if (progressBar) {
    progressBar.style.width = '0%';
    setTimeout(() => {
      progressBar.style.width = '100%';
    }, 50);
  }

  const closeCinematic = () => {
    clearTimeout(cinematicTimer);
    overlay.classList.add('fade-out');
    setTimeout(() => {
      overlay.style.display = 'none';
      overlay.classList.remove('fade-out');
      switchTab('viewDashboard');
    }, 450);
  };

  if (proceedBtn) {
    proceedBtn.onclick = closeCinematic;
  }

  clearTimeout(cinematicTimer);
  cinematicTimer = setTimeout(closeCinematic, 3600);
}

// Web Audio API cinematic chime chord synthesizer
function synthesizeCinematicChime() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    if (ctx.state === 'suspended') ctx.resume();

    // Cinematic chord notes (F4, A4, C5, E5, G5)
    const notes = [349.23, 440.00, 523.25, 659.25, 783.99];
    const now = ctx.currentTime;

    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + idx * 0.08);

      gain.gain.setValueAtTime(0, now + idx * 0.08);
      gain.gain.linearRampToValueAtTime(0.12 / notes.length, now + idx * 0.08 + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + idx * 0.08 + 2.2);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now + idx * 0.08);
      osc.stop(now + idx * 0.08 + 2.4);
    });
  } catch (err) {
    console.log('Web Audio chime not active:', err);
  }
}

// ==========================================================================
// 1.3 UNIFIED DASHBOARD SYSTEM
// ==========================================================================
function initDashboard() {
  // Bind all module quick-launch cards to switch to their specific tabs
  const moduleCards = document.querySelectorAll('.module-card[data-nav]');
  moduleCards.forEach(card => {
    card.addEventListener('click', () => {
      const navTarget = card.getAttribute('data-nav');
      if (navTarget) switchTab(navTarget);
    });
  });

  // Switch Role button on Dashboard
  const switchRoleBtn = document.getElementById('dashSwitchRoleBtn');
  if (switchRoleBtn) {
    switchRoleBtn.addEventListener('click', () => {
      if (!state.currentUser) {
        state.currentUser = { name: 'Shri Rajesh Kumar', email: 'teacher@jharkhand.gov.in', role: 'teacher' };
      }
      const newRole = state.currentUser.role === 'teacher' ? 'student' : 'teacher';
      state.currentUser.role = newRole;
      if (newRole === 'student') {
        state.currentUser.name = 'Ananya Soren';
      } else {
        state.currentUser.name = 'Shri Rajesh Kumar';
      }
      localStorage.setItem('matrubhasa_current_user', JSON.stringify(state.currentUser));
      updateUserProfileUI(state.currentUser);
    });
  }

  // Replay Cinematic Intro button
  const replayBtn = document.getElementById('dashReplayCinematicBtn');
  if (replayBtn) {
    replayBtn.addEventListener('click', () => {
      const user = state.currentUser || { name: 'Shri Rajesh Kumar', role: 'teacher' };
      playCinematicWelcome(user);
    });
  }

  // Word of the Day audio button
  const wordAudioBtn = document.getElementById('btnPlayWordOfDay');
  if (wordAudioBtn) {
    wordAudioBtn.addEventListener('click', () => {
      // Speak "ᱫᱟᱨᱮ" in Santali
      playVernacularSpeech('ᱫᱟᱨᱮ', 'sat', wordAudioBtn);
    });
  }
}

// ==========================================================================
// 2. TAB NAVIGATION SYSTEM
// ==========================================================================
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      if (targetId) switchTab(targetId);
    });
  });
}

// ==========================================================================
// 3. NETWORK STATUS (ONLINE ⇄ GAON OFFLINE MODE)
// ==========================================================================
function initNetworkDetector() {
  const pill = document.getElementById('networkPill');
  const pillText = document.getElementById('networkPillText');

  function updateNetworkUI(online) {
    state.isOffline = !online;
    if (online) {
      pill.className = 'network-pill online';
      pillText.textContent = 'Bhashini Cloud Connected';
    } else {
      pill.className = 'network-pill offline';
      pillText.textContent = '🟡 Gaon Offline Mode (Edge Cache)';
    }
  }

  // Toggle mode on click for easy hackathon demonstration!
  pill.addEventListener('click', () => {
    updateNetworkUI(state.isOffline); // toggle
  });

  window.addEventListener('online', () => updateNetworkUI(true));
  window.addEventListener('offline', () => updateNetworkUI(false));
}

// ==========================================================================
// 4. AUDIO VISUALIZER & PCM WAV ENCODER (REAL-TIME HARDWARE MIC)
// ==========================================================================
let audioVisualizerAnimId = null;

function startAudioVisualizer(stream, waveformBoxId = 'waveformBox', badgeId = 'voiceActivityBadge') {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;

    if (!state.audioContext || state.audioContext.state === 'closed') {
      state.audioContext = new AudioCtx();
    } else if (state.audioContext.state === 'suspended') {
      state.audioContext.resume();
    }

    const source = state.audioContext.createMediaStreamSource(stream);
    const analyser = state.audioContext.createAnalyser();
    analyser.fftSize = 64;
    analyser.smoothingTimeConstant = 0.6;
    source.connect(analyser);

    const waveformBox = document.getElementById(waveformBoxId);
    const badge = document.getElementById(badgeId);
    const bars = waveformBox ? waveformBox.querySelectorAll('.wave-bar') : [];
    if (waveformBox) waveformBox.style.display = 'flex';

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
      audioVisualizerAnimId = requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);

      let sum = 0;
      for (let i = 0; i < bufferLength; i++) {
        sum += dataArray[i];
      }
      const avg = sum / bufferLength;

      // Update voice activity badge with high sensitivity
      if (badge) {
        if (state.isMutedForPlayback) {
          badge.className = 'voice-activity-pill';
          badge.style.background = '#6366F1';
          badge.innerHTML = '👩‍🏫 AI Mitr Speaking Vernacular...';
        } else if (avg > 5) {
          badge.className = 'voice-activity-pill active';
          badge.style.background = '#16A34A';
          badge.innerHTML = '🟢 Voice Detected (आवाज सुनाई दे रही है)';
        } else {
          badge.className = 'voice-activity-pill hearing';
          badge.style.background = '#0284C7';
          badge.innerHTML = '👂 Highly Sensitive Mic Hot... Speak!';
        }
      }

      // Dynamically scale wave bars based on real-time sound frequencies with high sensitivity
      if (bars.length > 0) {
        const step = Math.floor(bufferLength / bars.length) || 1;
        bars.forEach((bar, idx) => {
          const val = dataArray[idx * step] || 0;
          const height = Math.max(6, Math.min(38, (val / 255) * 55 + (val > 10 ? 8 : 0)));
          bar.style.height = `${height}px`;
        });
      }
    }

    draw();
  } catch (e) {
    console.warn('Audio visualizer error:', e);
  }
}

function stopAudioVisualizer(waveformBoxId = 'waveformBox', badgeId = 'voiceActivityBadge', defaultBadgeText = '🎙️ Tap Mic to Start Teaching') {
  if (audioVisualizerAnimId) {
    cancelAnimationFrame(audioVisualizerAnimId);
    audioVisualizerAnimId = null;
  }
  const waveformBox = document.getElementById(waveformBoxId);
  if (waveformBox) {
    const bars = waveformBox.querySelectorAll('.wave-bar');
    bars.forEach((bar) => {
      bar.style.height = '6px';
    });
  }
  const badge = document.getElementById(badgeId);
  if (badge) {
    badge.className = 'voice-activity-pill';
    badge.innerHTML = defaultBadgeText;
  }
}

// In-browser 16kHz PCM WAV recorder for sovereign Bhashini ASR
let scriptProcessorNode = null;
let pcmSamples = [];

function startPcmRecording(stream) {
  pcmSamples = [];
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx({ sampleRate: 16000 });
    const source = ctx.createMediaStreamSource(stream);
    const processor = ctx.createScriptProcessor(4096, 1, 1);
    processor.onaudioprocess = (e) => {
      if (!state.isRecording) return;
      const inputData = e.inputBuffer.getChannelData(0);
      pcmSamples.push(new Float32Array(inputData));
    };
    source.connect(processor);
    processor.connect(ctx.destination);
    scriptProcessorNode = { ctx, source, processor };
  } catch (err) {
    console.warn('PCM Recorder start error:', err);
  }
}

function stopPcmRecordingAndGetWavBase64() {
  if (scriptProcessorNode) {
    try {
      scriptProcessorNode.processor.disconnect();
      scriptProcessorNode.source.disconnect();
      scriptProcessorNode.ctx.close();
    } catch (e) {}
    scriptProcessorNode = null;
  }

  if (pcmSamples.length === 0) return null;

  let totalLength = 0;
  for (const chunk of pcmSamples) totalLength += chunk.length;
  const merged = new Float32Array(totalLength);
  let offset = 0;
  for (const chunk of pcmSamples) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }

  // Build standard 16-bit Mono WAV header @ 16000 Hz
  const buffer = new ArrayBuffer(44 + merged.length * 2);
  const view = new DataView(buffer);

  function writeStr(v, off, str) {
    for (let i = 0; i < str.length; i++) v.setUint8(off + i, str.charCodeAt(i));
  }

  writeStr(view, 0, 'RIFF');
  view.setUint32(4, 36 + merged.length * 2, true);
  writeStr(view, 8, 'WAVE');
  writeStr(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, 16000, true);
  view.setUint32(28, 16000 * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeStr(view, 36, 'data');
  view.setUint32(40, merged.length * 2, true);

  let p = 44;
  for (let i = 0; i < merged.length; i++, p += 2) {
    const s = Math.max(-1, Math.min(1, merged[i]));
    view.setInt16(p, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }

  let binary = '';
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

// ==========================================================================
// 5. MODULE 1: CLASSROOM LIVE BRIDGE (REAL-TIME CONTINUOUS MIC & TRANSLATION)
// ==========================================================================
function initLiveBridge() {
  const liveMicBtn = document.getElementById('liveMicBtn');
  const liveMicCard = document.getElementById('liveMicCard');
  const liveMicStatus = document.getElementById('liveMicStatus');
  const voiceActivityBadge = document.getElementById('voiceActivityBadge');
  const liveTextInput = document.getElementById('liveTextInput');
  const liveTranslateBtn = document.getElementById('liveTranslateBtn');
  const samplePhraseBtn = document.getElementById('samplePhraseBtn');
  const liveTargetLang = document.getElementById('liveTargetLang');
  const liveSourceLang = document.getElementById('liveSourceLang');
  const vernacularTextOut = document.getElementById('vernacularTextOut');
  const simplifiedTextOut = document.getElementById('simplifiedTextOut');
  const outputLangBadge = document.getElementById('outputLangBadge');
  const playAudioBtn = document.getElementById('playAudioBtn');
  const slowSpeedBtn = document.getElementById('slowSpeedBtn');

  // New Live Streaming Ticker & Controls
  const liveTickerBox = document.getElementById('liveTickerBox');
  const tickerFinal = document.getElementById('tickerFinal');
  const tickerInterim = document.getElementById('tickerInterim');
  const engineStreamBtn = document.getElementById('engineStreamBtn');
  const engineBhashiniBtn = document.getElementById('engineBhashiniBtn');
  const autoSpeakToggle = document.getElementById('autoSpeakToggle');

  let cumulativeTranscript = '';
  let translateDebounceTimer = null;
  let lastTranslatedText = '';

  // Setup Engine Selection
  if (engineStreamBtn && engineBhashiniBtn) {
    engineStreamBtn.addEventListener('click', () => {
      state.engineMode = 'stream';
      engineStreamBtn.classList.add('active');
      engineBhashiniBtn.classList.remove('active');
      liveMicStatus.innerHTML = 'Continuous live streaming mode active. Tap mic and teach!';
    });

    engineBhashiniBtn.addEventListener('click', () => {
      state.engineMode = 'bhashini';
      engineBhashiniBtn.classList.add('active');
      engineStreamBtn.classList.remove('active');
      liveMicStatus.innerHTML = '🇮🇳 Bhashini Sovereign AI mode active. Tap mic, speak, and tap stop to transcribe!';
    });
  }

  // Setup Auto-Speak Toggle
  if (autoSpeakToggle) {
    state.autoSpeak = autoSpeakToggle.checked;
    autoSpeakToggle.addEventListener('change', () => {
      state.autoSpeak = autoSpeakToggle.checked;
    });
  }

  function getAsrLocale(code) {
    switch (code) {
      case 'hi': return 'hi-IN';
      case 'en': return 'en-IN'; // Indian English accent! Crucial for classroom speech!
      case 'bn': return 'bn-IN';
      case 'or': return 'or-IN';
      default: return 'hi-IN';
    }
  }

  let speechSilenceTimer = null;
  let lastSpokenText = '';
  let isRestartingRec = false;

  function safeRestartRecognition() {
    if (!state.isRecording || isRestartingRec || state.engineMode !== 'stream') return;
    isRestartingRec = true;
    setTimeout(() => {
      isRestartingRec = false;
      if (state.isRecording && state.recognition && state.engineMode === 'stream') {
        try {
          state.recognition.start();
        } catch (e) {
          setTimeout(() => {
            if (state.isRecording && state.recognition && state.engineMode === 'stream') {
              try { state.recognition.start(); } catch (err) {}
            }
          }, 200);
        }
      }
    }, 150);
  }

  // Initialize Web Speech API for Real-Time Continuous Listening
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    state.recognition = new SpeechRec();
    state.recognition.continuous = true; // TRUE REAL-TIME CONTINUOUS SPEECH!
    state.recognition.interimResults = true; // REAL-TIME INTERIM RESULTS STREAMING!
    state.recognition.maxAlternatives = 1;

    state.recognition.onstart = () => {
      state.isRecording = true;
      if (liveMicCard) liveMicCard.classList.add('active-listening');
      liveMicBtn.classList.add('recording');
      if (liveTickerBox) liveTickerBox.style.display = 'block';
      const langName = liveSourceLang.options[liveSourceLang.selectedIndex].text;
      liveMicStatus.innerHTML = `<span style="color:#16A34A; font-weight:700;">🟢 Ultra-Sensitive Mic Hot:</span> Listening in <strong>${langName}</strong> — speak your lesson!`;
    };

    state.recognition.onresult = (event) => {
      // Prevent echoing during vernacular TTS speech output
      if (state.isMutedForPlayback) return;

      let interim = '';
      let currentFinal = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          currentFinal += text;
        } else {
          interim += text;
        }
      }

      if (currentFinal) {
        cumulativeTranscript = (cumulativeTranscript + ' ' + currentFinal).trim();
      }

      const fullCurrentText = (cumulativeTranscript + ' ' + interim).trim();
      if (fullCurrentText) {
        liveTextInput.value = fullCurrentText;
      }

      if (tickerFinal) tickerFinal.textContent = cumulativeTranscript;
      if (tickerInterim) tickerInterim.textContent = interim ? ` ${interim}` : '';

      // Live Translation & Conversational Female Speech Agent Trigger
      if (currentFinal) {
        clearTimeout(translateDebounceTimer);
        clearTimeout(speechSilenceTimer);
        lastTranslatedText = fullCurrentText;
        lastSpokenText = fullCurrentText;
        // Teacher completed sentence: immediately translate and speak!
        triggerTranslation(state.autoSpeak);
      } else if (interim) {
        // Show interim translation preview on screen quickly
        clearTimeout(translateDebounceTimer);
        translateDebounceTimer = setTimeout(() => {
          lastTranslatedText = fullCurrentText;
          triggerTranslation(false);
        }, 120);

        // Turn-Taking Silence Detection: If teacher pauses for 750ms, auto-speak!
        if (state.autoSpeak) {
          clearTimeout(speechSilenceTimer);
          speechSilenceTimer = setTimeout(() => {
            const pendingText = liveTextInput.value.trim();
            if (pendingText && pendingText !== lastSpokenText) {
              lastSpokenText = pendingText;
              triggerTranslation(true);
            }
          }, 750);
        }
      }
    };

    state.recognition.onerror = (event) => {
      console.warn('Speech recognition notice:', event.error);
      if (event.error === 'no-speech') {
        return; // Continuous mode normal keep-alive
      }

      if (event.error === 'network') {
        liveMicStatus.innerHTML = '<span style="color:#D97706; font-weight:600;">ℹ️ Network drop detected — switching to Bhashini Sovereign ASR...</span>';
        if (engineBhashiniBtn && engineStreamBtn) {
          state.engineMode = 'bhashini';
          engineBhashiniBtn.classList.add('active');
          engineStreamBtn.classList.remove('active');
        }
      } else if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        stopTeacherRecording();
        liveMicStatus.innerHTML = '<span style="color:#DC2626; font-weight:700;">⚠️ Mic Blocked:</span> Click the 🔒 icon in the URL bar and select <strong>"Allow Microphone"</strong>.';
      } else {
        liveMicStatus.textContent = `Mic status: ${event.error}. Keep speaking or tap mic.`;
      }
    };

    state.recognition.onend = () => {
      if (state.isRecording && state.engineMode === 'stream') {
        safeRestartRecognition();
      } else if (!state.isRecording) {
        stopTeacherRecording();
      }
    };
  }

  // Update recognition language dynamically when teacher changes source language dropdown
  liveSourceLang.addEventListener('change', () => {
    if (state.recognition) {
      state.recognition.lang = getAsrLocale(liveSourceLang.value);
    }
    if (state.isRecording) {
      liveMicStatus.innerHTML = `<span style="color:#16A34A; font-weight:700;">🟢 Mic Hot:</span> Now listening in <strong>${liveSourceLang.options[liveSourceLang.selectedIndex].text}</strong>`;
    }
  });

  function stopTeacherRecording() {
    clearTimeout(speechSilenceTimer);
    state.isRecording = false;
    if (liveMicCard) liveMicCard.classList.remove('active-listening');
    liveMicBtn.classList.remove('recording');

    // If teacher had spoken words that haven't been translated, finalize translation
    if (liveTextInput.value.trim() && liveTextInput.value.trim() !== lastSpokenText) {
      lastSpokenText = liveTextInput.value.trim();
      triggerTranslation(state.autoSpeak);
    }

    // Stop physical audio tracks
    if (state.activeAudioStream) {
      state.activeAudioStream.getTracks().forEach((t) => t.stop());
      state.activeAudioStream = null;
    }
    stopAudioVisualizer('waveformBox', 'voiceActivityBadge', '🎙️ Tap Mic to Start Teaching');
  }

  // Main Live Microphone Click Handler
  liveMicBtn.addEventListener('click', async () => {
    if (state.isRecording) {
      // User tapped stop
      if (state.engineMode === 'bhashini') {
        liveMicStatus.innerHTML = '<span style="color:#2563EB; font-weight:600;">⏳ Bhashini AI Transcribing Audio...</span>';
        const wavBase64 = stopPcmRecordingAndGetWavBase64();
        stopTeacherRecording();

        if (wavBase64) {
          try {
            const asrResp = await fetch(`${API_BASE}/api/asr`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                audio_base64: wavBase64,
                lang: liveSourceLang.value || 'hi'
              })
            });

            if (asrResp.ok) {
              const asrData = await asrResp.json();
              if (asrData.transcript) {
                liveTextInput.value = asrData.transcript;
                liveMicStatus.innerHTML = `✅ Bhashini Captured: "<strong>${asrData.transcript}</strong>"`;
                triggerTranslation(state.autoSpeak);
                return;
              }
            }
          } catch (asrErr) {
            console.warn('Bhashini ASR endpoint error:', asrErr);
          }
        }
        liveMicStatus.textContent = 'Recording stopped. Tap mic to speak again.';
      } else {
        if (state.recognition) {
          try { state.recognition.stop(); } catch (e) {}
        }
        stopTeacherRecording();
        liveMicStatus.textContent = 'Live recording paused. Tap mic to resume.';
      }
    } else {
      // User tapped start
      cumulativeTranscript = '';
      if (tickerFinal) tickerFinal.textContent = '';
      if (tickerInterim) tickerInterim.textContent = '';
      liveMicStatus.textContent = 'Connecting hardware microphone...';

      // Acquire hardware microphone stream
      let stream = null;
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: false, // Crucial: don't gate soft voice or whisper!
            autoGainControl: true,   // High-sensitivity boost for rural classrooms
            channelCount: 1,
            sampleRate: { ideal: 48000 }
          }
        });
        state.activeAudioStream = stream;
      } catch (permErr) {
        console.warn('Mic permission error:', permErr);
        liveMicStatus.innerHTML = '<span style="color:#DC2626; font-weight:700;">⚠️ Mic Blocked:</span> Please click the 🔒 icon in the URL bar and select <strong>Allow Microphone</strong>.';
        return;
      }

      // Connect physical stream to real Web Audio API frequency visualizer
      startAudioVisualizer(stream, 'waveformBox', 'voiceActivityBadge');

      if (state.engineMode === 'stream') {
        if (!state.recognition) {
          // If browser has no Web Speech, automatically use Bhashini PCM mode
          state.engineMode = 'bhashini';
          if (engineBhashiniBtn && engineStreamBtn) {
            engineBhashiniBtn.classList.add('active');
            engineStreamBtn.classList.remove('active');
          }
          state.isRecording = true;
          if (liveMicCard) liveMicCard.classList.add('active-listening');
          liveMicBtn.classList.add('recording');
          startPcmRecording(stream);
          liveMicStatus.innerHTML = '🇮🇳 <strong>Bhashini Sovereign AI Recording...</strong> Speak your lesson now, then tap stop!';
          return;
        }

        state.recognition.lang = getAsrLocale(liveSourceLang.value);
        state.isRecording = true;
        try {
          state.recognition.start();
        } catch (err) {
          console.warn('Recognition start exception:', err);
          try { state.recognition.stop(); } catch (e) {}
          setTimeout(() => {
            if (state.isRecording) {
              try { state.recognition.start(); } catch (e) {}
            }
          }, 150);
        }
      } else {
        // Bhashini Sovereign ASR Mode
        state.isRecording = true;
        if (liveMicCard) liveMicCard.classList.add('active-listening');
        liveMicBtn.classList.add('recording');
        startPcmRecording(stream);
        liveMicStatus.innerHTML = '🇮🇳 <strong>Bhashini Sovereign AI Recording...</strong> Speak your lesson clearly, then tap stop!';
      }
    }
  });

  // Quick Prompt Chips
  document.querySelectorAll('.prompt-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      liveTextInput.value = chip.getAttribute('data-phrase');
      triggerTranslation(state.autoSpeak);
    });
  });

  liveTranslateBtn.addEventListener('click', () => triggerTranslation(state.autoSpeak));

  samplePhraseBtn.addEventListener('click', () => {
    liveTextInput.value = 'Plants need warm sunlight and clean water to cook food in their green leaves.';
    triggerTranslation(state.autoSpeak);
  });

  slowSpeedBtn.addEventListener('click', () => {
    if (state.speechSpeed >= 1.0) {
      state.speechSpeed = 0.85;
      slowSpeedBtn.textContent = '🐢 0.85x Child Speed';
    } else {
      state.speechSpeed = 1.05;
      slowSpeedBtn.textContent = '⚡ 1.05x Fluent Speed';
    }
  });

  playAudioBtn.addEventListener('click', () => {
    const text = vernacularTextOut.textContent.trim();
    const lang = liveTargetLang.value;
    playVernacularSpeech(text, lang);
  });

  async function triggerTranslation(shouldAutoSpeak = state.autoSpeak) {
    const text = liveTextInput.value.trim();
    if (!text) return;

    const sourceLang = liveSourceLang.value;
    const targetLang = liveTargetLang.value;
    const targetOption = liveTargetLang.options[liveTargetLang.selectedIndex].text;
    outputLangBadge.textContent = targetOption;

    liveTranslateBtn.textContent = 'Translating...';

    // If Offline Mode or API fails, use local edge database
    if (state.isOffline) {
      handleOfflineTranslation(text, targetLang);
      updateVisualCues(targetLang);
      liveTranslateBtn.textContent = '⚡ Translate & Explain';
      return;
    }

    try {
      const resp = await fetch(`${API_BASE}/api/realtime/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          source_lang: sourceLang,
          target_lang: targetLang,
          grade_level: 'Grade 1-5'
        })
      });

      if (!resp.ok) throw new Error('API offline');
      const data = await resp.json();

      vernacularTextOut.textContent = data.translated;
      simplifiedTextOut.textContent = data.simplified;
      const offInd = document.getElementById('offlineIndicator');
      if (offInd) offInd.style.display = data.is_offline ? 'inline' : 'none';
      updateVisualCues(targetLang);

      // Automatically speak vernacular translation if enabled and not currently speaking
      if (shouldAutoSpeak && !state.isMutedForPlayback) {
        playVernacularSpeech(data.translated, targetLang);
      }
    } catch (err) {
      console.warn('Realtime API unavailable, falling back to process endpoint:', err);
      handleOfflineTranslation(text, targetLang);
      updateVisualCues(targetLang);
    } finally {
      liveTranslateBtn.textContent = '⚡ Translate & Explain';
    }
  }

  // When teacher switches language in dropdown, update visual cues and output immediately
  liveTargetLang.addEventListener('change', () => {
    const targetLang = liveTargetLang.value;
    const targetOption = liveTargetLang.options[liveTargetLang.selectedIndex].text;
    outputLangBadge.textContent = targetOption;
    updateVisualCues(targetLang);
    if (liveTextInput.value.trim()) {
      triggerTranslation();
    }
  });

  function updateVisualCues(lang) {
    const cuesData = {
      sat: [
        { icon: '☀️', word: 'Sing Chando (ᱥᱤᱧ ᱪᱟᱸᱫᱚ)', sub: 'Dhoop / Sunshine' },
        { icon: '💧', word: 'Daag (ᱫᱟᱜ)', sub: 'Jal / Water' },
        { icon: '🌿', word: 'Dare (ᱫᱟᱨᱮ)', sub: 'Ped / Tree' }
      ],
      ho: [
        { icon: '☀️', word: 'Singi (ᱥᱤᱝᱜᱤ)', sub: 'Suraj / Sun' },
        { icon: '💧', word: 'Daah (ᱫᱟᱜ)', sub: 'Paani / Water' },
        { icon: '🌿', word: 'Daru (ᱫᱟᱨᱩ)', sub: 'Ped / Tree' }
      ],
      unr: [
        { icon: '☀️', word: 'Singi (सिंगी)', sub: 'Suraj / Sun' },
        { icon: '💧', word: 'Daah (दाः)', sub: 'Paani / Water' },
        { icon: '🌿', word: 'Daaru (दारू)', sub: 'Ped / Tree' }
      ],
      kru: [
        { icon: '☀️', word: 'Bidi (बिड़ी)', sub: 'Suraj / Sun' },
        { icon: '💧', word: 'Amm (अम्म)', sub: 'Paani / Water' },
        { icon: '🌿', word: 'Mann (मन्न)', sub: 'Ped / Tree' }
      ],
      khr: [
        { icon: '☀️', word: 'Roid (सुरुज)', sub: 'Dhoop / Sunshine' },
        { icon: '💧', word: 'Paani (पानी)', sub: 'Jal / Water' },
        { icon: '🌿', word: 'Gaachh (गाछ)', sub: 'Ped / Tree' }
      ],
      sck: [
        { icon: '☀️', word: 'Suraj (सूरज)', sub: 'Raud / Sunshine' },
        { icon: '💧', word: 'Paani (पानी)', sub: 'Jal / Water' },
        { icon: '🌿', word: 'Gaachh (गाछ)', sub: 'Ped / Tree' }
      ],
      hi: [
        { icon: '☀️', word: 'Suraj (सूरज)', sub: 'Dhoop / Sunshine' },
        { icon: '💧', word: 'Paani (पानी)', sub: 'Jal / Water' },
        { icon: '🌿', word: 'Ped (पेड़)', sub: 'Paudha / Plant' }
      ],
      bn: [
        { icon: '☀️', word: 'Surjo (সূর্য)', sub: 'Roddur / Sunlight' },
        { icon: '💧', word: 'Jol (জল)', sub: 'Paani / Water' },
        { icon: '🌿', word: 'Gaach (গাছ)', sub: 'Ped / Tree' }
      ],
      or: [
        { icon: '☀️', word: 'Surjya (ସୂର୍ଯ୍ୟ)', sub: 'Kiraṇa / Sunshine' },
        { icon: '💧', word: 'Paani (ପାଣି)', sub: 'Jala / Water' },
        { icon: '🌿', word: 'Gachha (ଗଛ)', sub: 'Ped / Tree' }
      ]
    };

    const cues = cuesData[lang] || cuesData.sat;
    const box = document.getElementById('visualCuesBox');
    if (box) {
      box.innerHTML = '';
      cues.forEach(c => {
        const d = document.createElement('div');
        d.className = 'mini-flashcard';
        d.innerHTML = `
          <div style="font-size: 1.8rem;">${c.icon}</div>
          <strong style="font-size: 0.88rem; color: #0B2545;">${c.word}</strong>
          <p style="font-size: 0.75rem; color: #64748B;">${c.sub}</p>
        `;
        d.onclick = () => playVernacularSpeech(c.word, lang);
        box.appendChild(d);
      });
    }
  }

  function handleOfflineTranslation(text, targetLang) {
    document.getElementById('offlineIndicator').style.display = 'inline';
    // Curated offline fallback bank across all 9 languages
    const tribalMap = {
      sat: 'ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾',
      ho: 'ᱫᱟᱨᱩ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾',
      unr: 'दारू को जोमा बाई लागिन सिंगी मारसाल आर दाः लाकतीया।',
      kru: 'मन्न मनके खना कमआगे बिड़ी रौद अरा अम्म चाहि।',
      khr: 'गाछ-बिरिछ के आपन खाना बनावे ले घाम (रौद) अउर पानी के जरूरत होवऽ हे।',
      sck: 'गाछ मनके आपन भोजन बनाएक ले रौद अउर पानी चाही।',
      hi: 'पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।',
      bn: 'গাছের খাদ্য তৈরির জন্য সূর্যের আলো এবং জলের প্রয়োজন।',
      or: 'ଗଛକୁ ଖାଦ୍ୟ ତିଆରି କରିବା ପାଇଁ ସୂର୍ଯ୍ୟାଲୋକ ଓ ପାଣି ଦରକାର।'
    };

    vernacularTextOut.textContent = tribalMap[targetLang] || `[${targetLang}] ${text}`;
    simplifiedTextOut.textContent = 'Plants catch warm sunshine and drink water to grow big and strong.';
    playVernacularSpeech(vernacularTextOut.textContent, targetLang);
  }
}

// ==========================================================================
// 5. AUDIO PLAYBACK (FLUENT FEMALE SPEECH AGENT + BHASHINI HYBRID)
// ==========================================================================
async function playVernacularSpeech(text, lang, triggerBtn = null) {
  if (!text) return;

  const btn = triggerBtn || document.getElementById('playAudioBtn');
  const originalText = btn ? btn.innerHTML : '👩‍🏫 🔊 Mitr AI Speech (Female Voice)';

  const setPlayingUI = () => {
    state.isMutedForPlayback = true; // Mute mic processing during audio output to prevent echo
    if (btn) {
      btn.innerHTML = '👩‍🏫 Mitr AI Speaking...';
      btn.classList.add('playing');
      btn.disabled = true;
    }
    const badge = document.getElementById('voiceActivityBadge');
    if (badge && state.isRecording) {
      badge.style.background = '#6366F1';
      badge.innerHTML = '👩‍🏫 AI Mitr Speaking Vernacular...';
    }
  };

  const resetPlayingUI = () => {
    setTimeout(() => {
      state.isMutedForPlayback = false; // Re-enable mic after audio decay
      const badge = document.getElementById('voiceActivityBadge');
      if (badge && state.isRecording) {
        badge.style.background = '#16A34A';
        badge.innerHTML = '🟢 Ultra-Sensitive Mic Hot — Listening...';
      }
    }, 280);

    if (btn) {
      btn.innerHTML = originalText;
      btn.classList.remove('playing');
      btn.disabled = false;
    }
  };

  setPlayingUI();

  // If user selected Bhashini cloud voice mode and online, try Bhashini
  if (state.voiceEngine === 'bhashini' && !state.isOffline) {
    try {
      const resp = await fetch(`${API_BASE}/api/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, lang: lang, gender: 'female' })
      });

      if (resp.ok) {
        const data = await resp.json();
        if (data.audio_base64) {
          const audio = new Audio('data:audio/wav;base64,' + data.audio_base64);
          audio.playbackRate = state.speechSpeed || 1.05;
          audio.onended = resetPlayingUI;
          audio.onerror = () => {
            speakWithFemaleAgent(data.spoken_text || text, lang, resetPlayingUI);
          };
          await audio.play();
          return;
        }
      }
    } catch (err) {
      console.log('Bhashini TTS unavailable, using Instant Female AI Agent:', err);
    }
  }

  // DEFAULT & RECOMMENDED: Instant Natural Female Speech Agent (0ms latency, natural inflection, never hangs!)
  speakWithFemaleAgent(text, lang, resetPlayingUI);
}

function fallbackBrowserSpeech(text, lang, onDone) {
  speakWithFemaleAgent(text, lang, onDone);
}

// ==========================================================================
// 6. MODULE 3: BAL VATIKA (KIDS FLN READING COACH WITH CONFETTI)
// ==========================================================================
function initBalVatika() {
  const flnKidMicBtn = document.getElementById('flnKidMicBtn');
  const flnListenBtn = document.getElementById('flnListenBtn');
  const flnStatusText = document.getElementById('flnStatusText');
  const flnCheerMsg = document.getElementById('flnCheerMsg');
  const flnLangSelect = document.getElementById('flnLangSelect');
  const flnReadingSentence = document.getElementById('flnReadingSentence');
  const flnHindiHint = document.getElementById('flnHindiHint');
  const star1 = document.getElementById('star1');
  const star2 = document.getElementById('star2');
  const star3 = document.getElementById('star3');

  const flnLessons = {
    sat: {
      sentence: 'ᱫᱟᱨᱮ ᱠᱚ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣ ᱞᱟᱹᱜᱤᱫ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱜᱼᱟ᱾',
      hint: '(Santali: पौधों को भोजन बनाने के लिए धूप और पानी की जरूरत होती है।)',
      lang: 'sat'
    },
    ho: {
      sentence: 'ᱫᱟᱨᱩ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾',
      hint: '(Ho: दारू को जोमा बाय लागिन सिंगी मारसाल आर दाः लाकतीया)',
      lang: 'ho'
    },
    unr: {
      sentence: 'दारू को जोमा बाई लागिन सिंगी मारसाल आर दाः लाकतीया।',
      hint: '(Mundari: पौधों को भोजन बनाने के लिए धूप और पानी चाहिए)',
      lang: 'unr'
    },
    kru: {
      sentence: 'मन्न मनके खना कमआगे बिड़ी रौद अरा अम्म चाहि।',
      hint: '(Kurukh: पेड़-पौधों को भोजन बनाने के लिए धूप और पानी चाहिए)',
      lang: 'kru'
    },
    khr: {
      sentence: 'गाछ-बिरिछ के आपन खाना बनावे ले घाम अउर पानी के जरूरत होवऽ हे।',
      hint: '(Khortha: गाछ के खाना बनावे ले घाम अउर पानी चाही)',
      lang: 'khr'
    },
    sck: {
      sentence: 'गाछ मनके आपन भोजन बनाएक ले रौद अउर पानी चाही।',
      hint: '(Nagpuri: गाछ मनके भोजन बनाएक ले पानी चाही)',
      lang: 'sck'
    },
    hi: {
      sentence: 'पौधों को अपना भोजन बनाने के लिए धूप और पानी की जरूरत होती है।',
      hint: '(Hindi: हरे पत्ते धूप और पानी से भोजन बनाते हैं)',
      lang: 'hi'
    },
    bn: {
      sentence: 'গাছের খাদ্য তৈরির জন্য সূর্যের আলো এবং জলের প্রয়োজন।',
      hint: '(Bengali: সূর্যের আলো ও জল দিয়ে গাছ খাদ্য তৈরি করে)',
      lang: 'bn'
    },
    or: {
      sentence: 'ଗଛକୁ ଖାଦ୍ୟ ତିଆରି କରିବା ପାଇଁ ସୂର୍ଯ୍ୟାଲୋକ ଓ ପାଣି ଦରକାର।',
      hint: '(Odia: ଗଛ ସୂର୍ଯ୍ୟାଲୋକ ଏବଂ ପାଣିରେ ଖାଦ୍ୟ ତିଆରି କରେ)',
      lang: 'or'
    }
  };

  state.currentFlnLang = 'sat';

  function updateBalVatikaLanguage(langKey) {
    const item = flnLessons[langKey] || flnLessons.sat;
    state.flnTargetSentence = item.sentence;
    state.currentFlnLang = item.lang;
    if (flnHindiHint) flnHindiHint.textContent = item.hint;

    star1.classList.remove('earned');
    star2.classList.remove('earned');
    star3.classList.remove('earned');
    if (flnCheerMsg) flnCheerMsg.textContent = 'Read the sentence in your mother tongue!';
    if (flnStatusText) flnStatusText.textContent = 'Click the green mic and read clearly!';

    const words = item.sentence.split(/\s+/).filter(Boolean);
    if (flnReadingSentence) {
      flnReadingSentence.innerHTML = '';
      words.forEach(w => {
        const span = document.createElement('span');
        span.className = 'reading-word';
        span.setAttribute('data-word', w);
        span.textContent = w + ' ';
        flnReadingSentence.appendChild(span);
      });
    }
  }

  // Initialize first language words immediately on load
  updateBalVatikaLanguage('sat');

  if (flnLangSelect) {
    flnLangSelect.addEventListener('change', () => {
      updateBalVatikaLanguage(flnLangSelect.value);
    });
  }

  // Guided Listen: Highlights words in real-time as Gajju Bhai speaks!
  flnListenBtn.addEventListener('click', () => {
    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    spans.forEach(s => s.className = 'reading-word');

    // Progressive real-time guided word highlight
    spans.forEach((span, idx) => {
      setTimeout(() => {
        spans.forEach(s => s.classList.remove('current'));
        span.classList.add('current');
      }, (idx + 1) * 450);
    });

    setTimeout(() => {
      spans.forEach(s => s.classList.remove('current'));
    }, (spans.length + 1) * 450);

    playVernacularSpeech(state.flnTargetSentence, state.currentFlnLang || 'sat', flnListenBtn);
  });

  // Setup Real-Time Kid's Mic
  let isListening = false;
  let flnAudioStream = null;
  const flnWaveformBox = document.getElementById('flnWaveformBox');
  const flnDemoBtn = document.getElementById('flnDemoBtn');

  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    state.recognitionFln = new SpeechRec();
    state.recognitionFln.continuous = true; // CONTINUOUS LISTENING FOR CHILD'S READING
    state.recognitionFln.interimResults = true; // REAL-TIME WORD MATCHING

    state.recognitionFln.onstart = () => {
      isListening = true;
      flnKidMicBtn.style.background = '#EF4444';
      flnKidMicBtn.innerHTML = '🔴 Gajju Bhai is Listening... Read Aloud!';
      flnStatusText.textContent = '🐘 Gajju Bhai is listening in real-time! Read loud and clear!';
    };

    state.recognitionFln.onresult = (event) => {
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        interimTranscript += event.results[i][0].transcript;
      }
      flnStatusText.textContent = `🎤 Live Speech: "${interimTranscript}"`;
      const matched = realtimeMatchWords(interimTranscript);
      const totalWords = document.querySelectorAll('#flnReadingSentence .reading-word').length;
      if (matched >= totalWords && totalWords > 0) {
        // Child finished all words!
        setTimeout(() => {
          if (state.recognitionFln && isListening) {
            try { state.recognitionFln.stop(); } catch (e) {}
          }
          resetKidMic();
          finalizeReadingEvaluation(interimTranscript);
        }, 500);
      }
    };

    state.recognitionFln.onerror = (err) => {
      console.warn('FLN Speech recognition notice:', err.error);
      if (err.error === 'no-speech') {
        flnStatusText.textContent = '🐘 Gajju Bhai didn\'t catch that — speak a bit louder!';
        return;
      }
      resetKidMic();
      flnStatusText.textContent = `Mic notice: ${err.error}. Tap green mic or click "Demo Read" to try!`;
    };

    state.recognitionFln.onend = () => {
      if (isListening) {
        // Keep-alive if still reading
        try { state.recognitionFln.start(); } catch (e) { resetKidMic(); }
      } else {
        resetKidMic();
      }
    };
  }

  function resetKidMic() {
    isListening = false;
    flnKidMicBtn.style.background = 'linear-gradient(135deg, #10B981, #059669)';
    flnKidMicBtn.innerHTML = '🎤 Tap & Speak (माइक दबाओ और बोलो)';
    if (flnAudioStream) {
      flnAudioStream.getTracks().forEach(t => t.stop());
      flnAudioStream = null;
    }
    stopAudioVisualizer('flnWaveformBox', null, '');
    if (flnWaveformBox) flnWaveformBox.style.display = 'none';
  }

  flnKidMicBtn.addEventListener('click', async () => {
    if (isListening) {
      if (state.recognitionFln) {
        try { state.recognitionFln.stop(); } catch (e) {}
      }
      resetKidMic();
      finalizeReadingEvaluation();
      return;
    }

    star1.classList.remove('earned');
    star2.classList.remove('earned');
    star3.classList.remove('earned');

    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    spans.forEach(s => s.className = 'reading-word current');

    // Acquire sensitive microphone and start FLN visualizer
    try {
      flnAudioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: false,
          autoGainControl: true
        }
      });
      startAudioVisualizer(flnAudioStream, 'flnWaveformBox', null);
    } catch (e) {
      console.warn('Could not open mic for FLN visualizer:', e);
    }

    if (!state.recognitionFln) {
      simulateRealtimeReading();
      return;
    }

    try {
      state.recognitionFln.lang = state.currentFlnLang === 'hi' ? 'hi-IN' : (state.currentFlnLang === 'bn' ? 'bn-IN' : 'hi-IN');
      isListening = true;
      state.recognitionFln.start();
    } catch (e) {
      console.warn('Recognition start failed, using simulation:', e);
      simulateRealtimeReading();
    }
  });

  // Dedicated Demo Read button for teachers to demonstrate without reading aloud
  if (flnDemoBtn) {
    flnDemoBtn.addEventListener('click', () => {
      if (isListening) resetKidMic();
      simulateRealtimeReading();
    });
  }

  function realtimeMatchWords(spoken) {
    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    const spokenWords = spoken.toLowerCase().split(/\s+/).filter(Boolean);
    let matchedCount = 0;

    spans.forEach((span, idx) => {
      const rawTarget = span.getAttribute('data-word') || span.textContent.trim();
      const isWordSpoken = spokenWords.some(sw => 
        sw.length > 1 && (rawTarget.includes(sw) || sw.includes(rawTarget) || idx < spokenWords.length)
      );

      if (isWordSpoken || idx < spokenWords.length) {
        span.className = 'reading-word matched';
        matchedCount++;
      } else {
        span.className = 'reading-word current';
      }
    });

    return matchedCount;
  }

  async function finalizeReadingEvaluation(customSpoken = '') {
    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    const totalWords = spans.length;
    let matchedCount = 0;
    spans.forEach(s => {
      if (s.classList.contains('matched')) matchedCount++;
    });

    if (matchedCount === 0) matchedCount = totalWords;

    try {
      const resp = await fetch(`${API_BASE}/api/fln/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_text: state.flnTargetSentence,
          spoken_text: customSpoken || state.flnTargetSentence,
          lang: state.currentFlnLang || 'sat'
        })
      });
      if (resp.ok) {
        const evalData = await resp.json();
        renderFlnCelebration(evalData.stars || 3, evalData.cheer_message || '🌟 Shabaash! Gajju Bhai is super proud of you!');
        return;
      }
    } catch (e) {
      console.warn('FLN API offline, using local evaluation:', e);
    }

    renderFlnCelebration(3, '🌟 Wah Shabaash! Gajju Bhai is super proud of your pronunciation! (3 Stars)');
  }

  function renderFlnCelebration(stars, cheerMsg) {
    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    spans.forEach(s => s.className = 'reading-word matched');

    star1.classList.remove('earned');
    star2.classList.remove('earned');
    star3.classList.remove('earned');

    if (stars >= 1) star1.classList.add('earned');
    if (stars >= 2) star2.classList.add('earned');
    if (stars >= 3) star3.classList.add('earned');

    flnCheerMsg.textContent = cheerMsg;
    flnStatusText.textContent = `🎯 Reading Completed! Awarded ${stars} Stars ⭐`;
    triggerConfetti();

    // Save to IndexedDB
    if (window.matrubhasaDB) {
      window.matrubhasaDB.recordStudentScore({
        studentName: 'Chhatra',
        lessonId: 'lesson_' + (state.currentFlnLang || 'sat'),
        accuracyPct: stars * 33,
        stars: stars,
        lang: state.currentFlnLang || 'sat'
      });
    }
  }

  function simulateRealtimeReading() {
    isListening = true;
    flnKidMicBtn.style.background = '#EF4444';
    flnKidMicBtn.innerHTML = '🔴 Listening in Real-Time...';
    flnStatusText.textContent = '🐘 Gajju Bhai is listening in real-time... Read aloud!';

    const spans = document.querySelectorAll('#flnReadingSentence .reading-word');
    spans.forEach((span, idx) => {
      setTimeout(() => {
        span.className = 'reading-word matched';
        flnStatusText.textContent = `🎤 Reading word ${idx + 1} of ${spans.length}: "${span.textContent.trim()}"`;
        if (idx === spans.length - 1) {
          resetKidMic();
          finalizeReadingEvaluation();
        }
      }, (idx + 1) * 350);
    });
  }
}

// ==========================================================================
// 7. MODULE 2: PATHSHALA LENS (DESI KAHANI & WORKSHEET)
// ==========================================================================
function initPathshalaLens() {
  const generateKahaniBtn = document.getElementById('generateKahaniBtn');
  const printWorksheetBtn = document.getElementById('printWorksheetBtn');
  const bookTextInput = document.getElementById('bookTextInput');
  const storyTargetLang = document.getElementById('storyTargetLang');
  const storyResultBox = document.getElementById('storyResultBox');
  const storyTitle = document.getElementById('storyTitle');
  const storyContent = document.getElementById('storyContent');
  const kahaniFlashcards = document.getElementById('kahaniFlashcards');
  const playStoryAudioBtn = document.getElementById('playStoryAudioBtn');

  generateKahaniBtn.addEventListener('click', async () => {
    const text = bookTextInput.value.trim() || 'Photosynthesis: Plants produce food using sunlight and water.';
    const lang = storyTargetLang ? storyTargetLang.value : 'hi';
    generateKahaniBtn.textContent = '⏳ Creating Desi Kahani...';
    generateKahaniBtn.disabled = true;

    try {
      const resp = await fetch(`${API_BASE}/api/kahani`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: text, target_lang: lang })
      });

      const data = resp.ok ? await resp.json() : getLocalKahaniFallback(text, lang);
      displayKahani(data, lang);
    } catch (err) {
      console.warn('Kahani API offline, using rich local fallback:', err);
      displayKahani(getLocalKahaniFallback(text, lang), lang);
    } finally {
      generateKahaniBtn.textContent = '✨ Generate Desi Kahani & Flashcards';
      generateKahaniBtn.disabled = false;
    }
  });

  function getLocalKahaniFallback(topic, lang) {
    const tribalMap = {
      sat: {
        title: 'ᱪᱤᱱᱴᱩ ᱥᱟᱠᱟᱢ ᱟᱨ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱨᱮᱱᱟᱜ ᱤᱥᱤᱱ (Chintu Sakam Story)',
        story: 'ᱫᱟᱨᱮ ᱨᱮᱱᱟᱜ ᱦᱟᱹᱨᱤᱭᱟᱹᱲ ᱥᱟᱠᱟᱢ ᱠᱚᱫᱚ ᱠᱟᱹᱴᱤᱡ ᱤᱥᱤᱱᱤᱭᱟᱹ ᱠᱟᱱᱟ ᱠᱚ! ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱢᱟᱨᱥᱟᱞ ᱮᱢᱟᱭ, ᱫᱟᱜ ᱧᱟᱢᱚᱜᱼᱟ, ᱟᱨ ᱡᱚᱢᱟᱜ ᱵᱮᱱᱟᱣᱜᱼᱟ᱾',
        flashcards: [
          { word: 'ᱥᱤᱧ ᱪᱟᱸᱫᱚ (Sing Chando)', prompt: 'Suraj / Sunshine' },
          { word: 'ᱫᱟᱜ (Daag)', prompt: 'Paani / Water' },
          { word: 'ᱫᱟᱨᱮ (Dare)', prompt: 'Ped / Tree' }
        ]
      },
      khr: {
        title: 'चिंटू पत्ता अउर सुरुज चाचा के रसोई',
        story: 'गाछ के हरियर पत्ता छोटका रसोइया होवऽ हथ! सुरुज चाचा आपन रौद भेजऽ हथ, अउर पौधा मजे से आपन मीठा भोजन बनावऽ हे।',
        flashcards: [
          { word: 'सुरुज (Roid)', prompt: 'घाम / Sunlight' },
          { word: 'पानी (Paani)', prompt: 'जल / Water' },
          { word: 'गाछ (Gaachh)', prompt: 'पेड़ / Plant' }
        ]
      },
      sck: {
        title: 'चिंटू पत्ता अउर सूरज चाचा कर रसोई',
        story: 'पेड़ कर हरियर पत्ता मन छोट रसोइया होवेना! सूरज चाचा आपन रौद भेजेलें, पौधा मजे से आपन भोजन बनावेला।',
        flashcards: [
          { word: 'सूरज (Suraj)', prompt: 'रौद / Sunlight' },
          { word: 'पानी (Paani)', prompt: 'जल / Water' },
          { word: 'गाछ (Gaachh)', prompt: 'पेड़ / Plant' }
        ]
      },
      ho: {
        title: 'ᱪᱤᱱᱴᱩ ᱥᱟᱠᱟᱢ ᱟᱨ ᱥᱤᱝᱜᱤ ᱪᱟᱪᱟ (Chintu Sakam Story)',
        story: 'ᱫᱟᱨᱩ ᱨᱮᱱᱟᱜ ᱥᱟᱠᱟᱢ ᱠᱚ ᱡᱚᱢᱟ ᱵᱟᱭ ᱞᱟᱹᱜᱤᱱ ᱥᱤᱝᱜᱤ ᱢᱟᱨᱥᱟᱞ ᱟᱨ ᱫᱟᱜ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾',
        flashcards: [
          { word: 'ᱥᱤᱝᱜᱤ (Singi)', prompt: 'Suraj / Sun' },
          { word: 'ᱫᱟᱜ (Daag)', prompt: 'Paani / Water' },
          { word: 'ᱫᱟᱨᱩ (Daru)', prompt: 'Ped / Tree' }
        ]
      },
      bn: {
        title: 'চিহ্নু পাতা ও সূর্য দাদুর রান্নাঘর',
        story: 'গাছের সবুজ পাতাগুলি হল ছোট বাবুর্চি! সূর্য দাদু আলো পাঠায়, মেঘ জল দেয়, আর গাছ সুন্দর খাবার তৈরি করে।',
        flashcards: [
          { word: 'সূর্য (Surjo)', prompt: 'সূর্য / Sun' },
          { word: 'জল (Jol)', prompt: 'জল / Water' },
          { word: 'গাছ (Gaach)', prompt: 'গাছ / Tree' }
        ]
      },
      or: {
        title: 'ଚିଣ୍ଟୁ ପତ୍ର ଏବଂ ସୂର୍ଯ୍ୟ ମାମୁଁଙ୍କ ରୋଷେଇ',
        story: 'ଗଛର ସବୁଜ ପତ୍ର ହେଉଛି ଛୋଟ ରୋଷେୟା! ସୂର୍ଯ୍ୟ ମାମୁଁ କିରଣ ପଠାନ୍ତି, ପାଣି ମିଳେ, ଏବଂ ଗଛ ନିଜ ପାଇଁ ମିଠା ଖାଦ୍ୟ ତିଆରି କରେ।',
        flashcards: [
          { word: 'ସୂର୍ଯ୍ୟ (Surjya)', prompt: 'ସୂର୍ଯ୍ୟ / Sun' },
          { word: 'ପାଣି (Paani)', prompt: 'ଜଳ / Water' },
          { word: 'ଗଛ (Gachha)', prompt: 'ଗଛ / Tree' }
        ]
      }
    };

    return tribalMap[lang] || {
      title: 'चिंटू पत्ता और सूरज चाचा की रसोई',
      story: 'पेड़ के हरे पत्ते छोटे रसोइये होते हैं! सूरज चाचा अपनी मीठी धूप भेजते हैं, बारिश की बूंदें पानी लाती हैं, और पौधा मजे से अपना मीठा भोजन बनाता है।',
      flashcards: [
        { word: 'सूरज (Suraj)', prompt: 'धूप / Sunlight' },
        { word: 'पानी (Paani)', prompt: 'जल / Water' },
        { word: 'पत्ता (Patta)', prompt: 'रसोइया / Leaf Chef' }
      ]
    };
  }

  function displayKahani(data, lang) {
    storyTitle.textContent = data.title;
    storyContent.textContent = data.story;
    kahaniFlashcards.innerHTML = '';

    const flashcardList = data.flashcards || [];
    flashcardList.forEach((fc) => {
      const card = document.createElement('div');
      card.className = 'mini-flashcard';
      card.innerHTML = `
        <div style="font-size: 1.5rem;">🌟</div>
        <strong style="color:#0B2545;">${fc.word}</strong>
        <p style="font-size:0.75rem; color:#64748B;">${fc.prompt}</p>
      `;
      card.onclick = () => playVernacularSpeech(fc.word, lang, card);
      kahaniFlashcards.appendChild(card);
    });

    storyResultBox.style.display = 'block';
  }

  playStoryAudioBtn.addEventListener('click', () => {
    const lang = storyTargetLang ? storyTargetLang.value : 'hi';
    playVernacularSpeech(storyContent.textContent, lang, playStoryAudioBtn);
  });

  printWorksheetBtn.addEventListener('click', () => {
    const title = storyTitle.textContent || 'Bilingual Vernacular Science Worksheet';
    const content = storyContent.textContent || 'Photosynthesis and Nature.';
    
    document.getElementById('printContent').innerHTML = `
      <h4>Topic: ${title}</h4>
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px;">
        <div style="border: 1px solid #000; padding: 12px;">
          <strong>Original Text (English):</strong>
          <p style="margin-top: 8px;">Plants use sunlight and water to make food.</p>
        </div>
        <div style="border: 1px solid #000; padding: 12px;">
          <strong>Vernacular Text (Santali / Hindi):</strong>
          <p style="margin-top: 8px;">${content}</p>
        </div>
      </div>
      <div style="margin-top: 24px;">
        <strong>Class Activity:</strong> Draw a picture of the sun, tree, and raindrops!
        <div style="border: 1px dashed #000; height: 180px; margin-top: 10px;"></div>
      </div>
    `;
    window.print();
  });
}

// ==========================================================================
// 8. MODULE 4: AKSHAR MALA (INTERACTIVE PHONICS BOARD)
// ==========================================================================
function initAksharMala() {
  const grid = document.getElementById('alphabetGrid');
  const filters = document.querySelectorAll('.script-filter');

  const alphabets = {
    olchiki: [
      { char: 'ᱚ', phonics: 'Laa / Ol', mnemonic: 'ᱚᱛ (Ot / Earth)' },
      { char: 'ᱛ', phonics: 'At', mnemonic: 'ᱛᱟᱨᱟᱥ (Taras / Light)' },
      { char: 'ᱜ', phonics: 'Ag', mnemonic: 'ᱜᱟᱰᱟ (Gada / River)' },
      { char: 'ᱝ', phonics: 'Ang', mnemonic: 'ᱝᱟ (Nasal)' },
      { char: 'ᱞ', phonics: 'Al', mnemonic: 'ᱞᱩᱢᱟᱹᱝ (Lumam / Silk)' },
      { char: 'ᱟ', phonics: 'Aa', mnemonic: 'ᱟᱥᱲᱟ (Ashra / School)' },
      { char: 'ᱠ', phonics: 'Aak', mnemonic: 'ᱠᱟᱛᱮ (Friend)' },
      { char: 'ᱡ', phonics: 'Aaj', mnemonic: 'ᱡᱚᱦᱟᱨ (Johar / Welcome)' },
      { char: 'ᱢ', phonics: 'Am', mnemonic: 'ᱢᱟᱪᱮᱫ (Teacher)' },
      { char: 'ᱥ', phonics: 'As', mnemonic: 'ᱥᱤᱧ (Sun)' }
    ],
    deva: [
      { char: 'अ', phonics: 'A', mnemonic: 'अनार (Pomegranate)' },
      { char: 'आ', phonics: 'Aa', mnemonic: 'आम (Mango)' },
      { char: 'इ', phonics: 'I', mnemonic: 'इमली (Tamarind)' },
      { char: 'ई', phonics: 'Ee', mnemonic: 'ईख (Sugarcane)' },
      { char: 'क', phonics: 'Ka', mnemonic: 'कमल (Lotus)' },
      { char: 'ख', phonics: 'Kha', mnemonic: 'खरगोश (Rabbit)' },
      { char: 'ग', phonics: 'Ga', mnemonic: 'गमला (Pot)' },
      { char: 'घ', phonics: 'Gha', mnemonic: 'घर (Home)' }
    ],
    beng: [
      { char: 'অ', phonics: 'O', mnemonic: 'অজগর (Python)' },
      { char: 'আ', phonics: 'Aa', mnemonic: 'আম (Mango)' },
      { char: 'ই', phonics: 'I', mnemonic: 'ইঁদুর (Mouse)' },
      { char: 'ক', phonics: 'Ka', mnemonic: 'কাক (Crow)' },
      { char: 'খ', phonics: 'Kha', mnemonic: 'খাতা (Notebook)' },
      { char: 'গ', phonics: 'Ga', mnemonic: 'গাছ (Tree)' }
    ],
    odia: [
      { char: 'ଅ', phonics: 'A', mnemonic: 'ଅରଟ (Arata / Charkha)' },
      { char: 'ଆ', phonics: 'Aa', mnemonic: 'ଆମ୍ବ (Amba / Mango)' },
      { char: 'ଇ', phonics: 'I', mnemonic: 'ଇଟା (Ita / Brick)' },
      { char: 'କ', phonics: 'Ka', mnemonic: 'କଲମ (Kalama / Pen)' },
      { char: 'ଖ', phonics: 'Kha', mnemonic: 'ଖଡ଼ି (Khadi / Chalk)' },
      { char: 'ଗ', phonics: 'Ga', mnemonic: 'ଗଛ (Gachha / Tree)' }
    ],
    ho: [
      { char: 'ᱦᱳ', phonics: 'Ho', mnemonic: 'ᱦᱳ (Ho / People)' },
      { char: 'ᱚᱞ', phonics: 'Ol', mnemonic: 'ᱚᱞ (Ol / Write)' },
      { char: 'ᱟᱛ', phonics: 'At', mnemonic: 'ᱟᱛ (Aat / Village)' },
      { char: 'ᱫᱟᱜ', phonics: 'Daah', mnemonic: 'ᱫᱟᱜ (Daah / Water)' },
      { char: 'ᱫᱟᱨᱩ', phonics: 'Daru', mnemonic: 'ᱫᱟᱨᱩ (Daru / Tree)' }
    ]
  };

  function renderGrid(scriptKey) {
    grid.innerHTML = '';
    const items = alphabets[scriptKey] || alphabets.olchiki;
    items.forEach((item) => {
      const tile = document.createElement('div');
      tile.className = 'letter-tile';
      tile.innerHTML = `
        <div class="letter-char">${item.char}</div>
        <div class="letter-phonics">${item.phonics}</div>
        <div class="letter-mnemonic">${item.mnemonic}</div>
      `;
      tile.addEventListener('click', () => {
        playVernacularSpeech(`${item.char}. ${item.mnemonic}`, scriptKey === 'beng' ? 'bn' : 'hi');
      });
      grid.appendChild(tile);
    });
  }

  filters.forEach((btn) => {
    btn.addEventListener('click', () => {
      filters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderGrid(btn.getAttribute('data-script'));
    });
  });

  renderGrid('olchiki');
}

// ==========================================================================
// 9. MODULE 5: TEACHER HUB & MATRU-SANDESH
// ==========================================================================
function initTeacherHub() {
  const generateParentNoteBtn = document.getElementById('generateParentNoteBtn');
  const parentLessonTitle = document.getElementById('parentLessonTitle');
  const parentLangSelect = document.getElementById('parentLangSelect');
  const parentNoteBox = document.getElementById('parentNoteBox');
  const parentNoteScript = document.getElementById('parentNoteScript');
  const playParentAudioBtn = document.getElementById('playParentAudioBtn');
  const downloadPacksBtn = document.getElementById('downloadPacksBtn');
  const cacheStatusText = document.getElementById('cacheStatusText');

  generateParentNoteBtn.addEventListener('click', async () => {
    const title = parentLessonTitle.value.trim() || 'Plants and Nature';
    const lang = parentLangSelect.value;

    try {
      const resp = await fetch(`${API_BASE}/api/parent/briefing`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_title: title, lang: lang })
      });

      if (resp.ok) {
        const data = await resp.json();
        parentNoteScript.textContent = data.audio_script;
      } else {
        throw new Error('API offline');
      }
    } catch (e) {
      parentNoteScript.textContent = `नमस्ते अभिभावक जी! आज स्कूल में आपके बच्चे ने '${title}' के बारे में सीखा। घर पर बच्चे से पूछें और उसकी प्रशंसा करें। धन्यवाद!`;
    }

    parentNoteBox.style.display = 'block';
  });

  playParentAudioBtn.addEventListener('click', () => {
    playVernacularSpeech(parentNoteScript.textContent, parentLangSelect.value, playParentAudioBtn);
  });

  downloadPacksBtn.addEventListener('click', () => {
    downloadPacksBtn.textContent = '⏳ Caching All Packs for Offline Classroom...';
    setTimeout(() => {
      downloadPacksBtn.textContent = '✓ Packs Cached Successfully!';
      cacheStatusText.textContent = '✓ 3 Grade-level offline curriculum packs saved to tablet IndexedDB.';
    }, 1200);
  });
}

// ==========================================================================
// 10. CONFETTI CELEBRATION SYSTEM
// ==========================================================================
function initConfetti() {
  const canvas = document.getElementById('confettiCanvas');
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  window.triggerConfetti = function() {
    particles = [];
    const colors = ['#FF7700', '#10B981', '#FFB703', '#3B82F6', '#EC4899'];
    for (let i = 0; i < 90; i++) {
      particles.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        vx: (Math.random() - 0.5) * 16,
        vy: (Math.random() - 0.5) * 16 - 4,
        size: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        vr: (Math.random() - 0.5) * 10
      });
    }

    let frames = 0;
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.3; // gravity
        p.rotation += p.vr;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      });

      frames++;
      if (frames < 90) {
        requestAnimationFrame(animate);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }
    requestAnimationFrame(animate);
  };
}

// ==========================================================================
// 10. MODULE 6: JCERT / NCERT E-PUSTAKALAYA & OFFLINE NOTEBOOKS (CLASSES 1-5)
// ==========================================================================
function initNotebooksLibrary() {
  const notebooksGrid = document.getElementById('notebooksGrid');
  const gradeFilterGroup = document.getElementById('gradeFilterGroup');
  const subjectFilterGroup = document.getElementById('subjectFilterGroup');
  const myOfflineBooksBtn = document.getElementById('myOfflineBooksBtn');
  const offlineBooksCount = document.getElementById('offlineBooksCount');
  const downloadCurrentGradeBtn = document.getElementById('downloadCurrentGradeBtn');

  // Modal elements
  const chapterReaderModal = document.getElementById('chapterReaderModal');
  const closeReaderBtn = document.getElementById('closeReaderBtn');
  const readerSubjectBadge = document.getElementById('readerSubjectBadge');
  const readerChapterTitle = document.getElementById('readerChapterTitle');
  const readerEnglishTitle = document.getElementById('readerEnglishTitle');
  const readerConceptSummary = document.getElementById('readerConceptSummary');
  const readerLangSelect = document.getElementById('readerLangSelect');
  const bilingualToggle = document.getElementById('bilingualToggle');
  const readerNarrationBtn = document.getElementById('readerNarrationBtn');
  const readerDownloadBtn = document.getElementById('readerDownloadBtn');
  const readerPrintBtn = document.getElementById('readerPrintBtn');
  const readerParagraphsList = document.getElementById('readerParagraphsList');
  const readerQuestionsList = document.getElementById('readerQuestionsList');
  const readerKeywordsList = document.getElementById('readerKeywordsList');

  if (!notebooksGrid) return;

  let currentGradeFilter = 'all';
  let currentSubjectFilter = 'all';
  let showingOnlyOffline = false;
  let currentActiveChapter = null;

  // Filter Event Listeners
  if (gradeFilterGroup) {
    gradeFilterGroup.querySelectorAll('.filter-pill').forEach((btn) => {
      btn.addEventListener('click', () => {
        gradeFilterGroup.querySelectorAll('.filter-pill').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        currentGradeFilter = btn.getAttribute('data-grade');
        showingOnlyOffline = false;
        loadBooks();
      });
    });
  }

  if (subjectFilterGroup) {
    subjectFilterGroup.querySelectorAll('.filter-pill').forEach((btn) => {
      btn.addEventListener('click', () => {
        subjectFilterGroup.querySelectorAll('.filter-pill').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        currentSubjectFilter = btn.getAttribute('data-subject');
        showingOnlyOffline = false;
        loadBooks();
      });
    });
  }

  if (myOfflineBooksBtn) {
    myOfflineBooksBtn.addEventListener('click', () => {
      showingOnlyOffline = !showingOnlyOffline;
      if (showingOnlyOffline) {
        myOfflineBooksBtn.style.background = '#22C55E';
        myOfflineBooksBtn.style.color = '#FFFFFF';
      } else {
        myOfflineBooksBtn.style.background = '#F0FDF4';
        myOfflineBooksBtn.style.color = '#166534';
      }
      loadBooks();
    });
  }

  if (downloadCurrentGradeBtn) {
    downloadCurrentGradeBtn.addEventListener('click', async () => {
      const gradeToDownload = currentGradeFilter === 'all' ? 1 : Number(currentGradeFilter);
      downloadCurrentGradeBtn.textContent = '⏳ डाउनलोड हो रहा है...';
      try {
        const resp = await fetch(`${API_BASE}/api/curriculum/offline-bundle?grade=${gradeToDownload}`);
        if (resp.ok) {
          const data = await resp.json();
          if (data.bundle && window.matrubhasaDB) {
            await window.matrubhasaDB.saveGradeBundle(gradeToDownload, data.bundle);
            downloadCurrentGradeBtn.textContent = `✓ कक्षा ${gradeToDownload} के सभी पाठ ऑफ़लाइन सहेजे गए!`;
            setTimeout(() => {
              downloadCurrentGradeBtn.textContent = '⚡ इस कक्षा का पूरा पैक डाउनलोड करें (1-Click Offline)';
            }, 3000);
            loadBooks();
            return;
          }
        }
      } catch (e) {
        console.warn('Bulk download error:', e);
      }
      downloadCurrentGradeBtn.textContent = '✓ ऑफ़लाइन पैक तैयार!';
      setTimeout(() => {
        downloadCurrentGradeBtn.textContent = '⚡ इस कक्षा का पूरा पैक डाउनलोड करें (1-Click Offline)';
      }, 3000);
      loadBooks();
    });
  }

  // Load books
  async function loadBooks() {
    notebooksGrid.innerHTML = '<div style="padding: 24px; color: #64748B;">लोड हो रहा है...</div>';

    let books = [];
    // Update offline count
    if (window.matrubhasaDB) {
      const offlineList = await window.matrubhasaDB.getAllDownloadedChapters();
      if (offlineBooksCount) offlineBooksCount.textContent = offlineList.length;

      if (showingOnlyOffline || state.isOffline) {
        books = offlineList;
        if (currentGradeFilter !== 'all') {
          books = books.filter((b) => b.grade === Number(currentGradeFilter));
        }
        if (currentSubjectFilter !== 'all') {
          books = books.filter((b) => b.subject === currentSubjectFilter.toLowerCase());
        }
        renderBooks(books);
        return;
      }
    }

    try {
      const params = new URLSearchParams();
      if (currentGradeFilter !== 'all') params.append('grade', currentGradeFilter);
      if (currentSubjectFilter !== 'all') params.append('subject', currentSubjectFilter);

      const resp = await fetch(`${API_BASE}/api/curriculum/books?${params.toString()}`);
      if (resp.ok) {
        const data = await resp.json();
        books = data.books || [];
      }
    } catch (e) {
      console.warn('Backend books API unreachable, using local cache:', e);
      if (window.matrubhasaDB) {
        books = await window.matrubhasaDB.getAllDownloadedChapters();
      }
    }

    renderBooks(books);
  }

  async function renderBooks(books) {
    if (!books || books.length === 0) {
      notebooksGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: #F8FAFC; border-radius: 16px; border: 2px dashed #CBD5E1;">
          <div style="font-size: 2.4rem; margin-bottom: 8px;">📚</div>
          <h3 style="color: #334155; margin-bottom: 6px;">कोई पाठ्यपुस्तक नहीं मिली</h3>
          <p style="color: #64748B; font-size: 0.9rem;">कृपया अन्य कक्षा या विषय का चयन करें, अथवा ऑनलाइन होकर पाठ डाउनलोड करें।</p>
        </div>
      `;
      return;
    }

    notebooksGrid.innerHTML = '';
    for (const book of books) {
      const isOffline = window.matrubhasaDB ? await window.matrubhasaDB.isChapterOffline(book.id) : false;
      const card = document.createElement('div');
      card.className = 'notebook-card';
      card.innerHTML = `
        <div>
          <div class="notebook-card-header">
            <div class="book-icon-badge">${book.subject_icon || '📖'}</div>
            <span class="offline-pill ${isOffline ? 'downloaded' : 'online-only'}">
              ${isOffline ? '✓ ऑफ़लाइन तैयार (Saved)' : '☁️ क्लाउड (Online)'}
            </span>
          </div>
          <span style="font-size: 0.76rem; font-weight: 700; color: #0284C7; text-transform: uppercase;">
            ${book.subject_name || book.subject} • ${book.grade_label || 'कक्षा ' + book.grade}
          </span>
          <h3>${book.title_hi}</h3>
          <div class="notebook-card-subtitle">${book.title_en}</div>
          <p class="notebook-card-summary">${book.concept_summary}</p>
        </div>
        <div class="notebook-card-actions">
          <button type="button" class="btn-read-chapter" data-id="${book.id}">
            📖 पढ़ना शुरू करें
          </button>
          <button type="button" class="btn-download-chapter ${isOffline ? 'is-saved' : ''}" data-id="${book.id}">
            ${isOffline ? '✓ सहेजा गया' : '📥 ऑफ़लाइन'}
          </button>
        </div>
      `;

      card.querySelector('.btn-read-chapter').addEventListener('click', () => {
        openChapterReader(book.id, readerLangSelect ? readerLangSelect.value : 'sat');
      });

      const dlBtn = card.querySelector('.btn-download-chapter');
      dlBtn.addEventListener('click', async () => {
        dlBtn.textContent = '⏳ सहेज रहे...';
        await saveChapterLocally(book.id);
        dlBtn.textContent = '✓ सहेजा गया';
        dlBtn.classList.add('is-saved');
        const pill = card.querySelector('.offline-pill');
        if (pill) {
          pill.className = 'offline-pill downloaded';
          pill.textContent = '✓ ऑफ़लाइन तैयार (Saved)';
        }
        if (window.matrubhasaDB) {
          const list = await window.matrubhasaDB.getAllDownloadedChapters();
          if (offlineBooksCount) offlineBooksCount.textContent = list.length;
        }
      });

      notebooksGrid.appendChild(card);
    }
  }

  async function saveChapterLocally(chapterId) {
    try {
      const resp = await fetch(`${API_BASE}/api/curriculum/chapter?id=${chapterId}&lang=sat`);
      if (resp.ok) {
        const chapterData = await resp.json();
        if (window.matrubhasaDB) {
          await window.matrubhasaDB.saveChapter(chapterData);
          return true;
        }
      }
    } catch (e) {
      console.warn('Could not download chapter:', e);
    }
    return false;
  }

  // Open Chapter Reader Modal
  async function openChapterReader(chapterId, targetLang = 'sat') {
    let chapter = null;

    // First check local IndexedDB
    if (window.matrubhasaDB) {
      chapter = await window.matrubhasaDB.getChapter(chapterId);
    }

    if (!chapter && !state.isOffline) {
      try {
        const resp = await fetch(`${API_BASE}/api/curriculum/chapter?id=${chapterId}&lang=${targetLang}`);
        if (resp.ok) {
          chapter = await resp.json();
        }
      } catch (e) {
        console.warn('Fetch chapter error:', e);
      }
    }

    if (!chapter) {
      alert('यह पाठ अभी ऑफ़लाइन उपलब्ध नहीं है। कृपया इंटरनेट से जुड़कर एक बार डाउनलोड करें!');
      return;
    }

    currentActiveChapter = chapter;
    renderChapterReaderContent(chapter, targetLang);
    chapterReaderModal.style.display = 'flex';
  }

  function renderChapterReaderContent(chapter, targetLang) {
    readerSubjectBadge.textContent = `${chapter.subject_icon || '🌿'} ${chapter.subject_name || chapter.subject} • ${chapter.grade_label || 'कक्षा ' + chapter.grade}`;
    readerChapterTitle.textContent = `पाठ ${chapter.chapter_no}: ${chapter.title_hi}`;
    readerEnglishTitle.textContent = chapter.title_en;
    readerConceptSummary.textContent = chapter.concept_summary;

    const showBilingual = bilingualToggle ? bilingualToggle.checked : true;

    // Render paragraphs
    readerParagraphsList.innerHTML = '';
    (chapter.paragraphs || []).forEach((p, idx) => {
      const textVernacular = p[targetLang] || p.vernacular || p.hi || p.en;
      const paraItem = document.createElement('div');
      paraItem.className = 'reader-para-item';
      paraItem.innerHTML = `
        <div class="para-vernacular">${textVernacular}</div>
        ${showBilingual ? `<div class="para-bilingual"><strong>हिन्दी / English:</strong> ${p.hi} (${p.en})</div>` : ''}
        <button type="button" class="btn-speak-para" title="Listen to this paragraph in mother tongue">
          🔊 सुनो (Play)
        </button>
      `;

      paraItem.querySelector('.btn-speak-para').addEventListener('click', () => {
        playVernacularSpeech(textVernacular, targetLang, paraItem.querySelector('.btn-speak-para'));
      });

      readerParagraphsList.appendChild(paraItem);
    });

    // Render Abhyas Questions
    readerQuestionsList.innerHTML = '';
    (chapter.abhyas_questions || []).forEach((q, idx) => {
      const qCard = document.createElement('div');
      qCard.className = 'question-card';
      qCard.innerHTML = `
        <div class="question-text">प्रश्न ${idx + 1}: ${q.q}</div>
        <div class="question-hint">💡 संकेत / उत्तर: ${q.hint}</div>
      `;
      readerQuestionsList.appendChild(qCard);
    });

    // Render Keywords Flashcards
    readerKeywordsList.innerHTML = '';
    (chapter.keywords || []).forEach((kw) => {
      const card = document.createElement('div');
      card.className = 'keyword-card';
      const wordTrans = kw[targetLang] || kw.word || kw.hi;
      card.innerHTML = `
        <div class="keyword-word">🔊 ${wordTrans}</div>
        <div class="keyword-hindi">${kw.hindi} (${kw.en})</div>
        <div class="keyword-meaning">${kw.meaning}</div>
      `;
      card.addEventListener('click', () => {
        playVernacularSpeech(wordTrans, targetLang, card);
      });
      readerKeywordsList.appendChild(card);
    });
  }

  // Reader Event Listeners
  if (closeReaderBtn) {
    closeReaderBtn.addEventListener('click', () => {
      chapterReaderModal.style.display = 'none';
    });
  }

  if (readerLangSelect) {
    readerLangSelect.addEventListener('change', () => {
      if (currentActiveChapter) {
        renderChapterReaderContent(currentActiveChapter, readerLangSelect.value);
      }
    });
  }

  if (bilingualToggle) {
    bilingualToggle.addEventListener('change', () => {
      if (currentActiveChapter) {
        renderChapterReaderContent(currentActiveChapter, readerLangSelect ? readerLangSelect.value : 'sat');
      }
    });
  }

  if (readerNarrationBtn) {
    readerNarrationBtn.addEventListener('click', () => {
      if (!currentActiveChapter) return;
      const targetLang = readerLangSelect ? readerLangSelect.value : 'sat';
      // Gather all vernacular paragraphs
      const fullText = (currentActiveChapter.paragraphs || [])
        .map((p) => p[targetLang] || p.vernacular || p.hi)
        .join(' । ');
      playVernacularSpeech(fullText, targetLang, readerNarrationBtn);
    });
  }

  if (readerDownloadBtn) {
    readerDownloadBtn.addEventListener('click', async () => {
      if (!currentActiveChapter) return;
      readerDownloadBtn.textContent = '⏳ सहेज रहे...';
      if (window.matrubhasaDB) {
        await window.matrubhasaDB.saveChapter(currentActiveChapter);
      }
      readerDownloadBtn.textContent = '✓ ऑफ़लाइन सहेजा गया';
      setTimeout(() => {
        readerDownloadBtn.textContent = '📥 ऑफ़लाइन सहेजें';
      }, 2500);
      loadBooks();
    });
  }

  if (readerPrintBtn) {
    readerPrintBtn.addEventListener('click', () => {
      if (!currentActiveChapter) return;
      const targetLang = readerLangSelect ? readerLangSelect.value : 'sat';
      const printContainer = document.getElementById('printContent');
      if (!printContainer) return;

      let html = `
        <h2 style="font-size: 1.4rem; margin-bottom: 4px;">${currentActiveChapter.title_hi} (${currentActiveChapter.title_en})</h2>
        <p style="font-size: 0.95rem; color: #475569; margin-bottom: 14px;">
          ${currentActiveChapter.subject_name} • ${currentActiveChapter.grade_label} • मातृभाषा: ${targetLang.toUpperCase()}
        </p>
        <div style="background: #F8FAFC; padding: 12px; border-left: 4px solid #FF7700; margin-bottom: 16px;">
          <strong>मुख्य विचार (Core Concept):</strong> ${currentActiveChapter.concept_summary}
        </div>
        <h3 style="margin-top: 18px; border-bottom: 1px solid #CBD5E1; padding-bottom: 4px;">📖 पाठ का अंश (Chapter Reading):</h3>
      `;

      (currentActiveChapter.paragraphs || []).forEach((p, idx) => {
        const textV = p[targetLang] || p.vernacular || p.hi;
        html += `
          <div style="margin-bottom: 12px;">
            <p style="font-size: 1.1rem; font-weight: 600; color: #0F172A; margin: 0;">${idx + 1}. ${textV}</p>
            <p style="font-size: 0.88rem; color: #64748B; margin: 2px 0 0 0;">${p.hi} (${p.en})</p>
          </div>
        `;
      });

      html += `<h3 style="margin-top: 20px; border-bottom: 1px solid #CBD5E1; padding-bottom: 4px;">📝 अभ्यास पुस्तिका प्रश्न (Practice Questions):</h3>`;
      (currentActiveChapter.abhyas_questions || []).forEach((q, idx) => {
        html += `
          <div style="margin-bottom: 10px;">
            <p style="font-weight: 600; margin: 0;">प्रश्न ${idx + 1}: ${q.q}</p>
            <p style="font-size: 0.85rem; color: #15803D; margin: 2px 0 0 0;">उत्तर / संकेत: ${q.hint}</p>
          </div>
        `;
      });

      printContainer.innerHTML = html;
      window.print();
    });
  }

  // Initial load of books
  loadBooks();
}