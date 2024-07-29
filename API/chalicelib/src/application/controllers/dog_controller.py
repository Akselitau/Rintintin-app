import json
from uuid import uuid4
import boto3
import os
from chalice import Blueprint, Response
from chalicelib.src.errors import InternalServerError, BadRequestError
from chalicelib.src.bootstrap import get_dog_repo
from chalicelib.src.usecase.create.create_dog_profile import create_dog_profile_handler
from chalicelib.src.usecase.get.get_dogs_by_user import get_dogs_by_user_handler

dog = Blueprint(__name__)

@dog.route('/generate-upload-url', methods=['POST'], cors=True)
def generate_upload_url():
    try:
        request = dog.current_request
        data = request.json_body

        # Utiliser un UUID pour le nom de fichier
        file_name = f"{uuid4()}{os.path.splitext(data.get('file_name'))[1]}"
        file_type = data.get('file_type')

        if not file_name or not file_type:
            return Response(
                body={"message": "File name and file type are required."},
                status_code=400,
                headers={"Content-Type": "application/json"}
            )

        s3 = boto3.client('s3')
        bucket_name = os.environ.get('S3_BUCKET_NAME')

        presigned_post = s3.generate_presigned_post(
            Bucket=bucket_name,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )

        return Response(
            body=json.dumps(presigned_post),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        return Response(
            body={"message": "An internal error occurred."},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@dog.route('/create-dog-profile', methods=['POST'], cors=True)
def create_dog_profile():
    try:
        request = dog.current_request
        data = request.json_body
        
        # Assume data includes `user_id`, `name`, `breed`, `birthdate`, `information`, `profile_photo_url`
        required_fields = ['user_id', 'name', 'breed', 'profile_photo_url']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return Response(
                body={"message": f"Missing required fields: {', '.join(missing_fields)}"},
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        response = create_dog_profile_handler(data)
        return response
    except BadRequestError as e:
        return Response(
            body={"message": e.message},
            status_code=e.status_code,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(
            body={"message": "An internal error occurred."},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@dog.route('/get-dogs/{user_id}', methods=['GET'], cors=True)
def get_dogs(user_id):
    try:
        response = get_dogs_by_user_handler(user_id)
        return response
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")

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
