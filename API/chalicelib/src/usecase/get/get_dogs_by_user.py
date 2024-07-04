from chalice import Response
from chalicelib.src.bootstrap import get_dog_repo
from chalicelib.src.application.schema.dog_schema import DogSchema

def get_dogs_by_user_handler(user_id):
    dog_repo = get_dog_repo()
    dogs = dog_repo.get_dogs_by_user(user_id)
    dogs_list = DogSchema(many=True).dump(dogs)

    return Response(
        body={"dogs": dogs_list},
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
