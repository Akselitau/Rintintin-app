from dataclasses import dataclass

@dataclass
class Reservation:
    id: str
    dog_id: str
    pension_id: str
    start_date: str
    end_date: str
    status: str  #TODO: change for Enum
    comment: str