from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class Pension(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    email: str
    max_capacity: int
    current_occupancy: int
    rating: float
    description: str
    image_urls: List[str]
    equipment: List[str]
    opening_hours: str
    distance_km: Optional[float] = 0.0
    status: str  # Ajout du champ status

    class Config:
        orm_mode = True


class PensionDetail(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    email: str
    max_capacity: int
    current_occupancy: int
    rating: float
    description: str
    image_urls: List[str]
    equipment: List[str]
    hours: str
    night_price: float
    staff: List[Dict[str, str]] = []
    reviews: List[Dict[str, Any]] = []
    status: str  # Ajout du champ status
    
    class Config:
        orm_mode = True
