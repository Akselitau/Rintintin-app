from chalice import Blueprint, Response, CORSConfig
import psycopg2
from chalicelib.src.utils import create_jwt_token, hash_password, check_password
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import BadRequestError, InternalServerError, UnauthorizedError

auth = Blueprint(__name__)

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['X-Custom-Header'],
    allow_credentials=True
)


DEFAULT_PROFIL_PICTURE = 'https://img.freepik.com/vecteurs-premium/photo-profil-avatar-homme-illustration-vectorielle_268834-538.jpg'

@auth.route('/create-user', methods=['POST'], cors=True)
def create_user():
    request = auth.current_request.json_body
    name = request.get('name')
    email = request.get('email')
    password = request.get('password')

    if not all([name, email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        if not isinstance(name, str) or not isinstance(email, str) or not isinstance(password, str):
            raise BadRequestError("Parameters must be strings")

        user_repo = get_user_repo()
        existing_user = user_repo.get_user_by_email(email)
        if existing_user:
            raise BadRequestError("User with this email already exists")

        hashed_password = hash_password(password)

        user_id = user_repo.create_user(name, email, hashed_password, DEFAULT_PROFIL_PICTURE)
        if user_id is None:
            raise InternalServerError("Failed to create user")

        token = create_jwt_token(user_id)

        return Response(
            body={"user_id": user_id, "token": token, "message": "User created successfully"},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except BadRequestError as e:
        raise e  
    except psycopg2.IntegrityError as e:
        raise BadRequestError("User with this email already exists")
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
        user = user_repo.get_user_by_email(email)

        if user:
            user_id, name, stored_hashed_password, profile_photo_url = user
            if check_password(password, stored_hashed_password):
                token = create_jwt_token(user_id)
                payload = {
                    "user_id": user_id,
                    "name": name,
                    "profile_photo_url": profile_photo_url,
                    "token": token
                }
                return Response(
                    body={"user": payload, "message": "Login successful"},
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                )
            else:
                raise UnauthorizedError("Invalid credentials")
        else:
            raise UnauthorizedError("Invalid credentials")

    except UnauthorizedError:
        raise 
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
