from chalice import Response
from pydantic import ValidationError
from src.errors import BadRequestError, InternalServerError
from src.domain.Pension import PensionDetail
from src.bootstrap import get_pension_repo

def update_pension_handler(data):
    try:
        pension = PensionDetail(**data)
    except ValidationError as e:
        raise BadRequestError("Missing required parameters")

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
