from fastapi import APIRouter, HTTPException
from models.request_api import EntryRequest,parking_slots, active_sessions

router = APIRouter()

@router.post("/entry")
async def record_entry(data: EntryRequest):
    if data.card_id in active_sessions:
        raise HTTPException(status_code=400, detail="User already inside")

    # Simulate slot assignment
    assigned_slot = None
    for slot, status in parking_slots.items():
        if status == "free":
            assigned_slot = slot
            break

    if not assigned_slot:
        raise HTTPException(status_code=400, detail="Parking full")

    # Update slot
    parking_slots[assigned_slot] = "occupied"

    # Create session
    active_sessions[data.card_id] = {
        "entry_time": data.timestamp,
        "slot_id": assigned_slot
    }

    return {
        "status": "granted",
        "slot_assigned": assigned_slot
    }