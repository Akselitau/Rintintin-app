from typing import List
from src.domain.Service import Service
from psycopg2 import sql
import psycopg2

DATABASE_URL = "dbname=doggydb user=aksel host=localhost password=changeme"


class PsqlServiceRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
    

    def get_services_by_pension(self, pension_id: str) -> List[Service]:
        try:
            service_query = sql.SQL(
                """
            SELECT service_id, pension_id, price, comment
            FROM services
            WHERE pension_id = {pension_id}
            """
            ).format(pension_id=sql.Literal(pension_id))
            with self.conn.cursor() as curs:
                curs.execute(service_query)
                query_results = curs.fetchall()
                
            services = []
            for row in query_results:
                services.append(Service(
                    id=row[0], 
                    pension_id=row[1],
                    price=row[2], 
                    description=row[3]))
            
            return services
        except psycopg2.Error as err:
            print("Error database: ", err)
