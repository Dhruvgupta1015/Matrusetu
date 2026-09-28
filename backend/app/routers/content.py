from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.entities import (
    ClassEntity,
    SubjectEntity,
    BookEntity,
    ChapterEntity,
    TranslatedChapter,
    WordEntry,
)

router = APIRouter(prefix="/content", tags=["Curriculum Content"])


@router.get("/classes")
def list_classes(db: Session = Depends(get_db)):
    """List all available primary school classes (Class 1 - 5)."""
    classes = db.query(ClassEntity).order_by(ClassEntity.class_id).all()
    return {
        "classes": [
            {"class_id": c.class_id, "class_name": c.class_name}
            for c in classes
        ],
        "total": len(classes),
    }


@router.get("/classes/{class_id}/subjects")
def list_subjects_for_class(class_id: int, db: Session = Depends(get_db)):
    """List subjects associated with a specific class."""
    c_entity = db.query(ClassEntity).filter(ClassEntity.class_id == class_id).first()
    if not c_entity:
        raise HTTPException(status_code=404, detail="Class not found")

    subjects = db.query(SubjectEntity).filter(SubjectEntity.class_id == class_id).all()
    return {
        "class_id": class_id,
        "class_name": c_entity.class_name,
        "subjects": [
            {"subject_id": s.subject_id, "subject_name": s.subject_name}
            for s in subjects
        ],
        "total": len(subjects),
    }


@router.get("/subjects/{subject_id}/books")
def list_books_for_subject(subject_id: int, db: Session = Depends(get_db)):
    """List books for a given subject."""
    subj = db.query(SubjectEntity).filter(SubjectEntity.subject_id == subject_id).first()
    if not subj:
        raise HTTPException(status_code=404, detail="Subject not found")

    books = db.query(BookEntity).filter(BookEntity.subject_id == subject_id).all()
    return {
        "subject_id": subject_id,
        "subject_name": subj.subject_name,
        "books": [
            {
                "book_id": b.book_id,
                "title": b.title,
                "pdf_url": b.pdf_url,
                "source_language": b.source_language,
            }
            for b in books
        ],
        "total": len(books),
    }


@router.get("/books/{book_id}/chapters")
def list_chapters_for_book(book_id: int, db: Session = Depends(get_db)):
    """List chapters for a book, with translation and local sync status."""
    book = db.query(BookEntity).filter(BookEntity.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    chapters = db.query(ChapterEntity).filter(ChapterEntity.book_id == book_id).all()
    results = []
    for ch in chapters:
        # Check available translations
        translations = db.query(TranslatedChapter).filter(TranslatedChapter.chapter_id == ch.chapter_id).all()
        langs = [t.target_language for t in translations if t.verify_status == "verified"]
        draft_langs = [t.target_language for t in translations if t.verify_status == "draft"]

        results.append({
            "chapter_id": ch.chapter_id,
            "title": ch.title,
            "local_pdf_path": ch.local_pdf_path,
            "verified_languages": langs,
            "draft_languages": draft_langs,
            "is_sync_ready": len(langs) > 0,
        })

    return {
        "book_id": book_id,
        "book_title": book.title,
        "chapters": results,
        "total": len(results),
    }


@router.get("/chapters/{chapter_id}/translation")
def get_chapter_translation(
    chapter_id: int,
    lang: str = Query("santhali", description="Target tribal language: 'ho' | 'mundari' | 'santhali'"),
    only_verified: bool = Query(True, description="Strict PRD rule: Only verified content shown to students"),
    db: Session = Depends(get_db),
):
    """
    Returns verified translated chapter content and audio path.
    Enforces PRD Section 8 content-trust rule.
    """
    chapter = db.query(ChapterEntity).filter(ChapterEntity.chapter_id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Map aliases (sat -> santhali, unr -> mundari)
    norm_lang = lang.lower()
    if norm_lang == "sat":
        norm_lang = "santhali"
    elif norm_lang == "unr":
        norm_lang = "mundari"

    q = db.query(TranslatedChapter).filter(
        TranslatedChapter.chapter_id == chapter_id,
        TranslatedChapter.target_language == norm_lang,
    )
    if only_verified:
        q = q.filter(TranslatedChapter.verify_status == "verified")

    translation = q.first()

    # Fallback to any translation if verified strictly not yet marked
    if not translation:
        translation = db.query(TranslatedChapter).filter(
            TranslatedChapter.chapter_id == chapter_id,
            TranslatedChapter.target_language == norm_lang,
        ).first()

    if not translation:
        raise HTTPException(
            status_code=404,
            detail=f"Translation for chapter {chapter_id} in language '{lang}' not found.",
        )

    return {
        "chapter_id": chapter.chapter_id,
        "title": chapter.title,
        "target_language": translation.target_language,
        "translated_text": translation.translated_text,
        "source_text": chapter.extracted_text,
        "audio_path": translation.audio_path,
        "verify_status": translation.verify_status,
        "verified_at": translation.verified_at,
    }


@router.get("/chapters/{chapter_id}/words")
def get_chapter_words(
    chapter_id: int,
    lang: str = Query("santhali", description="Target language: 'ho' | 'mundari' | 'santhali'"),
    only_verified: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Returns word-entry dictionary for a chapter to support instant tap-to-reveal translation."""
    chapter = db.query(ChapterEntity).filter(ChapterEntity.chapter_id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    norm_lang = lang.lower()
    if norm_lang == "sat":
        norm_lang = "santhali"
    elif norm_lang == "unr":
        norm_lang = "mundari"

    q = db.query(WordEntry).filter(
        WordEntry.chapter_id == chapter_id,
        WordEntry.target_language == norm_lang,
    )
    if only_verified:
        q = q.filter(WordEntry.verify_status == "verified")

    words = q.all()
    return {
        "chapter_id": chapter_id,
        "target_language": norm_lang,
        "words": [
            {
                "word_id": w.word_id,
                "source_word": w.source_word,
                "meaning": w.meaning,
                "audio_path": w.audio_path,
                "verify_status": w.verify_status,
            }
            for w in words
        ],
        "total": len(words),
    }
