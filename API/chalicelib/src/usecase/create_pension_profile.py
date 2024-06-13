from chalice import Response
from chalicelib.src.errors import BadRequestError, InternalServerError
from chalicelib.src.bootstrap import get_pension_repo

def create_pension_profile_handler(data):
    user_id = data.get('user_id')
    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')
    email = data.get('email')
    max_capacity = data.get('max_capacity')
    current_occupancy = data.get('current_occupancy', 0)
    rating = data.get('rating', 0)
    description = data.get('description')
    image_urls = data.get('image_urls')
    equipment = data.get('equipment')
    size = data.get('size')
    hours = data.get('hours')
    night_price = data.get('night_price')

    if not all([user_id, name, address, max_capacity]):
        raise BadRequestError("Missing required parameters")


    try:
        pension_repo = get_pension_repo()
        pension_id = pension_repo.create_pension_profile(user_id, name, address, phone, email, max_capacity, current_occupancy, rating, description, image_urls, equipment, hours, night_price)
        return Response(
            body={"pension_id": pension_id, "message": "Pension profile created successfully"},
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
