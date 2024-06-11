from src.infrastructure.database import Database

class UserPsqlRepository:
    def __init__(self):
        self.conn = Database.get_connection()

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT user_id, name, email, profile_photo_url FROM users WHERE user_id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def create_user(self, name, email, password, profile_photo_url):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, profile_photo_url) VALUES (%s, %s, %s, %s) RETURNING user_id",
            (name, email, password, profile_photo_url)
        )
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return user_id
    
    def get_user_by_credentials(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT user_id, name, profile_photo_url FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        return user