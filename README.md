# मातृभाषा AI (Matrubhasa AI)
### AI-Powered Vernacular Pedagogy & Real-Time Classroom Translation for Mother Tongue-Based Primary Education
**Created & Architected by Team MATRUSETU**  
**Smart India Hackathon 2026 — Problem Statement SIH26042**  
*Organization: Government of Jharkhand — Department of School Education*  
*Alignment: National Education Policy (NEP 2020) & NIPUN Bharat Mission (FLN)*

---

## 🌟 Executive Summary
In rural and tribal primary classrooms across India, textbooks are typically written in Standard English or Hindi, while young children (Grades 1–5) speak indigenous mother tongues at home (e.g. **Santali Ol Chiki, Ho, Mundari, Kurukh, Khortha, Nagpuri, Bengali, Odia**). 

Generic machine translation fails primary education because literal word-to-word translations cannot convey concepts to a 6-year-old child. **Matrubhasa AI** bridges this divide by delivering:
1. **Explain-Like-I'm-6 (ELI6) Concept Simplification** & Cultural Folk Metaphors (**Desi Kahani**).
2. **Real-Time Live Classroom Voice Bridge** for teachers & students with instant audio playback.
3. **Voice-First Interactive Reading Coach (Bal Vatika / Bhasha Mitr)** with real-time phoneme evaluation, green word highlighting, stars, and confetti (aligned with NIPUN Bharat FLN).
4. **100% Functional Gaon Offline Mode (PWA)** with client-side IndexedDB caching and local tribal glossaries for zero-connectivity schools.
5. **Community Inclusion (Matru-Sandesh)**: 30-second mother tongue audio briefings for illiterate parents.

---

## 🏛️ System Architecture

```
                                  ┌───────────────────────────────────────────────┐
                                  │          MATRUBHASA AI FULL STACK             │
                                  └──────────────────────┬────────────────────────┘
                                                         │
               ┌───────────────────────────┬─────────────┴────────────┬────────────────────────────┐
               ▼                           ▼                          ▼                            ▼
   【Real-Time Voice Bridge】     【Gaon Offline Hub】       【Bhasha Mitr (FLN)】        【Pathshala Lens】
    • Live Teacher-Student mic    • PWA Service Worker       • Voice-first reading aloud  • Textbook to Desi Kahani
    • Bhashini ASR + TTS          • IndexedDB Local Cache    • Word-by-word green matching• Interactive Flashcards
    • Live ELI6 Simplifier        • Tribal Dialect Glossary  • Confetti & 3 Stars ⭐⭐⭐   • Printable PDF Worksheets
    • Dual-Language Subtitles     • Browser Speech Fallback  • Offline Score Persistence  • QR Audio Handouts
``` . #Parental substitution AI   . #BOOKS SUBSTITUITION    . #DATABASES INTERACTUAL       . #AUDIO CHANGATION 

---

## 🚀 The 5 Core Working Modules

### 1. 🎙️ Classroom Live Bridge (कक्षा सेतु)
* Teachers speak into the microphone in English or Hindi.
* Real-time audio waveform visualizer and speech-to-text.
* Live translation into 9 indigenous and regional vernaculars with full native scripts:
  - ᱥᱟᱱᱛᱟᱲᱤ (Santali - Ol Chiki)
  - ᱦᱳ / हो (Ho - Warang Citi & Devanagari)
  - मुंडारी (Mundari)
  - कुड़ुख़ (Kurukh / Oraon)
  - खोरठा (Khortha)
  - नागपुरी / सादरी (Nagpuri)
  - हिन्दी (Hindi)
  - বাংলা (Bengali)
  - ଓଡ଼ିଆ (Odia)
* 🔊 One-tap vernacular audio playback with **🐢 0.85x Child Speed** for phonetic clarity.
* Interactive visual cue cards for foundational vocabulary (`☀️ Suraj`, `💧 Paani`, `🌿 Dare`).

### 2. 📖 Pathshala Lens (पाठशाला लेन्स)
* Transforms complex textbook definitions into relatable Indian cultural stories (*"चिंटू पत्ता और सूरज चाचा की रसोई"*).
* Generates interactive audio flashcards and a 1-click **Bilingual Printable Classroom Worksheet (PDF)**.

### 3. 🐘 Bal Vatika — Bhasha Mitr (भाषा मित्र)
* Guided by **"Gajju Bhai" (गज्जू भाई)**, an animated elephant mascot.
* Displays grade-appropriate reading sentences in the child's mother tongue.
* Child taps **🎤 Tap & Speak**: words dynamically turn **green** as spoken correctly, followed by a **confetti shower 🎊** and **3-star rating ⭐⭐⭐**.
* Scores are persisted in local IndexedDB for teacher progress tracking.

### 4. 🔤 Akshar & Shabda Mala (अक्षर व ध्वनि माला)
* Interactive soundboard for Santali Ol Chiki (`ᱚ, ᱛ, ᱜ, ᱝ...`), Devanagari, Bengali, Odia, and Ho Warang Citi.
* Tap any tile to hear the phonetic pronunciation and visual mnemonic.

### 5. 📊 Sikshak & Gaon Offline Hub (शिक्षक मंच)
* **Matru-Sandesh**: Generates 30-second vernacular audio briefings for rural parents.
* **Offline Curriculum Caching**: 1-click download of Grade 1-5 offline packs.
* **Network Status Pill**: Click the top-right pill to simulate and test **Gaon Offline Mode**.

---

## 🛠️ Quick Start & Running Locally

### 1. Start the Backend API
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
* Visit `http://127.0.0.1:8000/api/health` to verify status.
* Enter your Bhashini credentials in `backend/.env`:
  ```env
  BHASHINI_USER_ID=your_user_id
  BHASHINI_ULCA_API_KEY=your_api_key
  ```

### 2. Start the Frontend Web App
```bash
cd frontend
python -m http.server 5500
```
* Open **`http://127.0.0.1:5500`** in Google Chrome or Microsoft Edge.

---

## 🇮🇳 Why This Wins at SIH 2026
1. **Sovereign AI Integration**: Uses Digital India's **Bhashini (NLTM / MeitY)** with **AI4Bharat's IndicTrans2** as a zero-downtime backup.
2. **True Pedagogy, Not Just Translation**: Specifically engineered for Primary Education (NEP 2020 & NIPUN Bharat FLN).
3. **Indigenous Linguistic Inclusivity**: Purpose-built for Jharkhand's tribal languages (Santali Ol Chiki, Ho, Mundari, Kurukh, Khortha, Nagpuri).
4. **Resilient Offline-First Design**: Works completely inside village classrooms without internet access.
