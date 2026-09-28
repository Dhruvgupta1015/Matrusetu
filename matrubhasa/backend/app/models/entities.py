from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    JSON,
)
from sqlalchemy.orm import relationship
from ..db.session import Base


class ClassEntity(Base):
    __tablename__ = "class"

    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_name = Column(String(50), nullable=False)

    subjects = relationship("SubjectEntity", back_populates="class_rel", cascade="all, delete-orphan")
    students = relationship("AppUser", back_populates="class_rel")


class SubjectEntity(Base):
    __tablename__ = "subject"

    subject_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("class.class_id"), nullable=False)
    subject_name = Column(String(100), nullable=False)

    class_rel = relationship("ClassEntity", back_populates="subjects")
    books = relationship("BookEntity", back_populates="subject_rel", cascade="all, delete-orphan")


class BookEntity(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), nullable=False)
    title = Column(String(255), nullable=False)
    pdf_url = Column(Text, nullable=False, default="")
    source_language = Column(String(50), nullable=False, default="hi")

    subject_rel = relationship("SubjectEntity", back_populates="books")
    chapters = relationship("ChapterEntity", back_populates="book_rel", cascade="all, delete-orphan")


class ChapterEntity(Base):
    __tablename__ = "chapter"

    chapter_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    title = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    local_pdf_path = Column(Text, nullable=True)

    book_rel = relationship("BookEntity", back_populates="chapters")
    translations = relationship("TranslatedChapter", back_populates="chapter_rel", cascade="all, delete-orphan")
    words = relationship("WordEntry", back_populates="chapter_rel", cascade="all, delete-orphan")
    progress_records = relationship("StudentProgress", back_populates="chapter_rel")


class TranslatedChapter(Base):
    __tablename__ = "translated_chapter"

    translation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)
    target_language = Column(String(50), nullable=False)  # 'ho' | 'mundari' | 'santhali'
    translated_text = Column(Text, nullable=True)
    audio_path = Column(Text, nullable=True)
    verify_status = Column(String(20), nullable=False, default="draft")  # 'draft' | 'verified'
    verified_by = Column(Integer, ForeignKey("app_user.user_id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    chapter_rel = relationship("ChapterEntity", back_populates="translations")
    verifier_rel = relationship("AppUser", back_populates="verified_translations")


class WordEntry(Base):
    __tablename__ = "word_entry"

    word_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)
    source_word = Column(String(255), nullable=False)
    target_language = Column(String(50), nullable=False)
    meaning = Column(Text, nullable=False)
    audio_path = Column(Text, nullable=True)
    verify_status = Column(String(20), nullable=False, default="draft")  # 'draft' | 'verified'

    chapter_rel = relationship("ChapterEntity", back_populates="words")


class AppUser(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'student' | 'teacher' | 'parent' | 'admin'
    full_name = Column(String(255), nullable=True)
    class_id = Column(Integer, ForeignKey("class.class_id"), nullable=True)
    linked_student_id = Column(Integer, ForeignKey("app_user.user_id"), nullable=True)
    school_code = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    class_rel = relationship("ClassEntity", back_populates="students")
    verified_translations = relationship("TranslatedChapter", back_populates="verifier_rel")
    progress_records = relationship("StudentProgress", back_populates="student_rel")


class StudentProgress(Base):
    __tablename__ = "student_progress"

    progress_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("app_user.user_id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)
    concept_key = Column(String(100), nullable=True)
    mastery_status = Column(String(20), default="in_progress")  # 'in_progress' | 'mastered'
    error_pattern = Column(JSON, nullable=True)  # structured mistake history
    last_attempt_at = Column(DateTime, default=datetime.utcnow)

    student_rel = relationship("AppUser", back_populates="progress_records")
    chapter_rel = relationship("ChapterEntity", back_populates="progress_records")


class DeviceSyncLog(Base):
    __tablename__ = "device_sync_log"

    sync_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, index=True)
    school_code = Column(String(50), nullable=True)
    last_synced_at = Column(DateTime, default=datetime.utcnow)
    bundle_version = Column(String(20), nullable=True)
