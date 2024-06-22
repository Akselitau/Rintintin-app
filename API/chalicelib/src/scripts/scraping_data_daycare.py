import requests
from bs4 import BeautifulSoup
import csv

# URL de la recherche des pensions canines en Bretagne sur PagesJaunes
url = 'https://www.pagesjaunes.fr/recherche/bretagne/pensions-pour-chiens'

# Effectuer la requête HTTP
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les informations des pensions
pensions = soup.find_all('div', class_='bi-bloc')

data = []

for pension in pensions:
    name = pension.find('a', class_='denomination-links').text.strip()
    address = pension.find('div', class_='adresse-container').text.strip()
    phone = pension.find('a', class_='num-tel').text.strip() if pension.find('a', class_='num-tel') else 'N/A'
    description = pension.find('p', class_='desc-pj').text.strip() if pension.find('p', class_='desc-pj') else 'N/A'
    site_web = pension.find('a', class_='denomination-links')['href'] if pension.find('a', class_='denomination-links') else 'N/A'
    
    data.append([name, address, phone, description, site_web])

# Écrire les données dans un fichier CSV
with open('pensions_canines_bretagne.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Nom', 'Adresse', 'Téléphone', 'Description', 'Site Web'])
    writer.writerows(data)

print("Données des pensions canines sauvegardées dans pensions_canines_bretagne.csv")
