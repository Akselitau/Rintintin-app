from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.certification_schema import CertificationSchema
from chalicelib.bootstrap import get_certification_repo

certification_routes = Blueprint(__name__)

@certification_routes.route('/certifications', methods=['GET'], cors=True)
def get_certifications():
    psql_certification_repository = get_certification_repo()
    certifications = psql_certification_repository.get_all_certifications()
    return Response(
        body={"certifications": CertificationSchema().dump(certifications, many=True)},
        status_code=200,
        headers={"Content-Type": "application/json"})

@certification_routes.route('/certification/{certification_id}', methods=['GET'], cors=True)
def get_certification(certification_id: int):
    psql_certification_repository = get_certification_repo()
    certification = psql_certification_repository.get_certification_by_id(certification_id)
    return Response(
        body={"certification": CertificationSchema().dump(certification)},
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
