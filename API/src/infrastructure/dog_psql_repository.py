from typing import List
from src.domain.Dog import Dog
from psycopg2 import sql
import psycopg2

DATABASE_URL = "dbname=doggydb user=aksel host=localhost password=changeme"


class PsqlDogRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
    

    def get_all_dogs(self) -> List[Dog]:
        try:
            dog_query = sql.SQL(
                """
            SELECT dog_id, owner_id, name, breed, age, weight, special_needs
            FROM dogs
            """
            )
            with self.conn.cursor() as curs:
                curs.execute(dog_query)
                query_results = curs.fetchall()
                
            dogs = []
            for row in query_results:
                dogs.append(Dog(
                    id=row[0], 
                    owner_id=row[1],
                    name=row[2], 
                    breed=row[3], 
                    age=row[4], 
                    weight=row[5], 
                    special_needs=row[6]))
            return dogs
        except psycopg2.Error as err:
            print("Error database: ", err)
            
    def get_dog_by_id(self, id: int) -> Dog:
        try:
            dog_query = sql.SQL(
                """
            SELECT dog_id, owner_id, name, breed, age, weight, special_needs
            FROM dogs
            WHERE dog_id = {id}
            """
            ).format(id=sql.Literal(id))
            with self.conn.cursor() as curs:
                curs.execute(dog_query)
                query_result = curs.fetchone()
            return Dog(
                    id=query_result[0], 
                    owner_id=query_result[1],
                    name=query_result[2], 
                    breed=query_result[3], 
                    age=query_result[4], 
                    weight=query_result[5], 
                    special_needs=query_result[6])
        except psycopg2.Error as err:
            print("Error database: ", err)