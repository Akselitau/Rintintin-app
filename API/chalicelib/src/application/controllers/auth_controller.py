from chalice import Blueprint
from chalicelib.src.usecase.login import login_handler

auth = Blueprint(__name__)

@auth.route('/login', methods=['POST'], cors=True)
def login():
    request = auth.current_request
    data = request.json_body
    return login_handler(data)
