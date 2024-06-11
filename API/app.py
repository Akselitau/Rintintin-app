import os
import subprocess
import sys
from chalice import Chalice, CORSConfig
from flask import Response
from src.errors import CustomError
from src.infrastructure.database import Database
from src.application.controllers.auth_controller import auth
from src.application.controllers.pension_controller import pension
from src.application.controllers.reservation_controller import reservation
from src.application.controllers.user_controller import user
from src.application.controllers.dog_controller import dog

import os
import sys
from chalice import Chalice, Response, CORSConfig
from src.config import Config, initialize_app_config
import boto3

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

app = Chalice(app_name='image_processing')

initialize_app_config()

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['X-Custom-Header'],
    allow_credentials=True
)

# Initialize S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'mockup-product'

# Initialize database connection
Database.initialize_connection(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    db_name=Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD
)

@app.middleware('all')
def handle_errors(event, get_response):
    try:
        response = get_response(event)
    except CustomError as e:
        response = Response(
            body={"message": e.message},
            status_code=e.status_code,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        response = Response(
            body={"message": "An unexpected error occurred"},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
    return response

app.register_blueprint(auth)
app.register_blueprint(pension)
app.register_blueprint(reservation)
app.register_blueprint(user)
app.register_blueprint(dog)

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', script_name)
    if not os.path.exists(script_path):
        return {"message": f"Erreur : Le fichier {script_path} n'a pas été trouvé"}
    
    try:
        subprocess.run([sys.executable, script_path], check=True)
        return {"message": f"{script_name} exécuté avec succès"}
    except subprocess.CalledProcessError as e:
        return {"message": f"Erreur lors de l'exécution de {script_name} : {e}"}

@app.route('/reset-database', methods=['POST'], cors=cors_config)
def reset_database():
    return run_script('create_tables.py')

@app.route('/populate-database', methods=['POST'], cors=cors_config)
def populate_database_route():
    return run_script('populate_database.py')
