import os
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import boto3
from chalice import Chalice, Response, CORSConfig
from src.infrastructure.pension_psql_repository import PsqlPensionRepository
from src.application.schema.pension_schema import PensionSchema

app = Chalice(app_name='image_processing')
s3 = boto3.client('s3')
BUCKET_NAME = 'mockup-product'

# Configuration CORS
cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type'],
    max_age=600,
    expose_headers=['X-Custom-Header'],
    allow_credentials=True
)

def initialize_database():
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'create_tables.py')
    print(f"Chemin du script de création des tables : {script_path}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print("Initialisation de la base de données réussie")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {script_path} n'a pas été trouvé")

initialize_database()


@app.route('/populate-database', methods=['POST'], cors=cors_config)
def populate_database():
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'populate_database.py')
    print(f"Chemin du script de remplissage de la base de données : {script_path}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
        return {"message": "Base de données remplie avec succès"}
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du remplissage de la base de données : {e}")
        return {"message": f"Erreur lors du remplissage de la base de données : {e}"}
    except FileNotFoundError:
        print(f"Erreur : Le fichier {script_path} n'a pas été trouvé")
        return {"message": f"Erreur : Le fichier {script_path} n'a pas été trouvé"}
    
    

@app.route('/get-pensions', methods=['GET'], cors=cors_config)
def get_pensions():
    psql_pension_repository = get_pension_repo()
    pensions = psql_pension_repository.get_all_pensions()
    return Response(
        body={"pensions": PensionSchema().dump(pensions, many=True)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )

def get_pension_repo():
    return PsqlPensionRepository(
        host="localhost",
        port=5432,
        db_name="doggydb",
        user="mydbuser",
        password="mypassword",
    )
