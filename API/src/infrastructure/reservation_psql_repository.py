from typing import List
from chalicelib.domain.Reservation import Reservation
from psycopg2 import sql
import psycopg2

class PsqlReservationRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
        
    def get_all_reservations(self) -> List[Reservation]:
        try:
            reservation_query = sql.SQL(
                """
                SELECT id, dog_id, pension_id, start_date, end_date, special_requests
                FROM reservations
                """
            )
            with self.conn.cursor() as curs:
                curs.execute(reservation_query)
                query_results = curs.fetchall()
                    
            reservations = []
            for row in query_results:
                reservations.append(Reservation(
                    id=row[0], 
                    dog_id=row[1],
                    pension_id=row[2], 
                    start_date=row[3],
                    end_date=row[4], 
                    special_requests=row[5]))
            
            return reservations
        except psycopg2.Error as err:
            print("Error database: ", err)
        
    def get_reservation_by_id(self, id: int) -> Reservation:
        try:
            reservation_query = sql.SQL(
                """
                SELECT id, dog_id, pension_id, start_date, end_date, special_requests
                FROM reservations
                WHERE id = {id}
                """
            ).format(id=sql.Literal(id))
            with self.conn.cursor() as curs:
                curs.execute(reservation_query)
                query_result = curs.fetchone()
                    
            return Reservation(
                id=query_result[0], 
                dog_id=query_result[1],
                pension_id=query_result[2], 
                start_date=query_result[3],
                end_date=query_result[4], 
                special_requests=query_result[5])
        
        except psycopg2.Error as err:
            print("Error database: ", err)