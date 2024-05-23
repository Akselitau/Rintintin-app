from typing import List
from src.domain.Certification import Certification
from psycopg2 import sql
import psycopg2

class PsqlCertificationRepository:
    def __init__(self, host: str, port: str, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        self.conn.set_session(autocommit=True)

    def get_all_certifications(self) -> List[Certification]:
        try:
            certification_query = sql.SQL(
                """
                SELECT id, name, description, validity
                FROM certifications
                """
            )
            with self.conn.cursor() as curs:
                curs.execute(certification_query)
                query_results = curs.fetchall()

            certifications = []
            for row in query_results:
                certifications.append(Certification(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    validity=row[3]
                ))

            return certifications
        except psycopg2.Error as err:
            print("Error database: ", err)

    def get_certification_by_id(self, id: int) -> Certification:
        try:
            certification_query = sql.SQL(
                """
                SELECT id, name, description, validity
                FROM certifications
                WHERE id = {id}
                """
            ).format(id=sql.Literal(id))
            with self.conn.cursor() as curs:
                curs.execute(certification_query)
                query_result = curs.fetchone()

            return Certification(
                id=query_result[0],
                name=query_result[1],
                description=query_result[2],
                validity=query_result[3]
            )
        except psycopg2.Error as err:
            print("Error database: ", err)
