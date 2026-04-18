import uuid
from datetime import datetime
from typing import Dict

class BKPayClient:
    def __init__(self):
        self.gateway_url = "https://bkpay.hcmut.edu.vn/api"

    async def post_transaction(self, user_id: str, amount: float,description: str) -> Dict:
        # BKPay stuff
        return {
            "transaction_id": str(uuid.uuid4()),
            "status": "success",
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "description": description
        }
