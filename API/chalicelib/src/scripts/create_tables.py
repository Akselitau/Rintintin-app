import os
import psycopg2
from psycopg2 import sql

def create_tables():
    commands = [
        """
        DROP TABLE IF EXISTS reservations CASCADE;
        """,
        """
        DROP TABLE IF EXISTS reviews CASCADE;
        """,
        """
        DROP TABLE IF EXISTS staff CASCADE;
        """,
        """
        DROP TABLE IF EXISTS dogs CASCADE;
        """,
        """
        DROP TABLE IF EXISTS pensions CASCADE;
        """,
        """
        DROP TABLE IF EXISTS users CASCADE;
        """,
        """
        DROP TABLE IF EXISTS daily_occupancy CASCADE;
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            profile_photo_url TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS dogs (
            dog_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            breed VARCHAR(255) NOT NULL,
            profile_photo_url TEXT,
            information TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pensions (
            pension_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(255),
            max_capacity INTEGER,
            current_occupancy INTEGER,
            rating FLOAT,
            description TEXT,
            image_urls TEXT[],
            equipment TEXT[],
            hours VARCHAR(50),
            night_price FLOAT,
            status VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id SERIAL PRIMARY KEY,
            dog_id INTEGER NOT NULL,
            pension_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status VARCHAR(50),
            FOREIGN KEY (dog_id) REFERENCES dogs (dog_id),
            FOREIGN KEY (pension_id) REFERENCES pensions (pension_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS staff (
            staff_id SERIAL PRIMARY KEY,
            pension_id INTEGER NOT NULL,
            certification_id VARCHAR(50),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            role VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(255),
            image_url TEXT,
            FOREIGN KEY (pension_id) REFERENCES pensions (pension_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            pension_id INTEGER NOT NULL,
            name VARCHAR(255),
            date DATE,
            rating FLOAT,
            comment TEXT,
            FOREIGN KEY (pension_id) REFERENCES pensions (pension_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS daily_occupancy (
            id SERIAL PRIMARY KEY,
            pension_id INTEGER NOT NULL,
            date DATE NOT NULL,
            occupancy INTEGER,
            FOREIGN KEY (pension_id) REFERENCES pensions (pension_id),
            UNIQUE (pension_id, date)
        );
        """
    ]

    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
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


##SQL SCRIPT
# -- Drop existing tables if they exist
# DROP TABLE IF EXISTS reservations CASCADE;
# DROP TABLE IF EXISTS reviews CASCADE;
# DROP TABLE IF EXISTS staff CASCADE;
# DROP TABLE IF EXISTS dogs CASCADE;
# DROP TABLE IF EXISTS pensions CASCADE;
# DROP TABLE IF EXISTS users CASCADE;
# DROP TABLE IF EXISTS daily_occupancy CASCADE;

# -- Create tables
# CREATE TABLE IF NOT EXISTS users (
#     user_id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     password VARCHAR(100) NOT NULL,  -- Should be hashed in a real application
#     profile_photo_url TEXT
# );

# CREATE TABLE IF NOT EXISTS dogs (
#     dog_id SERIAL PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     breed VARCHAR(100) NOT NULL,
#     profile_photo_url TEXT,
#     information TEXT,
#     FOREIGN KEY (user_id)
#         REFERENCES users (user_id)
#         ON UPDATE CASCADE ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS pensions (
#     pension_id SERIAL PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     address VARCHAR(255) NOT NULL,
#     phone VARCHAR(20),
#     email VARCHAR(100),
#     max_capacity INTEGER NOT NULL,
#     current_occupancy INTEGER NOT NULL,
#     rating FLOAT NOT NULL,
#     description TEXT,
#     image_urls TEXT[],
#     equipment TEXT[],
#     hours VARCHAR(50),
#     night_price INTEGER NOT NULL,
#     FOREIGN KEY (user_id)
#         REFERENCES users (user_id)
#         ON UPDATE CASCADE ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS reservations (
#     reservation_id SERIAL PRIMARY KEY,
#     dog_id INTEGER NOT NULL,
#     pension_id INTEGER NOT NULL,
#     start_date DATE NOT NULL,
#     end_date DATE NOT NULL,
#     status VARCHAR(50) DEFAULT 'Requested' NOT NULL,
#     FOREIGN KEY (dog_id)
#         REFERENCES dogs (dog_id)
#         ON UPDATE CASCADE ON DELETE CASCADE,
#     FOREIGN KEY (pension_id)
#         REFERENCES pensions (pension_id)
#         ON UPDATE CASCADE ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS staff (
#     staff_id SERIAL PRIMARY KEY,
#     pension_id INTEGER NOT NULL,
#     certification_id VARCHAR(100),
#     first_name VARCHAR(100) NOT NULL,
#     last_name VARCHAR(100) NOT NULL,
#     role VARCHAR(50) NOT NULL,
#     email VARCHAR(100),
#     phone VARCHAR(20),
#     image_url TEXT,
#     FOREIGN KEY (pension_id)
#         REFERENCES pensions (pension_id)
#         ON UPDATE CASCADE ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS reviews (
#     review_id SERIAL PRIMARY KEY,
#     pension_id INTEGER NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     date DATE NOT NULL,
#     rating FLOAT NOT NULL,
#     comment TEXT,
#     FOREIGN KEY (pension_id)
#         REFERENCES pensions (pension_id)
#         ON UPDATE CASCADE ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS daily_occupancy (
#     id SERIAL PRIMARY KEY,
#     pension_id INTEGER REFERENCES pensions(pension_id),
#     date DATE NOT NULL,
#     occupancy INTEGER DEFAULT 0 NOT NULL
# );
