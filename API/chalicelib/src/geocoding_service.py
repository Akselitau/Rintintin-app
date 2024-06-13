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

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            print(f"Coordinates for {address}: {latitude}, {longitude}")
            return latitude, longitude
        else:
            print(f"No data returned for address: {address}")
    else:
        print(f"Failed to get coordinates for address: {address}, status code: {response.status_code}")
    return None, None
