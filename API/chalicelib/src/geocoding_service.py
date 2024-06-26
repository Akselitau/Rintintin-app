import requests

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
