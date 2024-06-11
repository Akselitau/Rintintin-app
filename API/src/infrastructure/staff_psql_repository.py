from typing import List
from src.domain.Staff import Staff
from psycopg2 import sql
import psycopg2

class PsqlStaffRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
        
    def get_all_staffs(self) -> List[Staff]:
        try:
            staff_query = sql.SQL(
                """
            SELECT staff_id, pension_id, certification_id, first_name, last_name, role, phone, email
            FROM staff
            """
            )
            with self.conn.cursor() as curs:
                curs.execute(staff_query)
                query_results = curs.fetchall()
                
            staffs = []
            for row in query_results:
                staffs.append(Staff(
                    id=row[0], 
                    pension_id=row[1],
                    certification_id=row[2], 
                    first_name=row[3], 
                    last_name=row[4], 
                    role=row[5], 
                    phone=row[6],
                    email=row[7]))
            
            return staffs
        except psycopg2.Error as err:
            print("Error database: ", err)
        
    def get_staff_by_id(self, id: int) -> Staff:
        try:
                staff_query = sql.SQL(
                    """
                SELECT staff_id, pension_id, certification_id, first_name, last_name, role, phone, email
                FROM staff
                WHERE staff_id = {id}
                """
                ).format(id=sql.Literal(id))
                with self.conn.cursor() as curs:
                    curs.execute(staff_query)
                    query_result = curs.fetchone()
                
                return Staff(
                        id=query_result[0], 
                        pension_id=query_result[1],
                        certification_id=query_result[2], 
                        first_name=query_result[3], 
                        last_name=query_result[4], 
                        role=query_result[5], 
                        phone=query_result[6],
                        email=query_result[7])
        except psycopg2.Error as err:
            print("Error database: ", err)