import os
import subprocess
import sys
from venv import logger
from chalicelib.src.scripts.create_tables import create_tables
from chalicelib.src.scripts.populate_database import populate_database
from chalicelib.src.errors import CustomError
from chalicelib.src.infrastructure.database import Database
from chalicelib.src.application.controllers.auth_controller import auth
from chalicelib.src.application.controllers.pension_controller import pension
from chalicelib.src.application.controllers.reservation_controller import reservation
from chalicelib.src.application.controllers.user_controller import user
from chalicelib.src.application.controllers.dog_controller import dog
import psycopg2
import os
import sys
from chalice import Chalice, Response, CORSConfig
from chalicelib.src.config import Config, initialize_app_config
import boto3
from dotenv import load_dotenv

try:
    from chalicelib.src.geocoding_service import get_coordinates
    logger.info("Module 'geocoding' imported successfully.")
except Exception as e:
    logger.error(f"Error importing module: {e}")
    raise e

sys.path.append(os.path.join(os.path.dirname(__file__), 'chalicelib/src'))

app = Chalice(app_name='image_processing')

initialize_app_config()

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['X-Custom-Header'],
    allow_credentials=True
)

s3 = boto3.client('s3')
BUCKET_NAME = 'mockup-product'

# Initialize the database connection
Database.initialize_connection()

@app.route('/test-db-connection', methods=['GET'])
def test_db_connection():
    connection = None
    try:
        connection = Database.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {
            'statusCode': 200,
            'body': 'Connexion réussie : ' + str(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Erreur de connexion : {e}"
        }
    finally:
        if Database._connection is not None:
            Database._connection.close()
            Database._connection = None
                        
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


@app.route('/reset-database', methods=['POST'], cors=cors_config)
def reset_database():
    result = create_tables()
    return {"message": result}

@app.route('/populate-database', methods=['POST'], cors=cors_config)
def populate_database_route():
    result = populate_database()
    return {"message": result}
