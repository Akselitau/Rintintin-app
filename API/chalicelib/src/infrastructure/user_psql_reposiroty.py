from chalicelib.src.infrastructure.database import Database
import psycopg2

class UserPsqlRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    def get_user_by_id(self, user_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, name, email, profile_photo_url FROM users WHERE user_id = %s",
                    (user_id,)
                )
                user = cursor.fetchone()
            return user
        except psycopg2.Error as err:
            print("Error database: ", err)
            return None

    def create_user(self, name, email, password, profile_photo_url):
        try:
            print(f"Creating user in database: {name}, {email}, {profile_photo_url}")
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, password, profile_photo_url) VALUES (%s, %s, %s, %s) RETURNING user_id",
                    (name, email, password, profile_photo_url)
                )
                user_id = cursor.fetchone()[0]
                self.conn.commit()
                print("User ID created:", user_id)  # Debugging line
            return user_id
        except psycopg2.Error as err:
            print("Error database: ", err)
            return None

    def get_user_by_email(self, email):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, name, password, profile_photo_url FROM users WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()
                print(f"Fetched user: {user}")  # Log pour débogage
            return user
        except psycopg2.Error as err:
            print("Error database: ", err)
            return None