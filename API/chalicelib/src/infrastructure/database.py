import os
import psycopg2

class Database:
    _connection = None

    @staticmethod
    def initialize_connection():
        try:
            Database._connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                connect_timeout=10
            )
        except psycopg2.OperationalError as e:
            print(f"Could not connect to the database: {e}")
            raise e

    @staticmethod
    def get_connection():
        if Database._connection is None or Database._connection.closed:
            raise Exception("Database connection is not initialized or is closed.")
        return Database._connection
