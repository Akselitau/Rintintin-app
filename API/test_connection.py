# TODO: Erase this, used to debug 

import psycopg2
import bcrypt

connection_params = {
    "host": "localhost",
    "port": "5433",
    "database": "doggydb",
    "user": "mydbuser",
    "password": "mypassword"
}

print(f"Connecting to database with host={connection_params['host']}, port={connection_params['port']}, database={connection_params['database']}, user={connection_params['user']}")

try:
    con = psycopg2.connect(**connection_params)
    cursor = con.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Connexion réussie :", result)

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
    
    # Commit les changements
    con.commit()
    print("Password migration completed successfully.")

except Exception as e:
    print("Erreur de connexion ou de migration des mots de passe :", e)
finally:
    if con:
        con.close()
