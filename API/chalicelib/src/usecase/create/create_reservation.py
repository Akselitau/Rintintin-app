from chalice import Response
from chalicelib.src.bootstrap import get_reservation_repo
from chalicelib.src.errors import BadRequestError, InternalServerError
from datetime import datetime

def create_reservation_handler(data, reservation_repo=None):
    if reservation_repo is None:
        reservation_repo = get_reservation_repo()

    pension_id = data.get('pension_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    dog_id = data.get('dog_id')

    if not all([pension_id, check_in, check_out, dog_id]):
        raise BadRequestError("Missing required parameters")

    try:
        if not isinstance(check_in, str):
            raise BadRequestError("check_in must be a string")
        if not isinstance(check_out, str):
            raise BadRequestError("check_out must be a string")

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        success = reservation_repo.make_reservation(pension_id, check_in_date, check_out_date, dog_id)

        if success:
            return Response(
                body={"message": "Reservation successful"},
                status_code=200,
                headers={"Content-Type": "application/json"},
            )
        else:
            raise BadRequestError("Reservation failed due to lack of capacity")

    except ValueError as e:
        raise BadRequestError(f"Invalid date format: {e}")
    except BadRequestError as e:
        raise e
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
