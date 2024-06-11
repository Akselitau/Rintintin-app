from chalice import Response
from src.errors import BadRequestError, InternalServerError
from src.bootstrap import get_reservation_repo

def update_reservation_handler(data):
    reservation_id = data.get('reservation_id')
    status = data.get('status')

    if not all([reservation_id, status]):
        raise BadRequestError("Missing required parameters")


    if status not in ["Rejected", "Accepted"]:
        raise BadRequestError("Invalid status")


    try:
        reservation_repo = get_reservation_repo()
        success = reservation_repo.update_reservation_status(reservation_id, status)
        if not success:
            raise InternalServerError("Failed to update reservation status")

        return Response(
            body={"message": "Reservation status updated successfully"},
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")