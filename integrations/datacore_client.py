from typing import Optional, Dict

class DataCoreClient:
    def __init__(self):
        # Configuration read-only 
        self.source = "HCMUT_DATACORE"

    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get Data on the user
        """
        ### Mock-up
        mock_database = {
            "STU001": {"name": "Martin Mystere", "role": "student", "faculty": "CSE","mail":"martin.mystere@mail.com"},
            "STAFF007": {"name": "Dr. Tran", "role": "lecturer", "faculty": "CSE","mail":"kevin.tran@mail.com"},
            "ADM007": {"name": "John Doe", "role": "admin", "faculty": None,"mail":"john.doe@mail.com"},
            "OFF007": {"name": "Alice Bam", "role": "officer", "faculty": None,"mail":"alice.bam@mail.com"},
            "EXT999": {"name": "Visitor", "role": "visitor", "faculty": None,"mail":None}
        }

        profile = mock_database.get(user_id)
        if profile:
            return profile.copy() # Copy because read-only
        return None