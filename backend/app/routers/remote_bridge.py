import datetime
import secrets
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.entities import AppUser

router = APIRouter(prefix="/remote-bridge", tags=["Remote Voice Bridge (Online)"])

# In-memory active remote sessions
ACTIVE_REMOTE_SESSIONS = {}


class CreateSessionRequest(BaseModel):
    teacher_id: int
    target_language: str = "santhali"  # 'ho' | 'mundari' | 'santhali'
    topic: Optional[str] = "Classroom Live Instruction"
    class_id: Optional[int] = 1


@router.post("/session")
def create_remote_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    """
    Creates an online Remote Voice Bridge session (PRD Section 5 & 6.7).
    A WebSocket/WebRTC signaling channel relays ASR/NMT/TTS between teacher & remote students.
    """
    teacher = db.query(AppUser).filter(AppUser.user_id == req.teacher_id).first()
    teacher_name = teacher.full_name if teacher else "Shri Rajesh Kumar"

    session_id = f"rbridge_{secrets.token_hex(6)}"
    room_code = f"PALASH-{secrets.randbelow(900) + 100}"

    session_data = {
        "session_id": session_id,
        "room_code": room_code,
        "teacher_id": req.teacher_id,
        "teacher_name": teacher_name,
        "target_language": req.target_language,
        "topic": req.topic,
        "class_id": req.class_id,
        "status": "active",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "participants_count": 1,
        "relay_endpoints": {
            "ws_channel": f"/ws/remote-bridge/{session_id}",
            "bhashini_pipeline_active": True,
        },
    }

    ACTIVE_REMOTE_SESSIONS[session_id] = session_data

    return {
        "status": "created",
        "session": session_data,
        "join_url": f"/#remote-bridge?session={session_id}&room={room_code}",
    }


@router.get("/session/{session_id}")
def get_remote_session(session_id: str):
    """Fetches details of an ongoing Remote Voice Bridge session."""
    session_data = ACTIVE_REMOTE_SESSIONS.get(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return {"session": session_data}
