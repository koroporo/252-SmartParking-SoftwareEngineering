from fastapi import APIRouter, HTTPException
from models.request_api import parking_slots, active_sessions

router = APIRouter()

@router.get("/status")
async def get_status():
    total = len(parking_slots)
    occupied = sum(1 for s in parking_slots.values() if s == "occupied")

    return {
        "total_slots": total,
        "occupied": occupied,
        "available": total - occupied
    }