import os
import psycopg2

class Database:
    _connection = None

    @staticmethod
    def initialize_connection():
        if Database._connection is None or Database._connection.closed:
            Database._connection = psycopg2.connect(
                host=os.environ['DB_HOST'],
                port=os.environ['DB_PORT'],
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )

    @staticmethod
    def get_connection():
        if Database._connection is None or Database._connection.closed:
            raise Exception("Database connection is not initialized or is closed.")
        return Database._connection
