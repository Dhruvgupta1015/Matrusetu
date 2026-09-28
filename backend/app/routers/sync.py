import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.entities import (
    DeviceSyncLog,
    ChapterEntity,
    TranslatedChapter,
    WordEntry,
)

router = APIRouter(prefix="/sync", tags=["Device Sync Protocol"])

CURRENT_PLATFORM_BUNDLE_VERSION = "v3.0-2026.09"


class SyncBundleRequest(BaseModel):
    device_id: str
    school_code: Optional[str] = "JH-DUM-001"
    target_languages: Optional[List[str]] = ["santhali", "ho", "mundari"]
    current_bundle_version: Optional[str] = None


class SyncAckRequest(BaseModel):
    device_id: str
    school_code: Optional[str] = "JH-DUM-001"
    bundle_version: str
    status: Optional[str] = "applied"  # 'applied' | 'failed'


@router.get("/bundle")
def get_sync_bundle(
    device_id: str = "TAB-DEFAULT",
    school_code: str = "JH-DUM-001",
    current_bundle_version: Optional[str] = None,
    db: Session = Depends(get_db)
):
    req = SyncBundleRequest(
        device_id=device_id,
        school_code=school_code,
        current_bundle_version=current_bundle_version
    )
    return request_sync_bundle(req, db)


@router.post("/bundle")
def request_sync_bundle(req: SyncBundleRequest, db: Session = Depends(get_db)):
    """
    Builds and returns a device sync bundle for client PWA & IndexedDB storage.
    Enforces that only verified curriculum content is bundled for offline classroom use.
    """
    is_delta = req.current_bundle_version == CURRENT_PLATFORM_BUNDLE_VERSION

    # Fetch verified translations
    verified_translations = (
        db.query(TranslatedChapter)
        .filter(TranslatedChapter.verify_status == "verified")
        .all()
    )

    chapters_payload = []
    seen_chapter_ids = set()
    for tr in verified_translations:
        ch = tr.chapter_rel
        if not ch:
            continue
        seen_chapter_ids.add(ch.chapter_id)
        chapters_payload.append({
            "translation_id": tr.translation_id,
            "chapter_id": ch.chapter_id,
            "book_id": ch.book_id,
            "title": ch.title,
            "target_language": tr.target_language,
            "translated_text": tr.translated_text,
            "source_text": ch.extracted_text,
            "audio_path": tr.audio_path,
            "verified_at": tr.verified_at.isoformat() if tr.verified_at else None,
        })

    # Fetch verified vocabulary words
    verified_words = (
        db.query(WordEntry)
        .filter(WordEntry.verify_status == "verified")
        .all()
    )

    words_payload = [
        {
            "word_id": w.word_id,
            "chapter_id": w.chapter_id,
            "source_word": w.source_word,
            "target_language": w.target_language,
            "meaning": w.meaning,
            "audio_path": w.audio_path,
        }
        for w in verified_words
    ]

    return {
        "status": "ready",
        "bundle_version": CURRENT_PLATFORM_BUNDLE_VERSION,
        "is_delta": is_delta,
        "device_id": req.device_id,
        "school_code": req.school_code,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_chapters": len(chapters_payload),
        "total_words": len(words_payload),
        "verified_chapters": chapters_payload,
        "word_dictionary": words_payload,
        "models_manifest": {
            "nmt_engine": "IndicTrans2-Compressed-ONNX",
            "asr_engine": "Bhashini-Edge-Wav2Vec2",
            "tts_engine": "Indic-FastSpeech2",
            "status": "cached_on_device",
        },
    }


@router.post("/ack")
def acknowledge_sync(req: SyncAckRequest, db: Session = Depends(get_db)):
    """
    Confirms device received and applied the offline bundle.
    Updates the official device_sync_log table.
    """
    log_entry = (
        db.query(DeviceSyncLog)
        .filter(DeviceSyncLog.device_id == req.device_id)
        .order_by(DeviceSyncLog.sync_id.desc())
        .first()
    )

    now = datetime.datetime.now(datetime.timezone.utc)
    if log_entry:
        log_entry.school_code = req.school_code
        log_entry.last_synced_at = now
        log_entry.bundle_version = req.bundle_version
    else:
        log_entry = DeviceSyncLog(
            device_id=req.device_id,
            school_code=req.school_code,
            last_synced_at=now,
            bundle_version=req.bundle_version,
        )
        db.add(log_entry)

    db.commit()
    db.refresh(log_entry)

    return {
        "status": "acknowledged",
        "sync_id": log_entry.sync_id,
        "device_id": log_entry.device_id,
        "last_synced_at": log_entry.last_synced_at.isoformat(),
        "bundle_version": log_entry.bundle_version,
    }
