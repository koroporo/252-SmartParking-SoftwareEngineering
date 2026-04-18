import datetime
from user import User

class ParkingSession:
    def __init__(self, user: User, slot_id : str):
        self.user: User = user
        self.entry_time: datetime = datetime.now()
        self.slot_id: str = slot_id
        self.fee: float = 0
        self.duration = 0
        self.is_paid = False

    def calculateDuration(self,exit_time: datetime) -> float: 
        """ Return the duration of the parking sessions in minutes (float) """
        duration = exit_time - self.entry_time
        self.duration = duration.total_seconds() / 60
        return self.duration
