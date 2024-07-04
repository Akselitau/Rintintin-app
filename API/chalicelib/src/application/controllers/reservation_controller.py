from chalice import Blueprint, Response
from chalicelib.src.usecase.get.get_reservations_by_pension import get_reservations_pension_handler
from chalicelib.src.usecase.get.get_reservations_by_user import get_reservations_user_handler
from chalicelib.src.usecase.create.create_reservation import create_reservation_handler
from chalicelib.src.usecase.update.update_reservation import update_reservation_handler
from chalicelib.src.errors import BadRequestError, InternalServerError

reservation = Blueprint(__name__)

@reservation.route('/make-reservation', methods=['POST'], cors=True)
def make_new_reservation():
    request = reservation.current_request
    data = request.json_body
    try:
        return create_reservation_handler(data)
    except BadRequestError as e:
        return Response(
            body={"error": str(e)},
            status_code=400,
            headers={"Content-Type": "application/json"}
        )
    except InternalServerError as e:
        return Response(
            body={"error": str(e)},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@reservation.route('/get-reservations-user/{user_id}', methods=['GET'], cors=True)
def get_reservations_user(user_id):
    try:
        return get_reservations_user_handler(user_id)
    except InternalServerError as e:
        return Response(
            body={"error": str(e)},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@reservation.route('/get-reservations-pension/{pension_id}', methods=['GET'], cors=True)
def get_reservations_pension(pension_id):
    try:
        return get_reservations_pension_handler(pension_id)
    except InternalServerError as e:
        return Response(
            body={"error": str(e)},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@reservation.route('/update-reservation', methods=['POST'], cors=True)
def update_reservation():
    request = reservation.current_request
    data = request.json_body
    try:
        return update_reservation_handler(data)
    except BadRequestError as e:
        return Response(
            body={"error": str(e)},
            status_code=400,
            headers={"Content-Type": "application/json"}
        )
    except InternalServerError as e:
        return Response(
            body={"error": str(e)},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
