from datetime import timedelta
from typing import List
from src.infrastructure.database import Database
from psycopg2 import sql
import psycopg2


class ReservationPsqlRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    #TODO: MOVE LOGIQUE IN USECASE
    def make_reservation(self, pension_id, check_in_date, check_out_date, dog_id):
        cursor = self.conn.cursor()

        # Log the received parameters
        print(f"make_reservation called with pension_id: {pension_id}, check_in_date: {check_in_date}, check_out_date: {check_out_date}, dog_id: {dog_id}")

        cursor.execute("SELECT max_capacity FROM pensions WHERE pension_id = %s", (pension_id,))
        max_capacity = cursor.fetchone()[0]
        
        current_date = check_in_date
        while current_date < check_out_date:
            cursor.execute(
                "SELECT occupancy FROM daily_occupancy WHERE pension_id = %s AND date = %s",
                (pension_id, current_date)
            )
            result = cursor.fetchone()
            current_occupancy = result[0] if result else 0
            
            if current_occupancy >= max_capacity:
                cursor.close()
                return False
            
            current_date += timedelta(days=1)
        
        current_date = check_in_date
        while current_date < check_out_date:
            cursor.execute(
                "SELECT occupancy FROM daily_occupancy WHERE pension_id = %s AND date = %s",
                (pension_id, current_date)
            )
            result = cursor.fetchone()
            if result:
                cursor.execute(
                    "UPDATE daily_occupancy SET occupancy = occupancy + 1 WHERE pension_id = %s AND date = %s",
                    (pension_id, current_date)
                )
            else:
                cursor.execute(
                    "INSERT INTO daily_occupancy (pension_id, date, occupancy) VALUES (%s, %s, %s)",
                    (pension_id, current_date, 1)
                )
            
            current_date += timedelta(days=1)
        
        cursor.execute(
            "INSERT INTO reservations (dog_id, pension_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
            (dog_id, pension_id, check_in_date, check_out_date, 'Requested')
        )
        
        self.conn.commit()
        cursor.close()
        return True
    
    def get_reservations_by_user(self, user_id: int) -> List[dict]:
            try:
                reservation_query = sql.SQL(
                    """
                    SELECT r.reservation_id, r.dog_id, r.pension_id, r.start_date, r.end_date, r.status,
                        p.name as pension_name, d.name as dog_name, d.breed as dog_breed
                    FROM reservations r
                    JOIN dogs d ON r.dog_id = d.dog_id
                    JOIN pensions p ON r.pension_id = p.pension_id
                    WHERE d.user_id = {user_id}
                    """
                ).format(user_id=sql.Literal(user_id))

                with self.conn.cursor() as curs:
                    curs.execute(reservation_query)
                    query_results = curs.fetchall()

                reservations = []
                for row in query_results:
                    reservations.append({
                        "reservation_id": row[0],
                        "dog_id": row[1],
                        "pension_id": row[2],
                        "start_date": row[3].strftime('%Y-%m-%d'),
                        "end_date": row[4].strftime('%Y-%m-%d'),
                        "status": row[5],
                        "pension_name": row[6],
                        "dog_name": row[7],
                        "dog_breed": row[8]
                    })

                return reservations
            except psycopg2.Error as err:
                print("Error database: ", err)
                return []

    def get_reservations_by_pension(self, pension_id: int) -> List[dict]:
        try:
            reservation_query = sql.SQL(
                """
                SELECT r.reservation_id, r.dog_id, r.pension_id, r.start_date, r.end_date, r.status,
                       p.name as pension_name, d.name as dog_name, d.breed as dog_breed
                FROM reservations r
                JOIN dogs d ON r.dog_id = d.dog_id
                JOIN pensions p ON r.pension_id = p.pension_id
                WHERE r.pension_id = {pension_id}
                """
            ).format(pension_id=sql.Literal(pension_id))

            with self.conn.cursor() as curs:
                curs.execute(reservation_query)
                query_results = curs.fetchall()

            reservations = []
            for row in query_results:
                reservations.append({
                    "reservation_id": row[0],
                    "dog_id": row[1],
                    "pension_id": row[2],
                    "start_date": row[3].strftime('%Y-%m-%d'),
                    "end_date": row[4].strftime('%Y-%m-%d'),
                    "status": row[5],
                    "pension_name": row[6],
                    "dog_name": row[7],
                    "dog_breed": row[8]
                })

            return reservations
        except psycopg2.Error as err:
            print("Error database: ", err)
            return []

    def update_reservation_status(self, reservation_id: int, status: str) -> bool:
        try:
            update_query = sql.SQL(
                """
                UPDATE reservations
                SET status = {status}
                WHERE reservation_id = {reservation_id}
                """
            ).format(
                status=sql.Literal(status),
                reservation_id=sql.Literal(reservation_id)
            )

            with self.conn.cursor() as curs:
                curs.execute(update_query)
                self.conn.commit()

            return True
        except psycopg2.Error as err:
            print("Error updating reservation status: ", err)
            return False