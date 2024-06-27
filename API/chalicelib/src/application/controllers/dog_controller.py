from chalice import Blueprint
from chalicelib.src.usecase.create.create_dog_profile import create_dog_profile_handler
from chalicelib.src.usecase.get.get_dogs import get_dogs_handler

dog = Blueprint(__name__)

@dog.route('/create-dog-profile', methods=['POST'], cors=True)
def create_dog_profile():
    request = dog.current_request
    data = request.json_body
    return create_dog_profile_handler(data)

@dog.route('/get-dogs/{user_id}', methods=['GET'], cors=True)
def get_dogs(user_id):
    return get_dogs_handler(user_id)