from ..models.user import User, UserRole

import asyncio

class NotificationService:
    def __init__(self,smtp_config):
        self.smtp_config = smtp_config # Contains all needed to send an email
        self.system_email = "noreply@smartparking.hcmut.edu.vn"

    def _send_email(self,users: list[User],subject,body):
        # Here would be the use of a lib to send an email. Not coded yet
        print(f"Mail Send !")

    async def notify_user(self, user: User, subject: str, message: str):
        await self._send_email(user.mail, subject, message)

    async def notify_group(self, role: UserRole, subject: str, message: str):
        users = self.db.get_users_by_role(role)
        tasks = [self._send_email(u.mail, subject, message) for u in users]
        await asyncio.gather(*tasks)

    async def broadcast_maintenance(self, area: str, start_time: str):
        users = self.db.get_all_users()
        subject = f"Maintenance Parking - Zone {area}"
        message = f"The parking will be under maintenance starting from : {start_time}."
        
        tasks = [self._send_email(u.mail, subject, message) for u in users]
        await asyncio.gather(*tasks)

    async def alert_admin(self,error_type: str, details: str):
        admins = self.db.get_users_by_role(UserRole.OFFICER)
        subject = f"SYSTEM ALERT : {error_type}"
        for admin in admins: # No need of asyncio here because there is no thousand of admins
            await self._send_email(admin.mail, subject, details)