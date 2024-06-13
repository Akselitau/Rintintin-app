from chalice import Response
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import BadRequestError, InternalServerError

def create_user_handler(data, user_repo=None):
    if user_repo is None:
        user_repo = get_user_repo()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    profile_photo_url = data.get('profile_photo_url', None)

    if not all([name, email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        user_id = user_repo.create_user(name, email, password, profile_photo_url)
        return Response(
            body={"user_id": user_id, "message": "User created successfully"},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
