
from chalice.app import Blueprint
from chalice.app import Response
from chalicelib.application.schema.staff_schema import StaffSchema
from chalicelib.bootstrap import get_staff_repo

staff_routes = Blueprint(__name__)

@staff_routes.route('/staff', methods=['GET'], cors=True)
def get_staffs():
    psql_staff_repository = get_staff_repo()
    staffs = psql_staff_repository.get_all_staffs()
    return Response(
        body={"staffs": StaffSchema().dump(staffs, many=True)}, 
        status_code=200,
        headers={"Content-Type": "application/json"})

@staff_routes.route('/staff/{staff_id}', methods=['GET'], cors=True)
def get_staff(staff_id: int):
    psql_staff_repository = get_staff_repo()
    staff = psql_staff_repository.get_staff_by_id(staff_id)
    return Response(
        body={"staff": StaffSchema().dump(staff)}, 
        status_code=200,
        headers={"Content-Type": "application/json"},
    )