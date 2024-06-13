import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host="",
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("Connexion réussie")
    except Exception as e:
        print(f"Erreur de connexion : {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    test_connection()
