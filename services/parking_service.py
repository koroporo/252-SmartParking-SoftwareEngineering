import datetime

from models.user import User
from models.parking_session import ParkingSession
from utils.rbac import check_permission
from pricing import PricingService

class ParkingService:
    def __init__(self, db, pricing_service: PricingService):
        self.db = db
        self.pricing_service = pricing_service

    def assign_slot(self,user : User):
        """ Look for the best places """
        priority = user.get_priority()
        if priority >= 2:
            slot = self.db.find_free_slot(zone="STAFF")
        elif priority == 1:
            slot = self.db.find_free_slot(zone="LECTURER")
        else:
            slot = self.db.find_free_slot(zone="GENERAL")
        return slot


    def handle_entry(self,user: User):
        if not check_permission(user, "entry"):
            print("Entry denied !")
            return None,None
        
        slot = self.assign_slot(user)
        if not slot:
            print("Parking full !")
            return None, None
        
        session = ParkingSession(user,slot)
        self.db.update_slot_status(slot.slot_id, is_available=False)
        self.db.save_session(session)
        return slot, session

    def handle_exit(self,session: ParkingSession):
        exit_time = datetime.now()
        duration = session.calculateDuration(exit_time)
        fee = self.pricing_service.calculate_fee(duration, session.user)

        self.db.update_slot_status(session.slot_id, is_available=True)
        self.db.update_session(session)
        
        return fee

