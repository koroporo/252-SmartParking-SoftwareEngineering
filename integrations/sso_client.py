import httpx
from typing import Optional, Dict

class SSOClient:
    def __init__(self):
        self.base_url = "https://sso.hcmut.edu.vn/api"

    async def verify_credentials(self, username,password: str) -> Optional[str]:
        """
        Validates the SSO token and returns the unique identifier (student_id/staff_id).
        """

        ### MOCK-UP
        mock_cred = {
            "student_123": "STU001",
            "lecturer_456": "LEC007",
            "admin_789": "ADM007",
            "visitor_135": "VIS007",
        }
    
        if password in mock_cred:
            return mock_cred[password]
        ###
        
        ### Real logic
        # response = await httpx.get(f"{self.base_url}/verify?ticket={token}")
        # return response.json().get("user_id") if response.status_code == 200 else None
        
        return None