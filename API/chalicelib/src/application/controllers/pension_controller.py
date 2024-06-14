from chalice import Blueprint
from chalicelib.src.usecase.update_pension import update_pension_handler
from chalicelib.src.usecase.get_pension_by_user import get_pension_by_user_handler
from chalicelib.src.usecase.create_pension_profile import create_pension_profile_handler
from chalicelib.src.usecase.get_pensions import get_pensions_handler
from chalicelib.src.usecase.get_pension_by_id import get_pension_by_id_handler

pension = Blueprint(__name__)

@pension.route('/create-pension-profile', methods=['POST'], cors=True)
def create_pension_profile():
    request = pension.current_request
    data = request.json_body
    return create_pension_profile_handler(data)

@pension.route('/get-pension-user/{userId}', methods=['GET'], cors=True)
def get_pensions_by_user(userId):
    return get_pension_by_user_handler(userId)

@pension.route('/get-pensions', methods=['GET'], cors=True)
def get_pensions():
    request = pension.current_request
    query_params = request.query_params
    return get_pensions_handler(query_params)

@pension.route('/update-pension', methods=['POST'], cors=True)
def update_pension():
    request = pension.current_request
    data = request.json_body
    return update_pension_handler(data)

@pension.route('/get-pension/{pensionId}', methods=['GET'], cors=True)
def get_pension_by_id(pensionId):
    return get_pension_by_id_handler(pensionId)