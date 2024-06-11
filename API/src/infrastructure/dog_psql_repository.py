from typing import List
from src.domain.Dog import Dog
from src.infrastructure.database import Database

class DogPsqlRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    def create_dog_profile(self, user_id: int, name: str, breed: str, profile_photo_url: str, information: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO dogs (user_id, name, breed, profile_photo_url, information) VALUES (%s, %s, %s, %s, %s) RETURNING dog_id",
            (user_id, name, breed, profile_photo_url, information)
        )
        dog_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return dog_id
    
    def get_dogs_by_user(self, user_id: int) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT dog_id, user_id, name, breed, profile_photo_url, information FROM dogs WHERE user_id = %s",
            (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()

        dogs = []
        for row in rows:
            dog = {
                "dog_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "breed": row[3],
                "profile_photo_url": row[4],
                "information": row[5]
            }
            dogs.append(dog)
        return dogs
