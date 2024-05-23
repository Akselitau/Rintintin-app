from typing import List
from src.domain.Pension import Pension
from psycopg2 import sql
import psycopg2

class PsqlPensionRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
    
    def get_all_pensions(self) -> List[Pension]:
        try:
            pension_query = sql.SQL(
                """
                SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_url
                FROM pensions
                """
            )
            with self.conn.cursor() as curs:
                curs.execute(pension_query)
                query_results = curs.fetchall()
                
            pensions = []
            for row in query_results:
                pensions.append(Pension(
                    id=row[0], 
                    name=row[1],
                    address=row[2], 
                    phone=row[3], 
                    email=row[4], 
                    max_capacity=row[5], 
                    current_occupancy=row[6],
                    rating=row[7],  # Nouvelle colonne
                    description=row[8],  # Nouvelle colonne
                    image_url=row[9]  # Nouvelle colonne
                ))
            
            return pensions
        except psycopg2.Error as err:
            print("Error database: ", err)
            
    def get_pension_by_id(self, id: int) -> Pension:
        try:
            pension_query = sql.SQL(
                """
                SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_url
                FROM pensions
                WHERE pension_id = {id}
                """
            ).format(id=sql.Literal(id))
            with self.conn.cursor() as curs:
                curs.execute(pension_query)
                query_result = curs.fetchone()
            return Pension(
                id=query_result[0], 
                name=query_result[1],
                address=query_result[2], 
                phone=query_result[3], 
                email=query_result[4], 
                max_capacity=query_result[5], 
                current_occupancy=query_result[6],
                rating=query_result[7],
                description=query_result[8], 
                image_url=query_result[9] 
            )
        except psycopg2.Error as err:
            print("Error database: ", err)
