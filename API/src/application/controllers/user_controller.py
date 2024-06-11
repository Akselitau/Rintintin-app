from chalice import Blueprint
from src.usecase.create_user import create_user_handler
from src.usecase.get_profile import get_profile_handler

user = Blueprint(__name__)

SECRET_KEY = "your_secret_key"

@user.route('/create-user', methods=['POST'], cors=True)
def create_user():
    request = user.current_request
    data = request.json_body
    return create_user_handler(data)

@user.route('/get-profile', methods=['GET'], cors=True)
def get_profile():
    request = user.current_request
    auth_header = request.headers.get('Authorization')
    return get_profile_handler(auth_header, SECRET_KEY)
