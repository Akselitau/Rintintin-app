from chalice import Response
from chalicelib.src.bootstrap import get_dog_repo
from chalicelib.src.errors import BadRequestError

def create_dog_profile_handler(data, dog_repo=None):
    if dog_repo is None:
        dog_repo = get_dog_repo()

    user_id = data.get('user_id')
    name = data.get('name')
    breed = data.get('breed')
    profile_photo_url = data.get('profile_photo_url')
    information = data.get('information')
    birthdate = data.get('birthdate')

    if not all([user_id, name, breed]):
        raise BadRequestError("Missing required parameters")

    dog_id = dog_repo.create_dog_profile(user_id, name, breed, profile_photo_url, information, birthdate)
    return Response(
        body={"dog_id": dog_id, "message": "Dog profile created successfully"},
        status_code=201,
        headers={"Content-Type": "application/json"},
    )
