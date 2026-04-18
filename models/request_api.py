from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- INPUT SCHEMAS ---

class EntryRequest(BaseModel):
    card_id: str = Field(..., description="RFID ID or QR Code")
    gate_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ExitRequest(BaseModel):
    card_id: str
    gate_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class SensorUpdate(BaseModel):
    slot_id: str
    status: str  # "occupied" ou "free"
    timestamp: datetime

# --- OUTPUT SCHEMAS ---

class AccessResponse(BaseModel): # Entry
    access_granted: bool
    slot_assigned: Optional[str] = None
    user_name: Optional[str] = None
    message: str
    display_message: str

class PaymentSummary(BaseModel): # Exit
    session_id: str
    duration_minutes: int
    fee: float
    payment_status: str