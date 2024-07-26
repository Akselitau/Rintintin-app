from chalice import Response
from chalicelib.src.bootstrap import get_dog_repo
from chalicelib.src.errors import BadRequestError, InternalServerError
import boto3
import base64
import os
import uuid
from io import BytesIO 

def create_dog_profile_handler(data, dog_repo=None):
    if dog_repo is None:
        dog_repo = get_dog_repo()

    user_id = data.get('user_id')
    name = data.get('name')
    breed = data.get('breed')
    profile_photo_base64 = data.get('profile_photo')
    information = data.get('information')
    birthdate = data.get('birthdate')

    if not all([user_id, name, breed]):
        raise BadRequestError("Missing required parameters")

    profile_photo_url = None
    if profile_photo_base64:
        try:
            # Décoder l'image base64
            profile_photo_data = base64.b64decode(profile_photo_base64)
            # Générer un nom de fichier unique
            file_extension = "png"  # Remplacez par la méthode appropriée si l'extension est dynamique
            file_name = f"{uuid.uuid4()}.{file_extension}"
            
            # Initialiser le client S3 et uploader le fichier
            s3 = boto3.client('s3')
            bucket_name = os.environ.get('S3_BUCKET_NAME')
            s3.upload_fileobj(BytesIO(profile_photo_data), bucket_name, file_name)
            profile_photo_url = f"https://{bucket_name}.s3.{os.environ.get('AWS_REGION')}.amazonaws.com/{file_name}"
        except Exception as e:
            raise InternalServerError(f"Failed to upload profile photo: {str(e)}")

    dog_id = dog_repo.create_dog_profile(user_id, name, breed, profile_photo_url, information, birthdate)
    return Response(
        body={"dog_id": dog_id, "message": "Dog profile created successfully"},
        status_code=201,
        headers={"Content-Type": "application/json"},
    )
