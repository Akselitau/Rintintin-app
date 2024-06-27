from datetime import date, timedelta
import os
import psycopg2
import json

def populate_database():
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = connection.cursor()

        # Insert users
        users = [
            ("Alice", "alice@example.com", "password123", "https://randomuser.me/api/portraits/women/1.jpg"),
            ("Bob", "bob@example.com", "password123", "https://randomuser.me/api/portraits/men/1.jpg"),
            ("Charlie", "charlie@example.com", "password123", "https://randomuser.me/api/portraits/men/2.jpg")
        ]
        for user in users:
            cursor.execute(
                "INSERT INTO users (name, email, password, profile_photo_url) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                user
            )
        print("Users inserted successfully.")

        # Fetch user IDs
        cursor.execute("SELECT user_id, email FROM users")
        users_from_db = cursor.fetchall()
        user_map = {email: user_id for user_id, email in users_from_db}

        # Insert dogs
        dogs = [
            (user_map['alice@example.com'], "Rex", "Labrador", "https://placedog.net/500/280?id=1", "A good boi"),
            (user_map['bob@example.com'], "Bella", "Beagle", "https://placedog.net/500/280?id=2", "Crazy as hell"),
            (user_map['charlie@example.com'], "Max", "Bulldog", "https://placedog.net/500/280?id=3", "Doesn't speak english")
        ]
        for dog in dogs:
            cursor.execute(
                "INSERT INTO dogs (user_id, name, breed, profile_photo_url, information) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                dog
            )
        print("Dogs inserted successfully.")

        # Insert pensions
        pensions = [
            (user_map['alice@example.com'], "Happy Paws", "10 Rue de Rivoli, 75001 Paris, France", "123-456-7890", "info@happypaws.com", 20, 5, 4.5, "A great place for your dog to stay.", ["https://placedog.net/500/280?id=1", "https://placedog.net/500/280?id=4"], ['Wifi', 'Air conditioning'], "9am - 5pm",23, "Validated"),
            (user_map['bob@example.com'], "Dog Haven", "20 Avenue de l'Opéra, 75001 Paris, France", "987-654-3210", "contact@doghaven.com", 15, 3, 4.2, "Safe and loving environment for your pet.", ["https://placedog.net/500/280?id=2", "https://placedog.net/500/280?id=5"], ['Playground', 'Swimming pool'], "8am - 6pm",30),
            (user_map['charlie@example.com'], "Puppy Paradise", "30 Boulevard de Sébastopol, 75004 Paris, France", "456-789-0123", "info@puppyparadise.com", 25, 10, 4.8, "The ultimate paradise for your puppy.", ["https://placedog.net/500/280?id=3", "https://placedog.net/500/280?id=6"], ['Grooming', 'Vet on call'], "7am - 7pm", 20)
        ]

        for pension in pensions:
            cursor.execute(
                """INSERT INTO pensions (user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                (
                    pension[0], pension[1], pension[2], pension[3], pension[4], pension[5],
                    pension[6], pension[7], pension[8], 
                    '{' + ','.join('"' + item + '"' for item in pension[9]) + '}',  # Correctly format the array for image URLs
                    '{' + ','.join('"' + item + '"' for item in pension[10]) + '}',  # Correctly format the array for equipment
                    pension[11], pension[12]
                )
            )
        print("Pensions inserted successfully.")


        # Insert staff
        staff = [
            (1, "CERT001", "John", "Doe", "Manager", "john.doe@example.com", "123-456-7890", "https://randomuser.me/api/portraits/men/1.jpg"),
            (2, "CERT002", "Jane", "Smith", "Groomer", "jane.smith@example.com", "098-765-4321", "https://randomuser.me/api/portraits/women/2.jpg"),
            (3, "CERT003", "Emily", "Jones", "Trainer", "emily.jones@example.com", "567-890-1234", "https://randomuser.me/api/portraits/women/3.jpg")
        ]
        for member in staff:
            cursor.execute(
                """INSERT INTO staff (pension_id, certification_id, first_name, last_name, role, email, phone, image_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                member
            )
        print("Staff inserted successfully.")

        # Insert reviews
        reviews = [
            (1, "Alice", '2024-05-10', 4.5, "Great place for my dog."),
            (2, "Bob", '2024-06-15', 4.2, "Nice and clean."),
            (3, "Charlie", '2024-07-10', 4.8, "My dog loved it!"),
            (1, "David", '2024-08-10', 4.6, "Very friendly staff."),
            (2, "Eve", '2024-09-15', 4.3, "Good service."),
            (3, "Frank", '2024-10-10', 4.9, "Highly recommend."),
            (1, "Grace", '2024-11-10', 4.4, "Will come back again."),
            (2, "Hank", '2024-12-15', 4.6, "Great experience."),
            (3, "Ivy", '2025-01-01', 4.7, "Excellent care for my dog."),
            (1, "Jack", '2025-01-15', 4.5, "Very satisfied.")
        ]
        for review in reviews:
            cursor.execute(
                """INSERT INTO reviews (pension_id, name, date, rating, comment)
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                review
            )
        print("Reviews inserted successfully.")

        # Insert daily occupancy
        cursor.execute("SELECT pension_id FROM pensions")
        pensions = cursor.fetchall()
        start_date = date.today()
        end_date = start_date + timedelta(days=30)
        
        for pension in pensions:
            current_date = start_date
            while current_date <= end_date:
                cursor.execute(
                    "INSERT INTO daily_occupancy (pension_id, date, occupancy) VALUES (%s, %s, %s)",
                    (pension[0], current_date, 0)
                )
                current_date += timedelta(days=1)
        print("Daily occupancy inserted successfully.")

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