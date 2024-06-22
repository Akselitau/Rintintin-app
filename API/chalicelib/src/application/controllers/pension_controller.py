from chalice import Blueprint, CORSConfig
from chalicelib.src.usecase.update_pension import update_pension_handler
from chalicelib.src.usecase.get_pension_by_user import get_pension_by_user_handler
from chalicelib.src.usecase.create_pension_profile import create_pension_profile_handler
from chalicelib.src.usecase.get_pensions import get_pensions_handler
from chalicelib.src.usecase.get_pension_by_id import get_pension_by_id_handler

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
    request = pension.current_request
    data = request.json_body
    return create_pension_profile_handler(data)

@pension.route('/get-pension-user/{userId}', methods=['GET'], cors=cors_config)
def get_pensions_by_user(userId):
    return get_pension_by_user_handler(userId)

@pension.route('/get-pensions', methods=['GET'], cors=cors_config)
def get_pensions():
    request = pension.current_request
    query_params = request.query_params
    return get_pensions_handler(query_params)

@pension.route('/update-pension', methods=['POST'], cors=cors_config)
def update_pension():
    request = pension.current_request
    data = request.json_body
    return update_pension_handler(data)

@pension.route('/get-pension/{pensionId}', methods=['GET'], cors=cors_config)
def get_pension_by_id(pensionId):
    return get_pension_by_id_handler(pensionId)
