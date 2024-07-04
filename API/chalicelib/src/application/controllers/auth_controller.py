from chalice import Blueprint, Response
from chalicelib.src.utils import create_jwt_token, hash_password, check_password
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import BadRequestError, InternalServerError, UnauthorizedError

auth = Blueprint(__name__)

DEFAULT_PROFIL_PICTURE = 'https://img.freepik.com/vecteurs-premium/photo-profil-avatar-homme-illustration-vectorielle_268834-538.jpg'

from chalicelib.src.utils import create_jwt_token, hash_password

@auth.route('/create-user', methods=['POST'], cors=True)
def create_user():
    request = auth.current_request.json_body
    name = request.get('name')
    email = request.get('email')
    password = request.get('password')

    if not all([name, email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        print(f"Received request to create user: {name}, {email}")
        hashed_password = hash_password(password)
        print(f"Hashed password: {hashed_password}")
        
        user_repo = get_user_repo()
        user_id = user_repo.create_user(name, email, hashed_password, DEFAULT_PROFIL_PICTURE)
        if user_id is None:
            raise InternalServerError("Failed to create user")
        
        token = create_jwt_token(user_id)
        print(f"Generated token: {token}")
        
        return Response(
            body={"user_id": user_id, "token": token, "message": "User created successfully"},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the exception
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
        user = user_repo.get_user_by_email(email)  # On utilise l'email pour récupérer l'utilisateur

        if user:
            user_id, name, stored_hashed_password, profile_photo_url = user
            print(f"Stored hashed password: {stored_hashed_password}")  # Log pour débogage
            if check_password(password, stored_hashed_password):
                token = create_jwt_token(user_id)
                payload = {
                    "user_id": user_id,
                    "name": name,
                    "profile_photo_url": profile_photo_url,
                    "token": token
                }
                print(f"User logged in: {payload}")  # Log pour débogage
                return Response(
                    body={"user": payload, "message": "Login successful"},
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                )
            else:
                print("Password check failed")  # Log pour débogage
                raise UnauthorizedError("Invalid credentials")
        else:
            print("User not found")  # Log pour débogage
            raise UnauthorizedError("Invalid credentials")

    except UnauthorizedError:
        raise  # Propagate the UnauthorizedError
    except Exception as e:
        print(f"Login error: {e}")  # Log pour débogage
        raise InternalServerError(f"An error occurred: {e}")