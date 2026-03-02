from fastapi import APIRouter, HTTPException
from models.request_api import ExitRequest,parking_slots, active_sessions

router = APIRouter()

@router.post("/exit")
async def record_exit(data: ExitRequest):
    if data.card_id not in active_sessions:
        raise HTTPException(status_code=404, detail="No active session found")

    session = active_sessions[data.card_id]

    # Free slot
    parking_slots[session["slot_id"]] = "free"

    # Calculate duration
    duration = (data.timestamp - session["entry_time"]).total_seconds() / 3600

    # Simple fee calculation
    fee = round(duration * 5, 2)  # 5 units per hour

    # Remove session
    del active_sessions[data.card_id]

    return {
        "status": "exit recorded",
        "duration_hours": round(duration, 2),
        "fee": fee
    }