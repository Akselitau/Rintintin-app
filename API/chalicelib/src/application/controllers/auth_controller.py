from chalice import Blueprint, Response
from chalicelib.src.utils import create_jwt_token
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import BadRequestError, InternalServerError, UnauthorizedError

auth = Blueprint(__name__)

@auth.route('/create-user', methods=['POST'], cors=True)
def create_user():
    request = auth.current_request.json_body
    name = request.get('name')
    email = request.get('email')
    password = request.get('password')

    if not all([name, email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        user_repo = get_user_repo()
        user_id = user_repo.create_user(name, email, password, None)
        if user_id is None:
            raise InternalServerError("Failed to create user")
        return Response(
            body={"user_id": user_id, "message": "User created successfully"},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

@auth.route('/login', methods=['POST'], cors=True)
def login():
    request = auth.current_request.json_body
    email = request.get('email')
    password = request.get('password')

    if not all([email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        user_repo = get_user_repo()
        user = user_repo.get_user_by_credentials(email, password)

        if user:
            user_id, name, profile_photo_url = user
            token = create_jwt_token(user_id)
            payload = {
                "user_id": user_id,
                "name": name,
                "profile_photo_url": profile_photo_url,
                "token": token
            }
            print(f"User logged in: {payload}")  # Log for debugging
            return Response(
                body={"user": payload, "message": "Login successful"},
                status_code=200,
                headers={"Content-Type": "application/json"},
            )
        else:
            raise UnauthorizedError("Invalid credentials")

    except UnauthorizedError:
        raise  # Propagate the UnauthorizedError
    except Exception as e:
        print(f"Login error: {e}")  # Log for debugging
        raise InternalServerError(f"An error occurred: {e}")