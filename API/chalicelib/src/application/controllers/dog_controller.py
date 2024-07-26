import base64
import json
import boto3
import os
from chalice import Blueprint, Response
from chalicelib.src.errors import InternalServerError, BadRequestError
from chalicelib.src.bootstrap import get_dog_repo
from chalicelib.src.usecase.create.create_dog_profile import create_dog_profile_handler
from chalicelib.src.usecase.get.get_dogs_by_user import get_dogs_by_user_handler
from io import BytesIO
from werkzeug.datastructures import FileStorage


dog = Blueprint(__name__)

@dog.route('/create-dog-profile', methods=['POST'], cors=True)
def create_dog_profile():
    try:
        request = dog.current_request
        data = request.json_body
        
        if 'profile_photo' not in data or not data['profile_photo']:
            return Response(
                body={"message": "Profile photo is required."},
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        try:
            profile_photo_data = data['profile_photo']
            # Split only if there's a header
            if 'data:image' in profile_photo_data:
                header, profile_photo_data = profile_photo_data.split(',', 1)
            
            # Check if the base64 string is valid
            try:
                base64.b64decode(profile_photo_data)
            except Exception as e:
                print(f"Error decoding base64: {e}")
                return Response(
                    body={"message": "Invalid base64 string for profile photo."},
                    status_code=400,
                    headers={"Content-Type": "application/json"}
                )
            
            data['profile_photo'] = profile_photo_data
        except Exception as e:
            print(f"Error processing profile photo: {e}")
            return Response(
                body={"message": "Error processing profile photo."},
                status_code=400,
                headers={"Content-Type": "application/json"}
            )

        return create_dog_profile_handler(data)
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
        return get_dogs_by_user_handler(user_id)
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
