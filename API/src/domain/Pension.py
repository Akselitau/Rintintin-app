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
    image_url: str 

    class Config:
        orm_mode: True
