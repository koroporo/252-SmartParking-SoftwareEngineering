from ..models.user import User
from ..models.parking_session import ParkingSession

class PDFService: 
    def __init__(self, invoice_id,user_id,session_id,amount, pdf_path = None):
        self.invoice_id = invoice_id
        self.user_id = user_id
        self.session_id = session_id
        self.amount = amount
        self.pdf_path = pdf_path

    def create_invoice_pdf(self,user: User, session: ParkingSession, amount, is_paid):
        pass

    def create_analytics_report(self):
        pass
