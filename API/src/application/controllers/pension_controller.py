from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.pension_schema import PensionSchema
from chalicelib.bootstrap import (
    get_pension_repo,
)

pension_routes = Blueprint(__name__)

@pension_routes.route('/pensions', methods=['GET'], cors=True)
def get_pensions():
    psql_pension_repository = get_pension_repo()
    pensions = psql_pension_repository.get_all_pensions()
    return Response(
        body={"pensions": PensionSchema().dump(pensions, many=True)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
    
@pension_routes.route('/pension/{pension_id}', methods=['GET'], cors=True)
def get_pension(pension_id: int) -> Response:
    psql_pension_repository = get_pension_repo()
    pension = psql_pension_repository.get_pension_by_id(pension_id)
    return Response(
        body={"pension": PensionSchema().dump(pension)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
