import psycopg2
from chalicelib.src.config import Config

class Database:
    _connection = None

    @staticmethod
    def initialize_connection():
        if Database._connection is None or Database._connection.closed:
            Database._connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )

    @staticmethod
    def get_connection():
        if Database._connection is None or Database._connection.closed:
            raise Exception("Database connection is not initialized or is closed.")
        return Database._connection
