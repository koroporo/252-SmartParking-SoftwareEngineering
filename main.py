from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict

from api import entry, exit, sensor, status

app = FastAPI(title="Smart Parking API")

# Database

parking_slots: Dict[str, str] = {}       # slot_id -> status
active_sessions: Dict[str, dict] = {}    # card_id -> session data

# Router

app.include_router(entry.router)
app.include_router(exit.router)
app.include_router(sensor.router)
app.include_router(status.router)