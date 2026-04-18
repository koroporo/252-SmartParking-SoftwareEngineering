from fastapi import HTTPException, status

from models.user import Student, Lecturer, Visitor, Officer, Admin,UserRole
from integrations.sso_client import SSOClient
from integrations.datacore_client import DataCoreClient

class AuthenticationService:
    def __init__(self, db, sso_client: SSOClient, datacore_client: DataCoreClient):
        self.db = db
        self.sso_client = sso_client
        self.datacore_client = datacore_client

    async def authenticate_via_rfid(self, rfid_tag: str):
        user = await self.datacore.get_user_profile_by_rfid(rfid_tag)
        if not user:
            raise HTTPException(status_code=401, detail="Unknown Card RFID")
        return self._map_to_user_model(user)

    async def authenticate_via_sso(self, username, password):
        user_id = await self.sso_client.verify_credentials(username, password)
        if not user_id:
            return None
        
        user = await self.datacore.get_user_profile(user_id)
        if not user:
            return None
        
        return self._map_to_user_model(user)
    
    def _map_to_user_model(self, profile: dict):
        """
        DataCore answer to User model
        """
        role = profile["role"].lower()
        user = self.db.get_user(profile["id"])

        # profile is read-only (DataCore) while user can be use to update student data
        if role == UserRole.STUDENT:
            return Student(
                id=profile["id"], 
                rfid_tag=profile["rfid_tag"], 
                full_name=profile["name"],
                is_monthly_billing=user["is_monthly_billing"],
                debt_balance=user["debt_balance"],
                student_id=profile.get("student_id", "N/A"),
                mail=profile.get("mail","N/A")
            )
        
        elif role == UserRole.LECTURER:
            return Lecturer(
                id=profile["id"], 
                rfid_tag=profile["rfid_tag"], 
                full_name=profile["name"],
                is_monthly_billing=user["is_monthly_billing"],
                debt_balance=user["debt_balance"],
                mail=profile.get("mail","N/A"),
                department=profile.get("department")
            )
        
        elif role == UserRole.OFFICER:
            return Officer(
                id=profile["id"], 
                rfid_tag=profile["rfid_tag"], 
                full_name=profile["name"],
                is_monthly_billing=user["is_monthly_billing"],
                debt_balance=user["debt_balance"],
                mail=profile.get("mail","N/A"),
            )
        
        return Admin(
            id=profile["id"], 
                rfid_tag=profile["rfid_tag"], 
                full_name=profile["name"],
                is_monthly_billing=user["is_monthly_billing"],
                debt_balance=user["debt_balance"],
                mail=profile.get("mail","N/A"),
        )
    
    async def issue_visitor_access(self, ticket_id: int) -> Visitor:
        return Visitor(
            id=ticket_id,
            rfid_tag=ticket_id,
            full_name="Visitor",
            token=f"TICKET_{ticket_id}"
        )

    async def verify_access(self, user_id: str, user_role: UserRole):
        user = self.datacore.get_user_profile(user_id)
        if user["role"] != user_role:
            raise HTTPException(status_code=403, detail="Access Denied")
        return True
    