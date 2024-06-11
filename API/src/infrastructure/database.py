# src/infrastructure/database.py

import psycopg2
from psycopg2.extensions import connection

class Database:
    _connection = None

    @staticmethod
    def initialize_connection(host: str, port: str, db_name: str, user: str, password: str):
        if Database._connection is None:
            Database._connection = psycopg2.connect(
                host=host,
                port=port,
                database=db_name,
                user=user,
                password=password
            )
            Database._connection.set_session(autocommit=True)

    @staticmethod
    def get_connection() -> connection:
        if Database._connection is None:
            raise Exception("Database connection is not initialized. Call 'initialize_connection' first.")
        return Database._connection
