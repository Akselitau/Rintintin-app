import os
import psycopg2
import bcrypt

def migrate_passwords():
    conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port="5433",
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
    )

    try:
        with conn.cursor() as cursor:
            # Sélectionner les utilisateurs avec des mots de passe non hachés
            cursor.execute("SELECT user_id, password FROM users WHERE password NOT LIKE '$2b$%'")
            users = cursor.fetchall()

            for user_id, password in users:
                # Hacher chaque mot de passe
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                # Mettre à jour la base de données avec les mots de passe hachés
                cursor.execute(
                    "UPDATE users SET password = %s WHERE user_id = %s",
                    (hashed_password, user_id)
                )

        conn.commit()
        print("Password migration completed successfully.")
    except Exception as e:
        print(f"An error occurred during password migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_passwords()
