from ..models.user import User
from ..models.invoice import Invoice

class PaymentService: 
    def __init__(self,payment_gateway,notif_service,db):
        self.payment_gateway = payment_gateway # BKPay Client in this project
        self.notif_service = notif_service
        self.db = db

    async def process_parking_payment(self, user: User, session,amount: float) -> bool:

        # self.logger.info(f"Initiating payment of {amount} for User {user.id}")

        response = await self.payment_gateway.post_transaction(
            uid=user.id, 
            amount=amount,
            description="Parking Fee"
        )

        if response.status == "success":
            # self.logger.info(f"Payment successful for User {user.id}")
            await self.notif_service.notify_user(user, "Payment Successfull", f"Payment Successfull ! Amount : ${amount}")
            return True
        else:
            # self.logger.error(f"Payment failed for User {user.id}: {response.error}")
            return False   

    def record_debt(self,user: User,amount):
        user.debt_balance += amount
        self.db.update_user(user)

    def generate_invoice(self,user: User,sessions, is_paid):
        """ is_paid -> Label for the Invoice (True if payment suceed, False if just a notification to the user)"""
        pdf_file = self.pdf_service.create_invoice_pdf(user, sessions, user.debt_balance,is_paid)
            
        invoice = Invoice(
            user_id=user.id,
            session_id=sessions,
            amount=user.debt_balance,
            pdf_path=pdf_file
        )
        # In the DB update the invoice.is_paid to True (if already exist) or add the invoice to the DB
        self.db.update_invoice(invoice, is_paid) 
        return invoice

    def get_sessions_debt(self,user: User) -> list[str]:
        sessions = self.db.get_sessions_id("CLOSED_DEBT",user)
        self.db.update_sessions(from_status="CLOSED_DEBT",to_status="CLOSED")
        return sessions
    
    async def process_monthly_payment(self, user: User):

        if user.debt_balance > 0:
            success = await self.process_parking_payment(user, user.debt_balance)
            if success:
                user.debt_balance = 0
                self.db.update_user(user)
                sessions = self.get_sessions_debt(user)
                invoice = self.generate_invoice(user,sessions)
                await self.notif_service.notify_user(user, "Invoice", f"Invoice: {invoice}")
                return True
            return False
        return True