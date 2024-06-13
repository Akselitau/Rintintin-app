from chalice import Response
from datetime import datetime, timedelta
import jwt
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import BadRequestError, UnauthorizedError, InternalServerError

def login_handler(data, user_repo=None, secret_key='your_secret_key'):
    if user_repo is None:
        user_repo = get_user_repo()

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        raise BadRequestError("Missing required parameters")

    try:
        user = user_repo.get_user_by_credentials(email, password)

        if user:
            user_id, name, profile_photo_url = user
            payload = {
                "user_id": user_id,
                "name": name,
                "profile_photo_url": profile_photo_url,
                "exp": datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            return Response(
                body={"token": token},
                status_code=200,
                headers={"Content-Type": "application/json"},
            )
        else:
            raise UnauthorizedError("Invalid credentials")

    except UnauthorizedError:
        raise  # Propagate the UnauthorizedError
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
