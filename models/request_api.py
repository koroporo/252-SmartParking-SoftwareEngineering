from pydantic import BaseModel
from datetime import datetime

class EntryRequest(BaseModel):
    card_id: str
    gate_id: str
    timestamp: datetime


class ExitRequest(BaseModel):
    card_id: str
    gate_id: str
    timestamp: datetime


class SensorUpdate(BaseModel):
    slot_id: str
    status: str  # "occupied" or "free"
    timestamp: datetime