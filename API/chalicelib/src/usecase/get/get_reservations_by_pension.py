from chalice import Response
from chalicelib.src.errors import InternalServerError
from chalicelib.src.bootstrap import get_reservation_repo

def get_reservations_pension_handler(pension_id):
    try:
        reservation_repo = get_reservation_repo()
        reservations = reservation_repo.get_reservations_by_pension(pension_id)
        if not reservations:
            return Response(
                body={"message": "Reservations not found"},
                status_code=404,
                headers={"Content-Type": "application/json"},
            )
        return Response(
            body={"reservations": reservations},
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
