from dataclasses import dataclass

@dataclass
class Dog:
    id: int
    owner_id: int
    name: str
    breed: str
    age: int
    weight: int
    special_needs: str 

