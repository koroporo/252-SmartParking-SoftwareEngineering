from models.parking import ParkingSlot
import asyncio

class SensorService:
    def __init__(self, db, logging_service, notif_service):
        self.db = db
        self.logger = logging_service
        self.notif = notif_service
        self.stability_threshold = 3 

    async def update_slot_from_sensor(self, slot_id: int, sensor_occupied: bool):
        slot = self.db.parking.get_slot(slot_id)
        if not slot:
            self.logger.log_system_error("SensorService", f"Slot {slot_id} not found")
            return

        if slot.is_maintenance:
            if sensor_occupied:
                await self.notif.alert_admin("Error Maintenance", f"Slot occupied even if it should not :  {slot_id}")
                self.logger.log_audit("SYSTEM", "MAINTENANCE_VIOLATION", f"Slot {slot_id}")
            return

        if slot.is_available == sensor_occupied: 
            slot.is_available = not sensor_occupied
            
            status_text = "OCCUPIED" if sensor_occupied else "FREE"
            self.logger.log_info("SensorService", f"Slot {slot_id} is now {status_text}")
            

    def handle_malfunction(self, slot_id: int):
        """If sensor has Timeout """
        self.logger.log_system_error("SensorService", f"{slot_id} Not working")
        slot = self.db.parking.get_slot(slot_id)
        slot.set_maintenance(True)