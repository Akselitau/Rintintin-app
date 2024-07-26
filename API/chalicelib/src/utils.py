import datetime
import math
import os
from dotenv import load_dotenv
import jwt
import requests
from chalicelib.src.errors import CustomError
import bcrypt
import boto3
from botocore.exceptions import NoCredentialsError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def upload_to_s3(file_name, bucket, object_name=None):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    if object_name is None:
        object_name = file_name

    try:
        s3.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        url = f"https://{bucket}.s3.amazonaws.com/{object_name}"
        return url
    except NoCredentialsError:
        print("Credentials not available")
        return None

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    # Comparer le mot de passe fourni avec le hachage stocké
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise CustomError('Token has expired', status_code=401)
    except jwt.InvalidTokenError:
        raise CustomError('Invalid token', status_code=401)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance en kilomètres


def get_coordinates(address: str) -> (float, float):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'my-app/1.0.0'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            print(f"Coordinates for {address}: {latitude}, {longitude}")  # Debugging line
            return latitude, longitude
        else:
            print(f"No data returned for address: {address}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None, None

