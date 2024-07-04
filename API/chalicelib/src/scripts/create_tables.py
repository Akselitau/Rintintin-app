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
    
# DELETE FROM dog_breed;

# INSERT INTO dog_breed (name) VALUES
# ('Affenpinscher'),
# ('Lévrier Afghan'),
# ('Airedale Terrier'),
# ('Akita'),
# ('Malamute de l''Alaska'),
# ('Bouledogue Américain'),
# ('Cocker Américain'),
# ('Chien Esquimau Américain'),
# ('Foxhound Américain'),
# ('American Pit Bull Terrier'),
# ('American Staffordshire Terrier'),
# ('Épagneul d''eau Américain'),
# ('Chien de berger d''Anatolie'),
# ('Bouvier Australien'),
# ('Berger Australien'),
# ('Terrier Australien'),
# ('Basenji'),
# ('Basset Hound'),
# ('Beagle'),
# ('Colley barbu'),
# ('Berger de Beauce'),
# ('Bedlington Terrier'),
# ('Malinois'),
# ('Berger Belge'),
# ('Tervuren'),
# ('Bouvier Bernois'),
# ('Bichon à poil frisé'),
# ('Coonhound noir et feu'),
# ('Terrier noir russe'),
# ('Chien de Saint-Hubert'),
# ('Border Collie'),
# ('Border Terrier'),
# ('Borzoi'),
# ('Boston Terrier'),
# ('Bouvier des Flandres'),
# ('Boxer'),
# ('Épagneul Boykin'),
# ('Briard'),
# ('Épagneul Breton'),
# ('Griffon Bruxellois'),
# ('Bull Terrier'),
# ('Bouledogue'),
# ('Bullmastiff'),
# ('Cairn Terrier'),
# ('Chien de Canaan'),
# ('Cane Corso'),
# ('Corgi Gallois de Cardigan'),
# ('Cavalier King Charles Spaniel'),
# ('Retriever de la baie de Chesapeake'),
# ('Chihuahua'),
# ('Chien chinois à crête'),
# ('Shar-Pei'),
# ('Chow Chow'),
# ('Clumber Spaniel'),
# ('Cocker Spaniel'),
# ('Colley'),
# ('Coonhound'),
# ('Coton de Tuléar'),
# ('Retriever à poil bouclé'),
# ('Teckel'),
# ('Dalmatien'),
# ('Dandie Dinmont Terrier'),
# ('Dobermann'),
# ('Dogue de Bordeaux'),
# ('Cocker anglais'),
# ('Foxhound anglais'),
# ('Setter anglais'),
# ('Épagneul Springer anglais'),
# ('Épagneul King Charles'),
# ('Chien de montagne de l''Entlebuch'),
# ('Field Spaniel'),
# ('Lapphund finlandais'),
# ('Spitz finlandais'),
# ('Retriever à poil plat'),
# ('Bouledogue français'),
# ('Pinscher allemand'),
# ('Berger allemand'),
# ('Braque allemand à poil court'),
# ('Braque allemand à poil dur'),
# ('Schnauzer géant'),
# ('Terrier Glen of Imaal'),
# ('Golden Retriever'),
# ('Setter Gordon'),
# ('Dogue allemand'),
# ('Chien de montagne des Pyrénées'),
# ('Grand Bouvier suisse'),
# ('Lévrier'),
# ('Bichon havanais'),
# ('Chien d''Ibiza'),
# ('Berger islandais'),
# ('Setter irlandais rouge et blanc'),
# ('Setter irlandais'),
# ('Terrier irlandais'),
# ('Épagneul d''eau irlandais'),
# ('Lévrier irlandais'),
# ('Petit lévrier italien'),
# ('Chin japonais'),
# ('Keeshond'),
# ('Terrier Kerry Blue'),
# ('Komondor'),
# ('Kuvasz'),
# ('Labrador Retriever'),
# ('Lagotto Romagnolo'),
# ('Lakeland Terrier'),
# ('Leonberger'),
# ('Lhassa Apso'),
# ('Petit Chien lion'),
# ('Maltese'),
# ('Terrier de Manchester'),
# ('Mastiff'),
# ('Bull Terrier miniature'),
# ('Pinscher nain'),
# ('Schnauzer nain'),
# ('Mastiff napolitain'),
# ('Terre-Neuve'),
# ('Norfolk Terrier'),
# ('Buhund norvégien'),
# ('Elkhound norvégien'),
# ('Lundehund norvégien'),
# ('Norwich Terrier'),
# ('Retriever de la Nouvelle-Écosse'),
# ('Old English Sheepdog'),
# ('Otterhound'),
# ('Papillon'),
# ('Parson Russell Terrier'),
# ('Pékinois'),
# ('Corgi Gallois de Pembroke'),
# ('Petit Basset Griffon Vendéen'),
# ('Chien du Pharaon'),
# ('Plott Hound'),
# ('Pointer'),
# ('Berger Polonais de Plaine'),
# ('Spitz nain'),
# ('Caniche'),
# ('Chien d''eau portugais'),
# ('Carlin'),
# ('Puli'),
# ('Berger des Pyrénées'),
# ('Rat Terrier'),
# ('Redbone Coonhound'),
# ('Rhodesian Ridgeback'),
# ('Rottweiler'),
# ('Saint-Bernard'),
# ('Saluki'),
# ('Samoyède'),
# ('Schipperke'),
# ('Lévrier écossais'),
# ('Terrier écossais'),
# ('Sealyham Terrier'),
# ('Berger des Shetland'),
# ('Shiba Inu'),
# ('Shih Tzu'),
# ('Husky sibérien'),
# ('Silky Terrier'),
# ('Terrier de Skye'),
# ('Sloughi'),
# ('Petit épagneul de Münster'),
# ('Terrier à poil doux'),
# ('Chien d''eau espagnol'),
# ('Spinone Italiano'),
# ('Staffordshire Bull Terrier'),
# ('Schnauzer'),
# ('Sussex Spaniel'),
# ('Vallhund suédois'),
# ('Mastiff tibétain'),
# ('Épagneul tibétain'),
# ('Terrier tibétain'),
# ('Toy Fox Terrier'),
# ('Treeing Walker Coonhound'),
# ('Vizsla'),
# ('Braque de Weimar'),
# ('Épagneul Springer gallois'),
# ('Terrier gallois'),
# ('West Highland White Terrier'),
# ('Whippet'),
# ('Griffon à poil dur'),
# ('Vizsla à poil dur'),
# ('Chien nu mexicain'),
# ('Yorkshire Terrier');

#ALTER TABLE dogs ADD COLUMN birthdate DATE;



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

