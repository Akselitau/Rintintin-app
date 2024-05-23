import psycopg2
from psycopg2 import sql

def populate_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="doggydb",
            user="mydbuser",
            password="mypassword"
        )
        cursor = connection.cursor()

        # Insérer des propriétaires
        owners = [
            ("Alice", "alice@example.com"),
            ("Bob", "bob@example.com"),
            ("Charlie", "charlie@example.com")
        ]
        for owner in owners:
            cursor.execute(
                "INSERT INTO owners (name, email) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                owner
            )

        # Insérer des chiens
        dogs = [
            (1, "Rex", "Labrador"),
            (2, "Bella", "Beagle"),
            (3, "Max", "Bulldog")
        ]
        for dog in dogs:
            cursor.execute(
                "INSERT INTO dogs (owner_id, name, breed) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                dog
            )

        # Insérer des pensions
        pensions = [
            ("Happy Paws", "123 Dog Street", "123-456-7890", "info@happypaws.com", 20, 5, 4.5, "A great place for your dog to stay.", "https://placedog.net/500/280?id=1"),
            ("Dog Haven", "456 Pup Avenue", "987-654-3210", "contact@doghaven.com", 15, 3, 4.2, "Safe and loving environment for your pet.", "https://placedog.net/500/280?id=2")
        ]
        for pension in pensions:
            cursor.execute(
                """INSERT INTO pensions (name, address, phone, email, max_capacity, current_occupancy, rating, description, image_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                pension
            )

        # Insérer des réservations
        reservations = [
            (1, 1, '2024-05-01', '2024-05-10'),
            (2, 2, '2024-06-01', '2024-06-15')
        ]
        for reservation in reservations:
            cursor.execute(
                """INSERT INTO reservations (dog_id, pension_id, start_date, end_date)
                   VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                reservation
            )

        connection.commit()
        print("Base de données remplie avec succès")
    except Exception as e:
        print(f"Erreur lors du remplissage de la base de données : {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    populate_database()
