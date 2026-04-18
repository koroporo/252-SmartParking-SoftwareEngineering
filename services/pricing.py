from ..models.parking_session import ParkingSession
from ..models.user import User

class PricingService:
    def __init__(self, payment_service, config):
        self.payment_service = payment_service # PaymentService
        self.config = config # base tarif

    def calculate_gross_fee(self, duration) -> float:
        gross_amount = duration * self.config.BASE_RATE
        return round(gross_amount, 2)
    
    def apply_discount(self,gross_amount,user: User):
        discount_factor = user.get_discount_rate() 
        final_amount = gross_amount * (1 - discount_factor)
        return round(final_amount, 2)
    
    def calculate_fee(self,duration,user:User) -> float:
        gross_fee = self.calculate_gross_fee(duration)
        return self.apply_discount(gross_fee,user)

    async def finalize_billing(self, session: ParkingSession, user: User):
        amount = self.calculate_fee(session.duration, user)
        if amount <= 0:
            return True, 0

        if user.is_monthly_billing:
            self.payment_service.record_debt(user,amount)
            session.is_paid = False
            return True, amount
        else:
            success = await self.payment_service.process_parking_payment(user, amount)
            if success : 
                invoice = self.payment_service.generate_invoice(user,[session])
                await self.notif_service.notify_user(user, "Invoice", f"Invoice: {invoice}")
                session.is_paid = True
            return success,amount
