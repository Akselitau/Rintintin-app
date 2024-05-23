from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.reservation_schema import ReservationSchema
from chalicelib.bootstrap import get_reservation_repo

reservation_routes = Blueprint(__name__)

@reservation_routes.route('/reservations', methods=['GET'], cors=True)
def get_reservations():
    # Implémentation de la méthode pour récupérer toutes les réservations

@reservation_routes.route('/reservation/{reservation_id}', methods=['GET'], cors=True)
def get_reservation(reservation_id: int):
    # Implémentation de la méthode pour récupérer une réservation par son ID
