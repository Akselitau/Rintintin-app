import requests
import pandas as pd

API_KEY = 'YOUR_API_KEY'  # Remplacez par votre clé API
SEARCH_QUERY = 'dog day care center'
LOCATION = '48.8566,2.3522'  # Coordonnées de Paris (latitude,longitude)
RADIUS = 50000  # Rayon de recherche en mètres

def get_places(api_key, query, location, radius, next_page_token=None):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'key': api_key,
        'location': location,
        'radius': radius,
        'keyword': query,
        'pagetoken': next_page_token
    }
    response = requests.get(url, params=params)
    return response.json()

def scrape_dog_day_care_centers(api_key, query, location, radius):
    places = []
    next_page_token = None

    while True:
        data = get_places(api_key, query, location, radius, next_page_token)
        places.extend(data.get('results', []))
        next_page_token = data.get('next_page_token')

        if not next_page_token:
            break

    return places

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')

def main():
    places = scrape_dog_day_care_centers(API_KEY, SEARCH_QUERY, LOCATION, RADIUS)
    formatted_data = []

    for place in places:
        formatted_data.append({
            'name': place.get('name'),
            'address': place.get('vicinity'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'place_id': place.get('place_id'),
            'lat': place['geometry']['location']['lat'],
            'lng': place['geometry']['location']['lng']
        })

    save_to_csv(formatted_data, 'dog_day_care_centers_france.csv')

if __name__ == '__main__':
    main()
