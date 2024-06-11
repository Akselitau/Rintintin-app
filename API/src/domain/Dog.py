from typing import List, Optional
from pydantic import BaseModel

class Dog(BaseModel):
    dog_id: int
    user_id: int
    name: str
    breed: str
    profile_photo_url: Optional[str] = None
    information: Optional[str] = None

    class Config:
        orm_mode = True
