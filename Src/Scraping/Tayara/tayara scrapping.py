import requests
from bs4 import BeautifulSoup
import csv

# Base API URL for fetching IDs
ids_api_url = "https://www.tayara.tn/_next/data/w-igF8RTxVccmBlp6D-YQ/en/ads/c/V%C3%A9hicules/Voitures.json"
query_params = {
    "minPrice": 10000,
    "page": 1,
    "category": "Véhicules",
    "subCategory": "Voitures",
}

# Function to fetch vehicle IDs
def fetch_vehicle_ids():
    page = 1
    vehicle_ids = []

    while True:
        print(f"Fetching page {page} for IDs...")
        query_params["page"] = page
        response = requests.get(ids_api_url, params=query_params)

        if response.status_code != 200:
            print(f"Failed to fetch data for page {page}. Status Code: {response.status_code}")
            break

        data = response.json()
        vehicles = data["pageProps"]["searchedListingsAction"]["newHits"]

        if not vehicles:
            print(f"No more IDs found on page {page}. Stopping.")
            break

        for vehicle in vehicles:
            vehicle_ids.append(vehicle["id"])

        page += 1

    print(f"Total IDs fetched: {len(vehicle_ids)}")
    return vehicle_ids

# Function to scrape vehicle details
def scrape_vehicle_details(vehicle_id):
    base_url = f"https://www.tayara.tn/item/{vehicle_id}/"
    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Failed to fetch the page for vehicle ID {vehicle_id}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting basic details
    try:
        name = soup.find("h1", class_="text-gray-700 font-bold text-2xl font-arabic").text.strip()
    except AttributeError:
        name = "N/A"

    try:
        # Use the correct selector to extract the value from the 'data' tag
        price = soup.find("data", class_="font-bold font-arabic text-red-600 text-2xl").get("value")
        if price is None:
            price = "N/A"
    except AttributeError:
        price = "N/A"


    # Extracting criteria
    criteria = {}
    for crit in soup.select("ul.grid li"):
        try:
            key = crit.find("span", class_="text-gray-600/80").text.strip()
            value = crit.find("span", class_="text-gray-700/80").text.strip()
            criteria[key] = value
        except AttributeError:
            continue

    vehicle_details = {
        "Name": name,
        "Price": price,
        **criteria,
    }

    return vehicle_details

# Main function to fetch IDs, scrape data, and save to CSV
def main():
    # Fetch all vehicle IDs
    vehicle_ids = fetch_vehicle_ids()

    # File to save data
    csv_file = "vehicle_data.csv"
    fieldnames = ["Name", "Price", "Kilométrage", "Couleur du véhicule", "Etat du véhicule",
                  "Boite", "Année", "Cylindrée", "Marque", "Modèle", "Puissance fiscale",
                  "Type de carrosserie", "Carburant"]

    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Scrape data for each vehicle
        for vehicle_id in vehicle_ids:
            print(f"Scraping data for vehicle ID: {vehicle_id}")
            details = scrape_vehicle_details(vehicle_id)
            if details:
                writer.writerow(details)

    print(f"Data scraping complete. Results saved to {csv_file}.")

# Run the script
main()
