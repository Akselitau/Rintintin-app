from chalice import Blueprint, Response, CORSConfig
from chalicelib.src.usecase.update.update_pension import update_pension_handler
from chalicelib.src.usecase.get.get_pension_by_user import get_pension_by_user_handler
from chalicelib.src.usecase.create.create_pension_profile import create_pension_profile_handler
from chalicelib.src.usecase.get.get_pensions import get_pensions_handler
from chalicelib.src.usecase.get.get_pension_by_id import get_pension_by_id_handler
from chalicelib.src.errors import BadRequestError, InternalServerError

pension = Blueprint(__name__)

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['X-Custom-Header'],
    allow_credentials=True
)

@pension.route('/create-pension-profile', methods=['POST'], cors=cors_config)
def create_pension_profile():
    try:
        request = pension.current_request
        data = request.json_body
        return create_pension_profile_handler(data)
    except BadRequestError as e:
        return Response(
            body={"message": e.message},
            status_code=e.status_code,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

@pension.route('/get-pension-user/{userId}', methods=['GET'], cors=cors_config)
def get_pensions_by_user(userId):
    try:
        return get_pension_by_user_handler(userId)
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

@pension.route('/get-pensions', methods=['GET'], cors=cors_config)
def get_pensions():
    try:
        request = pension.current_request
        query_params = request.query_params
        return get_pensions_handler(query_params)
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

@pension.route('/update-pension', methods=['POST'], cors=cors_config)
def update_pension():
    try:
        request = pension.current_request
        data = request.json_body
        return update_pension_handler(data)
    except BadRequestError as e:
        return Response(
            body={"message": e.message},
            status_code=e.status_code,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

@pension.route('/get-pension/{pensionId}', methods=['GET'], cors=cors_config)
def get_pension_by_id(pensionId):
    try:
        return get_pension_by_id_handler(pensionId)
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
