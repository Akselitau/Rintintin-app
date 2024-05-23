import psycopg2
from psycopg2 import sql

def create_tables():
    commands = [
        """
        DROP TABLE IF EXISTS reservations CASCADE;
        """,
        """
        DROP TABLE IF EXISTS dogs CASCADE;
        """,
        """
        DROP TABLE IF EXISTS owners CASCADE;
        """,
        """
        DROP TABLE IF EXISTS pensions CASCADE;
        """,
        """
        CREATE TABLE IF NOT EXISTS owners (
            owner_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dogs (
            dog_id SERIAL PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            breed VARCHAR(100) NOT NULL,
            FOREIGN KEY (owner_id)
                REFERENCES owners (owner_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pensions (
            pension_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(100),
            max_capacity INTEGER NOT NULL,
            current_occupancy INTEGER NOT NULL,
            rating FLOAT NOT NULL,
            description TEXT,
            image_url TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id SERIAL PRIMARY KEY,
            dog_id INTEGER NOT NULL,
            pension_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (dog_id)
                REFERENCES dogs (dog_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (pension_id)
                REFERENCES pensions (pension_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    ]

    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="doggydb",
            user="mydbuser",
            password="mypassword"
        )
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        connection.commit()
        print("Tables créées avec succès")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
