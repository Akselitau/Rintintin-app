from chalice import Blueprint
from chalicelib.src.usecase.get.get_reservations_by_pension import get_reservations_pension_handler
from chalicelib.src.usecase.get.get_reservations_by_user import get_reservations_user_handler
from chalicelib.src.usecase.create.create_reservation import create_reservation_handler
from chalicelib.src.usecase.update.update_reservation import update_reservation_handler

reservation = Blueprint(__name__)

@reservation.route('/make-reservation', methods=['POST'], cors=True)
def make_new_reservation():
    request = reservation.current_request
    data = request.json_body
    return create_reservation_handler(data)

@reservation.route('/get-reservations-user/{user_id}', methods=['GET'], cors=True)
def get_reservations_user(user_id):
    return get_reservations_user_handler(user_id)

@reservation.route('/get-reservations-pension/{pension_id}', methods=['GET'], cors=True)
def get_reservations_pension(pension_id):
    return get_reservations_pension_handler(pension_id)

@reservation.route('/update-reservation', methods=['POST'], cors=True)
def update_reservation():
    request = reservation.current_request
    data = request.json_body
    return update_reservation_handler(data)
