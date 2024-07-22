from datetime import datetime
from typing import Any, Dict, List
import psycopg2
from chalicelib.src.infrastructure.database import Database
from chalicelib.src.domain.Pension import Pension, PensionDetail
from chalicelib.src.domain.Reservation import Reservation
from chalice import Response
from chalicelib.src.utils import get_coordinates

class PsqlPensionRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    def get_all_pensions(self) -> List[Pension]:
        try:
            query = """
                SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours AS opening_hours, status
                FROM pensions
                """
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                query_results = cursor.fetchall()

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
                    distance_km=0.0,
                    status=row[12] if row[12] is not None else "Validated"
                ))

            return pensions
        except psycopg2.Error as err:
            print("Error database: ", err)
            return []

    def get_pension_by_user_id(self, user_id: int) -> Dict[str, Any]:
        try:
            query = """
                SELECT pension_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, status 
                FROM pensions 
                WHERE user_id = %s
                """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
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
                    "status": pension[12],
                    "distance_km": 0.0 
                }
                return {"pension": pension_data}
            else:
                return {"message": "Pension not found"}

        except psycopg2.Error as err:
            print(f"Error database: {err}")
            return {"message": f"An error occurred: {err}"}

    def get_pension_by_id(self, id: int) -> PensionDetail:
        try:
            query = """
                SELECT 
                    p.pension_id, p.name, p.address, p.phone, p.email, p.max_capacity, 
                    p.current_occupancy, p.rating, p.description, p.image_urls,
                    p.equipment, p.hours, p.night_price, p.status,
                    s.first_name, s.role, s.image_url,
                    r.name, r.date, r.rating, r.comment
                FROM pensions p
                LEFT JOIN staff s ON p.pension_id = s.pension_id
                LEFT JOIN reviews r ON p.pension_id = r.pension_id
                WHERE p.pension_id = %s
                """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (id,))
                query_results = cursor.fetchall()

            if not query_results:
                return None

            pension_data = query_results[0]
            staff_members = []
            reviews = []

            for row in query_results:
                print("Processing row:", row) 

                if row[14]: 
                    staff_members.append({
                        "first_name": row[14],
                        "role": row[15],
                        "image_url": row[16]
                    })
                if row[17]:
                    review_date = row[18]
                    if isinstance(review_date, datetime):
                        review_date_str = review_date.strftime('%Y-%m-%d')
                    else:
                        review_date_str = None

                    reviews.append({
                        "name": row[17],
                        "date": review_date_str,
                        "rating": row[19],
                        "comment": row[20]
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
                status=pension_data[13],
                staff=staff_members,
                reviews=reviews
            )

            return pension

        except psycopg2.Error as err:
            print("Error database: ", err)
            return None

    def create_pension_profile(self, user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price):
        try:
            query = """
                INSERT INTO pensions (user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING pension_id
                """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price, 'Référencé'))
                pension_id = cursor.fetchone()[0]
                self.conn.commit()
            return pension_id
        except psycopg2.Error as err:
            print("Error database: ", err)
            return None

    def update_pension(self, pension: PensionDetail):
        try:
            query = """
                UPDATE pensions SET name = %s, address = %s, phone = %s, email = %s, max_capacity = %s, rating = %s, description = %s, equipment = %s, hours = %s, night_price = %s, status = %s 
                WHERE pension_id = %s
                """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (pension.name, pension.address, pension.phone, pension.email, pension.max_capacity, pension.rating, pension.description, pension.equipment, pension.hours, pension.night_price, pension.status, pension.id))
                self.conn.commit()
            return True
        except psycopg2.Error as err:
            print("Error database: ", err)
            return False
