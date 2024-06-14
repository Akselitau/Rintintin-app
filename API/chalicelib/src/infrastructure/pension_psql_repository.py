from datetime import datetime
from typing import Any, Dict, List
from psycopg2 import sql
import psycopg2
from chalicelib.src.infrastructure.database import Database
from chalicelib.src.domain.Pension import Pension, PensionDetail
from chalicelib.src.domain.Reservation import Reservation
from chalice import Response
from chalicelib.src.geocoding_service import get_coordinates

class PsqlPensionRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    def get_all_pensions(self) -> List[Pension]:
        try:
            pension_query = sql.SQL(
                """
                SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours AS opening_hours
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
                    rating=row[7],
                    description=row[8],
                    image_urls=row[9],
                    equipment=row[10],
                    opening_hours=row[11],
                    distance_km=0.0  # Valeur par défaut pour distance_km
                ))

            return pensions
        except psycopg2.Error as err:
            print("Error database: ", err)
            return []

    def get_pension_by_user_id(self, user_id: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours 
                    FROM pensions 
                    WHERE user_id = %s""",
                    (user_id,)
                )
                pension = cursor.fetchone()

            if pension:
                pension_data = {
                    "pension_id": pension[0],
                    "name": pension[1],
                    "address": pension[2],
                    "phone": pension[3],
                    "email": pension[4],
                    "max_capacity": pension[5],
                    "current_occupancy": pension[6],
                    "rating": pension[7],
                    "description": pension[8],
                    "image_urls": pension[9],
                    "equipment": pension[10],
                    "hours": pension[11],
                    "distance_km": 0.0  # Valeur par défaut pour distance_km
                }
                return {"pension": pension_data}
            else:
                return {"message": "Pension not found"}

        except psycopg2.Error as err:
            print(f"Error database: {err}")
            return {"message": f"An error occurred: {err}"}

    def get_pension_by_id(self, id: int) -> PensionDetail:
        try:
            pension_query = sql.SQL(
                """
                SELECT 
                    p.pension_id, p.name, p.address, p.phone, p.email, p.max_capacity, 
                    p.current_occupancy, p.rating, p.description, p.image_urls,
                    p.equipment, p.hours, p.night_price,
                    s.first_name, s.role, s.image_url,
                    r.name, r.date, r.rating, r.comment
                FROM pensions p
                LEFT JOIN staff s ON p.pension_id = s.pension_id
                LEFT JOIN reviews r ON p.pension_id = r.pension_id
                WHERE p.pension_id = {id}
                """
            ).format(id=sql.Literal(id))

            with self.conn.cursor() as curs:
                curs.execute(pension_query)
                query_result = curs.fetchall()

            if not query_result:
                return None

            pension_data = query_result[0]
            staff_members = []
            reviews = []

            for row in query_result:
                print("Processing row:", row)  # Debugging print

                if row[13]:  # Check if staff first_name exists
                    staff_members.append({
                        "first_name": row[13],
                        "role": row[14],
                        "image_url": row[15]
                    })
                if row[16]:  # Check if review name exists
                    review_date = row[17]
                    if isinstance(review_date, datetime):
                        review_date_str = review_date.strftime('%Y-%m-%d')
                    else:
                        review_date_str = None

                    reviews.append({
                        "name": row[16],
                        "date": review_date_str,
                        "rating": row[18],
                        "comment": row[19]
                    })

            pension = PensionDetail(
                id=pension_data[0],
                name=pension_data[1],
                address=pension_data[2],
                phone=pension_data[3],
                email=pension_data[4],
                max_capacity=pension_data[5],
                current_occupancy=pension_data[6],
                rating=pension_data[7],
                description=pension_data[8],
                image_urls=pension_data[9],
                equipment=pension_data[10],
                hours=pension_data[11],
                night_price=pension_data[12],
                staff=staff_members,
                reviews=reviews
            )

            return pension

        except psycopg2.Error as err:
            print("Error database: ", err)
            return None



    def create_pension_profile(self, user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pensions (user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING pension_id",
                    (user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price)
                )
                pension_id = cursor.fetchone()[0]
                self.conn.commit()
            return pension_id
        except psycopg2.Error as err:
            print("Error database: ", err)
            return None

    def update_pension(self, pension: PensionDetail):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE pensions SET name = %s, address = %s, phone = %s, email = %s, max_capacity = %s, rating = %s, description = %s, equipment = %s, hours = %s, night_price = %s WHERE pension_id = %s",
                    (pension.name, pension.address, pension.phone, pension.email, pension.max_capacity, pension.rating, pension.description, pension.equipment, pension.hours, pension.night_price, pension.id)
                )
                self.conn.commit()
            return True
        except psycopg2.Error as err:
            print("Error database: ", err)
            return False
