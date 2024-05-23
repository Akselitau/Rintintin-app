from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.service_schema import ServiceSchema
from chalicelib.bootstrap import get_service_repo

service_routes = Blueprint(__name__)

@service_routes.route('/services/{pension_id}', methods=['GET'], cors=True)
def get_services(pension_id):
    psql_service_repository = get_service_repo()
    services = psql_service_repository.get_services_by_pension(pension_id)
    return Response(
        body={"services": ServiceSchema().dump(services, many=True)}, 
        status_code=200,
        headers={"Content-Type": "application/json"})
