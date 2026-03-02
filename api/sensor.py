from fastapi import APIRouter, HTTPException
from models.request_api import SensorUpdate,parking_slots, active_sessions

router = APIRouter()

@router.post("/sensor/update")
async def update_sensor(data: SensorUpdate):
    if data.status not in ["occupied", "free"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    parking_slots[data.slot_id] = data.status

    return {
        "slot_id": data.slot_id,
        "new_status": data.status
    }