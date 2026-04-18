from fastapi import APIRouter, HTTPException
from models.request_api import EntryRequest,parking_slots, active_sessions
from database.memory_db import db

router = APIRouter()

@router.post("/entry")
async def record_entry(data: EntryRequest):
    user = db.get_user_by_rfid(data.card_id)
    if not user:
        raise HTTPException(status_code=404, detail="Unknown RFID Tag")
    
    if db.is_user_in_session(user.id):
        raise HTTPException(status_code=400, detail="User already inside")

    assigned_slot = db.parking.get_first_free_slot()
    
    if not assigned_slot:
        raise HTTPException(status_code=400, detail="Parking full")

    db.parking.update_slot_status(assigned_slot.slot_id, status=False)
    db.create_session(user.id, assigned_slot.slot_id, data.timestamp)

    return {
        "status": "granted",
        "user_name": user.full_name,
        "role": user.role,
        "slot_assigned": assigned_slot.slot_id,
        "priority_level": user.get_priority()
    }