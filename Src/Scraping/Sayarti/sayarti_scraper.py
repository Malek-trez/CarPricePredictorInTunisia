import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
URL = "https://www.sayarti.tn/prix-des-voitures/page/3/?sort_order=price_low"

# Send an HTTP GET request to the URL
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract car listings
car_listings = soup.find_all('div', class_='stm-listing-directory-list-loop')

# List to store car data
cars = []

# Loop through each car listing
for listing in car_listings:
    try:
        # Extract the car title
        title = listing.find('div', class_='title').text.strip()

        # Extract the price
        price = listing.find('span', class_='heading-font').text.strip()

        # Extract additional details
        details = {}
        for unit in listing.find_all('div', class_='meta-middle-unit'):
            name = unit.find('div', class_='name').text.strip()
            value = unit.find('div', class_='value').text.strip()
            details[name] = value

        # Combine all data
        cars.append({
            'Model': title,
            'Price': price,
            'Fuel Type': details.get('Type de carburant', ''),
            'Fiscal Power': details.get('Puissance fiscale', ''),
            'Horsepower': details.get('Puissance (Ch DIN)', ''),
            'Transmission': details.get('Boîte', '')
        })

    except AttributeError:
        # Skip listings with missing data
        continue

# Save data to a CSV file with utf-8-sig encoding
csv_file = "car_data3.csv"
fieldnames = ['Model', 'Price', 'Fuel Type', 'Fiscal Power', 'Horsepower', 'Transmission']

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cars)

print(f"Data has been exported to {csv_file}")
