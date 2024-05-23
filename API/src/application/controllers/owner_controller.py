
from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.owner_schema import OwnerSchema
from chalicelib.bootstrap import get_owner_repo

owner_routes = Blueprint(__name__)


@owner_routes.route('/owner/{owner_id}', methods=['GET'], cors=True)
def get_owner(owner_id: int):
    psql_owner_repository = get_owner_repo()
    owner = psql_owner_repository.get_owner_by_id(owner_id)
    return Response(
        body={"owner": OwnerSchema().dump(owner)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )