from dataclasses import dataclass

@dataclass
class Staff:
    id: str
    pension_id: str
    certification_id: str
    first_name: str
    last_name: str
    role: str  #TODO: change for Enum
    email: str
    phone: str
