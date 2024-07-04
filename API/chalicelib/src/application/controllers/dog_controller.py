from chalice import Blueprint, Response
from chalicelib.src.errors import InternalServerError
from chalicelib.src.bootstrap import get_dog_repo
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


@dog.route('/get-dog-breeds', methods=['GET'], cors=True)
def get_dog_breeds():
    try:
        dog_repo = get_dog_repo()
        breeds = dog_repo.get_dog_breeds()
        return Response(
            body={"breeds": breeds},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")