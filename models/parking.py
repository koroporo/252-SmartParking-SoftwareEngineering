from typing import Dict

class ParkingSlot:
    def __init__(self, slot_id:int):
        self.id : int = slot_id
        self.is_available : bool = True # Boolean, true = free, false = occupied
        self.maintenance : bool = False

    def set_maintenance(self, state: bool):
        self.is_maintenance = state

    def set_status(self, new_state : bool):
        self.is_available = new_state

    def __str__(self):
        return f"Slot ID : {self.id} | Status : " + "Maintenance" if self.is_maintenance else ("Free" if self.is_available else "Occupied")
    
class ParkingZone:
    def __init__(self, zone_id):
        self.id: str = zone_id
        self.slots: Dict[int, ParkingSlot] = {}
        self.is_maintenance: bool = False

    def add_slot(self, slot_id: int):
        if slot_id not in self.slots:
            self.slots[slot_id] = ParkingSlot(slot_id=slot_id)
        return self.slots[slot_id]

    def set_maintenance(self, state: bool):
        self.is_maintenance = state
        for slot in self.slots.values():
            slot.set_maintenance(state)

    @property
    def free_slots_count(self) -> int:
        return len([s for s in self.slots.values() if s.is_available and not s.is_maintenance])

class Parking:
    def __init__(self,parking_id : int, slots : Dict[int, ParkingSlot]=None):
        self.id : int = parking_id
        self.zones : Dict[str, ParkingZone] = {}
        self.maintenance : bool = False

    def add_zone(self, zone_id: str):
        if zone_id not in self.zones:
            self.zones[zone_id] = ParkingZone(zone_id=zone_id)
        return self.zones[zone_id]

    def set_maintenance(self, state: bool):
        self.is_maintenance = state
        for zone in self.zones.values():
            zone.set_maintenance(state)

    def get_slot(self, slot_id: int) -> ParkingSlot:
        for zone in self.zones.values():
            if slot_id in zone.slots:
                return zone.slots[slot_id]
        return None

    @property
    def total_free_slots(self) -> int:
        return sum(zone.free_slots_count for zone in self.zones.values())

