from chalice import Response
from chalicelib.src.bootstrap import get_user_repo
from chalicelib.src.errors import UnauthorizedError, NotFoundError, InternalServerError
import jwt

def get_profile_handler(auth_header, secret_key, user_repo=None):
    if user_repo is None:
        user_repo = get_user_repo()

    if not auth_header:
        raise UnauthorizedError("Authorization header missing")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload['user_id']

        user = user_repo.get_user_by_id(user_id)

        if user:
            user_id, name, email, profile_photo_url = user
            return Response(
                body={
                    "user_id": user_id,
                    "name": name,
                    "email": email,
                    "profile_photo_url": profile_photo_url
                },
                status_code=200,
                headers={"Content-Type": "application/json"},
            )
        else:
            raise NotFoundError("User not found")

    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid token")
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
