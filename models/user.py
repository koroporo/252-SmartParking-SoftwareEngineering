from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    LECTURER = "lecturer"
    VISITOR = "visitor"
    OFFICER = "officer"
    ADMIN = "admin"

class User:
    def __init__(self,id : int,rfid_tag : int,full_name : str,role : UserRole, 
                 is_monthly_billing: bool,debt_balance: float, mail):
        self.id : int = id
        self.full_name : str = full_name
        self.rfid_tag : int = rfid_tag 
        self.role : UserRole = role 
        self.is_monthly_billing: bool = is_monthly_billing
        self.debt_balance: float = debt_balance
        self.mail = mail

    # Will be Override
    def get_priority(self) -> int:
        return 0
    
    def __str__(self):
        return f"[{self.role.upper()}] FULL NAME: {self.full_name} | ID: {self.id} | RFID: {self.rfid_tag}"

class Visitor(User):
    def __init__(
            self,id : int,rfid_tag : int,full_name : str,token: str):
        super.__init__(id,rfid_tag,full_name,UserRole.VISITOR,False,0)
        self.token : str = token 

class Student(User):
    def __init__(
            self,id : int,rfid_tag : int,full_name : str,
            is_monthly_billing: bool,debt_balance: float,student_id: str):
        super.__init__(id,rfid_tag,full_name,UserRole.STUDENT,is_monthly_billing,debt_balance)
        self.student_id : str = student_id

    def get_priority(self) -> int:
        return 1

class Lecturer(User):
    def __init__(
            self,id : int,rfid_tag : int,full_name : str,
            is_monthly_billing: bool,debt_balance: float,department: str):
        super.__init__(id,rfid_tag,full_name,UserRole.LECTURER,is_monthly_billing,debt_balance)
        self.department : str = department

    def get_priority(self) -> int:
        return 2

class Officer(User):
    def __init__(
            self,id : int,rfid_tag : int,full_name : str,
            is_monthly_billing: bool,debt_balance: float):
        super.__init__(id,rfid_tag,full_name,UserRole.OFFICER,is_monthly_billing,debt_balance)

    def get_priority(self) -> int:
        return 2
    
class Admin(User):
    def __init__(self, id: int, rfid_tag: int, full_name: str, 
                 is_monthly_billing: bool, debt_balance: float, mail: str):
        super().__init__(id, rfid_tag, full_name, UserRole.ADMIN, is_monthly_billing, debt_balance, mail)

    def get_priority(self) -> int:
        return 3 
