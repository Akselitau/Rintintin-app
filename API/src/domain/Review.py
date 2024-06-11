from typing import List
from pydantic import BaseModel

class Review(BaseModel):
    pension_id: int
    name: str
    date: str
    rating: float
    comment: str
    
    class Config:
        orm_mode: True
