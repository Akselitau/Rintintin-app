#TODO: Erase this, used to debbug 

import psycopg2

connection_params = {
    "host": "localhost",
    "port": "5433",
    "database": "doggydb",
    "user": "mydbuser",
    "password": "mypassword"
}

print(f"Connecting to database with host={connection_params['host']}, port={connection_params['port']}, database={connection_params['database']}, user={connection_params['user']}")

try:
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Connexion réussie :", result)
except Exception as e:
    print("Erreur de connexion :", e)
finally:
    if connection:
        connection.close()
