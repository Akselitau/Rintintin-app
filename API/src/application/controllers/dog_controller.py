
from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.dog_schema import DogSchema
from chalicelib.bootstrap import get_dog_repo

dog_routes = Blueprint(__name__)

@dog_routes.route('/dogs', methods=['GET'], cors=True)
def get_dogs():
    psql_dog_repository = get_dog_repo()
    dogs = psql_dog_repository.get_all_dogs()
    return Response(
        body={"dogs": DogSchema().dump(dogs, many=True)}, 
        status_code=200,
        headers={"Content-Type": "application/json"})

@dog_routes.route('/dog/{dog_id}', methods=['GET'], cors=True)
def get_dog(dog_id: int):
    psql_dog_repository = get_dog_repo()
    dog = psql_dog_repository.get_dog_by_id(dog_id)
    return Response(
        body={"dog": DogSchema().dump(dog)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )