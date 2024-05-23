from dataclasses import dataclass

@dataclass
class Owner:
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str