from chalice import Response
import logging
from chalicelib.src.geocoding_service import get_coordinates
from chalicelib.src.errors import InternalServerError
from chalicelib.src.application.schema.pension_schema import PensionSchema
from chalicelib.src.utils import haversine
from chalicelib.src.bootstrap import get_pension_repo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pensions_handler(query_params):
    address = query_params.get('address', None) if query_params else None

    try:
        repo = get_pension_repo()
        pensions = repo.get_all_pensions()

        if address:
            latitude, longitude = get_coordinates(address)
            if latitude is not None and longitude is not None:
                for pension in pensions:
                    pension_lat, pension_lon = get_coordinates(pension.address)
                    if pension_lat is not None and pension_lon is not None:
                        pension.distance_km = haversine(latitude, longitude, pension_lat, pension_lon)
                        logger.info(f"Distance from {address} to {pension.address}: {pension.distance_km} km")
                    else:
                        logger.warning(f"Failed to get coordinates for pension address: {pension.address}")
                pensions.sort(key=lambda x: x.distance_km if x.distance_km is not None else float('inf'))
            else:
                logger.warning(f"Failed to get coordinates for provided address: {address}")
                pensions.sort(key=lambda x: x.rating, reverse=True)
        else:
            pensions.sort(key=lambda x: x.rating, reverse=True)

        response_body = []
        for pension in pensions:
            pension_data = PensionSchema().dump(pension)
            if hasattr(pension, 'distance_km'):
                pension_data['distance_km'] = pension.distance_km
            pension_data['status'] = pension.status  # Ajout du champ status
            response_body.append(pension_data)

        return Response(
            body={"pensions": response_body},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        raise InternalServerError(f"An error occurred: {e}")
