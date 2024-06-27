from chalice import Blueprint
from chalicelib.src.usecase.create.create_user import create_user_handler
from chalicelib.src.usecase.get.get_profile import get_profile_handler

user = Blueprint(__name__)

SECRET_KEY = "your_secret_key"

@user.route('/get-profile', methods=['GET'], cors=True)
def get_profile():
    request = user.current_request
    auth_header = request.headers.get('Authorization')
    return get_profile_handler(auth_header, SECRET_KEY)
