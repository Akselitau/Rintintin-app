from src.domain.Owner import Owner
from psycopg2 import sql
import psycopg2

DATABASE_URL = "dbname=doggydb user=aksel host=localhost password=changeme"


class PsqlOwnerRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)
            
    def get_owner_by_id(self, id: int) -> Owner:
        try:
            owner_query = sql.SQL(
                """
            SELECT owner_id, first_name, last_name, email, phone, address
            FROM owners
            WHERE owner_id = {id}
            """
            ).format(id=sql.Literal(id))
            with self.conn.cursor() as curs:
                curs.execute(owner_query)
                query_result = curs.fetchone()
            return Owner(
                    id=query_result[0], 
                    first_name=query_result[1], 
                    last_name=query_result[2], 
                    email=query_result[3], 
                    phone=query_result[4], 
                    address=query_result[5])
        except psycopg2.Error as err:
            print("Error database: ", err)