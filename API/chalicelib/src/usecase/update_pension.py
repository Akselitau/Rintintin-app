from chalice import Response
from pydantic import ValidationError
from chalicelib.src.errors import BadRequestError, InternalServerError
from chalicelib.src.domain.Pension import PensionDetail
from chalicelib.src.bootstrap import get_pension_repo

def update_pension_handler(data):
    try:
        pension = PensionDetail(**data)
    except ValidationError as e:
        raise BadRequestError("Invalid parameters provided")

    try:
        pension_repo = get_pension_repo()
        success = pension_repo.update_pension(pension)
        if not success:
            raise InternalServerError("Failed to update pension status")

        return Response(
            body={"message": "Pension status updated successfully"},
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
