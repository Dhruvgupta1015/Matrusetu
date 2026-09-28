import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.entities import (
    StudentProgress,
    AppUser,
    ChapterEntity,
    ClassEntity,
)

router = APIRouter(prefix="/progress", tags=["Student FLN Progress & Heatmap"])


class AttemptRequest(BaseModel):
    student_id: int
    chapter_id: int
    concept_key: str
    mastery_status: str = "in_progress"  # 'in_progress' | 'mastered'
    error_pattern: Optional[Dict[str, Any]] = None
    accuracy_pct: Optional[int] = 85
    stars: Optional[int] = 3


@router.post("/attempt")
def log_student_attempt(req: AttemptRequest, db: Session = Depends(get_db)):
    """
    Logs a Bhasha Mitr test or practice attempt.
    Updates the student_progress table with structured error patterns.
    """
    student = db.query(AppUser).filter(AppUser.user_id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    chapter = db.query(ChapterEntity).filter(ChapterEntity.chapter_id == req.chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Update existing record for this student and concept or create new
    progress = (
        db.query(StudentProgress)
        .filter(
            StudentProgress.student_id == req.student_id,
            StudentProgress.chapter_id == req.chapter_id,
            StudentProgress.concept_key == req.concept_key,
        )
        .first()
    )

    now = datetime.datetime.now(datetime.timezone.utc)
    err_data = req.error_pattern or {}
    err_data["last_accuracy_pct"] = req.accuracy_pct
    err_data["stars"] = req.stars

    if progress:
        progress.mastery_status = req.mastery_status
        progress.error_pattern = err_data
        progress.last_attempt_at = now
    else:
        progress = StudentProgress(
            student_id=req.student_id,
            chapter_id=req.chapter_id,
            concept_key=req.concept_key,
            mastery_status=req.mastery_status,
            error_pattern=err_data,
            last_attempt_at=now,
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)

    return {
        "status": "logged",
        "progress_id": progress.progress_id,
        "student_id": progress.student_id,
        "concept_key": progress.concept_key,
        "mastery_status": progress.mastery_status,
        "last_attempt_at": progress.last_attempt_at.isoformat(),
    }


@router.get("/student/{student_id}")
def get_student_progress(student_id: int, db: Session = Depends(get_db)):
    """Teacher view: individual student's progress and error patterns."""
    student = db.query(AppUser).filter(AppUser.user_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    records = (
        db.query(StudentProgress)
        .filter(StudentProgress.student_id == student_id)
        .order_by(StudentProgress.last_attempt_at.desc())
        .all()
    )

    total_mastered = sum(1 for r in records if r.mastery_status == "mastered")
    total_in_progress = sum(1 for r in records if r.mastery_status == "in_progress")

    return {
        "student": {
            "user_id": student.user_id,
            "full_name": student.full_name,
            "phone_number": student.phone_number,
            "class_id": student.class_id,
        },
        "summary": {
            "total_attempts": len(records),
            "mastered_concepts": total_mastered,
            "in_progress_concepts": total_in_progress,
            "fln_completion_pct": int((total_mastered / max(len(records), 1)) * 100),
        },
        "history": [
            {
                "progress_id": r.progress_id,
                "chapter_id": r.chapter_id,
                "chapter_title": r.chapter_rel.title if r.chapter_rel else "",
                "concept_key": r.concept_key,
                "mastery_status": r.mastery_status,
                "error_pattern": r.error_pattern,
                "last_attempt_at": r.last_attempt_at.isoformat() if r.last_attempt_at else None,
            }
            for r in records
        ],
    }


@router.get("/class/{class_id}/heatmap")
def get_class_weak_topic_heatmap(class_id: int, db: Session = Depends(get_db)):
    """
    Teacher view: Class-wide weak-topic heatmap.
    Returns matrix of students x concepts with mastery status,
    enabling teachers to prioritize weekly mother-tongue focus areas.
    """
    c_entity = db.query(ClassEntity).filter(ClassEntity.class_id == class_id).first()
    if not c_entity:
        raise HTTPException(status_code=404, detail="Class not found")

    students = db.query(AppUser).filter(
        AppUser.class_id == class_id,
        AppUser.role == "student"
    ).all()

    # Predefined curriculum concepts for Class 1-5
    key_concepts = [
        {"key": "L-FLN-01: Oral Family Dialogue", "domain": "Oral Language", "weight": 1},
        {"key": "L-FLN-02: Phonics & Letter Matching", "domain": "Phonics", "weight": 2},
        {"key": "E-FLN-01: Plants & Nature", "domain": "EVS", "weight": 1},
        {"key": "M-FLN-01: Number Sense 1-10", "domain": "Math", "weight": 2},
        {"key": "L-FLN-04: Folk Narrative", "domain": "Literature", "weight": 1},
    ]

    heatmap_rows = []
    concept_summary = {c["key"]: {"mastered": 0, "in_progress": 0, "needs_support": 0} for c in key_concepts}

    for s in students:
        s_records = db.query(StudentProgress).filter(StudentProgress.student_id == s.user_id).all()
        rec_map = {r.concept_key: r for r in s_records}

        student_scores = []
        for c in key_concepts:
            r = rec_map.get(c["key"])
            if r:
                status = r.mastery_status
                err_count = len(r.error_pattern.get("errors", [])) if r.error_pattern else 0
                student_scores.append({
                    "concept_key": c["key"],
                    "status": status,
                    "accuracy_pct": r.error_pattern.get("last_accuracy_pct", 85) if r.error_pattern else 70,
                    "error_count": err_count,
                })
                if status == "mastered":
                    concept_summary[c["key"]]["mastered"] += 1
                elif err_count > 1:
                    concept_summary[c["key"]]["needs_support"] += 1
                else:
                    concept_summary[c["key"]]["in_progress"] += 1
            else:
                student_scores.append({
                    "concept_key": c["key"],
                    "status": "untested",
                    "accuracy_pct": 0,
                    "error_count": 0,
                })

        heatmap_rows.append({
            "student_id": s.user_id,
            "student_name": s.full_name or f"Student {s.user_id}",
            "concepts": student_scores,
        })

    # Find the top weak concepts for teacher recommendation
    weakest_concepts = sorted(
        key_concepts,
        key=lambda c: concept_summary[c["key"]]["needs_support"] + concept_summary[c["key"]]["in_progress"],
        reverse=True
    )
    recommended_focus = weakest_concepts[0]["key"] if weakest_concepts else "L-FLN-02: Phonics & Letter Matching"

    return {
        "class_id": class_id,
        "class_name": c_entity.class_name,
        "total_students": len(students),
        "concepts": key_concepts,
        "concept_aggregate": concept_summary,
        "recommended_focus_chapter": recommended_focus,
        "matrix": heatmap_rows,
    }
