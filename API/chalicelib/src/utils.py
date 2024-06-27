import math
import requests

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance en kilomètres


def get_coordinates(address: str) -> (float, float):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'my-app/1.0.0'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            print(f"Coordinates for {address}: {latitude}, {longitude}")  # Debugging line
            return latitude, longitude
        else:
            print(f"No data returned for address: {address}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None, None

