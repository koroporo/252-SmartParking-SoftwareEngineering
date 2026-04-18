import datetime

class Invoice:
    def __init__(self, invoice_id,user_id,session_id,amount, pdf_path,is_paid):
        self.invoice_id = invoice_id
        self.user_id = user_id
        self.session_id = session_id
        self.amount = amount
        self.timestamp: datetime = datetime.now()
        self.pdf_path = pdf_path
        self.is_paid = is_paid 