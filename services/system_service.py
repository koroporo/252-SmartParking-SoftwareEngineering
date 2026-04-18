import datetime

from models.parking import Parking

class SystemService:
    def __init__(self, db, notif_service):
        self.db = db
        self.notif_service = notif_service

    # To Finish : Put parking state into db, allown delay maintenance

    async def set_slot_maintenance(self, slot_id: int, state: bool = True):
        slot = self.db.parking.get_slot(slot_id)
        if slot:
            slot.set_maintenance(state)
            return True
        return False

    async def set_zone_maintenance(self, zone_id: str, state: bool = True):
        zone = self.db.parking.zones.get(zone_id)
        if zone:
            zone.set_maintenance(state)
            return True
        return False

    async def set_parking_maintenance(self, parking_id,state: bool = True):
        parking = self.db.get_parking(parking_id)
        if parking:
            parking.set_maintenance(state)
            return True
        return False