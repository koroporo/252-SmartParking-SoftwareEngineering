import logging
from datetime import datetime

class LoggingService:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler("smart_parking.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SmartParking")

    def log_transaction(self, user_id, amount, status):
        """Financial log"""
        msg = f"[TRANSACTION] User: {user_id} | Amount: {amount} | Status: {status}"
        self.logger.info(msg)

    def log_audit(self, admin_user, action, details):
        """Admin Log """
        msg = f"[AUDIT] Admin: {admin_user.id} | Action: {action} | Details: {details}"
        self.logger.warning(msg)

    def log_system_error(self, service_name, error):
        """System error log"""
        msg = f"[SYSTEM_ERROR] Service: {service_name} | Error: {str(error)}"
        self.logger.error(msg)