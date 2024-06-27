import os
import sys
from venv import logger
from chalicelib.src.errors import CustomError
from chalicelib.src.infrastructure.database import Database
from chalicelib.src.application.controllers.auth_controller import auth
from chalicelib.src.application.controllers.pension_controller import pension
from chalicelib.src.application.controllers.reservation_controller import reservation
from chalicelib.src.application.controllers.user_controller import user
from chalicelib.src.application.controllers.dog_controller import dog
from chalice import Chalice, Response, CORSConfig

#TODO: to help debugging geolocalisation in prod, to delete once the feature's complete
try:
    from chalicelib.src.utils import get_coordinates
    logger.info("Module 'geocoding' imported successfully.")
except Exception as e:
    logger.error(f"Error importing module: {e}")
    raise e

sys.path.append(os.path.join(os.path.dirname(__file__), 'chalicelib/src'))

app = Chalice(app_name='rintintin-API')

Database.initialize_connection()


app.register_blueprint(auth)
app.register_blueprint(pension)
app.register_blueprint(reservation)
app.register_blueprint(user)
app.register_blueprint(dog)


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