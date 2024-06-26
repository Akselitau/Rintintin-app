import os
from stytch import Client
from dotenv import load_dotenv


load_dotenv()

project_id = os.getenv("AUTH_PROJECT_ID")
secret = os.getenv("AUTH_SECRETS")
environment = os.getenv("AUTH_ENVIRONMENT")

if not project_id or not secret or not environment:
    raise ValueError("Environment variables AUTH_PROJECT_ID, AUTH_SECRETS, and AUTH_ENVIRONMENT must be set")

stytch_client = Client(
    project_id=project_id,
    secret=secret,
    environment=environment
)
