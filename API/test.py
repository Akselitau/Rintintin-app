import os
from dotenv import load_dotenv
import psycopg2

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Vérifier les variables d'environnement
print(f"DB_HOST={os.getenv('DB_HOST')}")
print(f"DB_PORT={os.getenv('DB_PORT')}")
print(f"DB_NAME={os.getenv('DB_NAME')}")
print(f"DB_USER={os.getenv('DB_USER')}")
print(f"DB_PASSWORD={os.getenv('DB_PASSWORD')}")

# Tester la connexion à la base de données
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=40
    )
    print("Connection successful")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Could not connect to the database: {e}")
