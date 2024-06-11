import psycopg2

def test_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="doggydb",
            user="mydbuser",
            password="mypassword"
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
