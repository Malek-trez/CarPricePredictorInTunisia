import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = 'https://www.automobile.tn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def get_Cars_Urls():
    Cars_links = []
    for i in range (1,176,1):
        brand_url = f'{BASE_URL}/fr/occasion/{str(i)}'
        response = requests.get(brand_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')


        articles =soup.findAll(class_='occasion-item-v2')
        for article in articles:
            a_tag = article.find('a', class_='occasion-link-overlay')
            link = a_tag['href']
            Cars_links.append(link)

    return Cars_links

def get_car_details(car_url):
    brand_url = f'{BASE_URL}/{car_url}'
    response = requests.get(brand_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    Price =soup.find('div', {'class':'price'}).get_text(strip=True)

    Specs = {}

    MainSpecsList=soup.find('div', {'class':'main-specs'}).find_all('li')
    for li in MainSpecsList:
        spec_name = li.find('span', class_='spec-name').get_text(strip=True)
        spec_value = li.find('span', class_='spec-value').get_text(strip=True)
        spec_value = spec_value.replace(' ', '')
        Specs[spec_name] = spec_value

    DivOtherSpecs=soup.findAll('div', {'class':'divided-specs'})
    for div in DivOtherSpecs:
        specs_list = div.find_all('li')
        for li in specs_list:
            spec_name = li.find('span', class_='spec-name').get_text(strip=True)
            spec_value = li.find('span', class_='spec-value').get_text(strip=True) 
            if li.find('a'):
                spec_value = li.find('a').get_text(strip=True)
            Specs[spec_name] = spec_value

    
    Brand=Specs["Marque"]
    Model=Specs["Modèle"]
    keys_to_delete=["Date de l'annonce", "Marque", "Modèle"]
    for key in keys_to_delete:
        Specs.pop(key, None)

    return Brand,Model,Price,Specs
    
def save_to_csv(data, headers, filename='Data/Automobiletn_Occasion_Data.csv'):
    """ Write data to CSV, dynamically handling the headers """
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers if the file is empty
        if file.tell() == 0:
            writer.writerow(headers)
        # Write the data row
        writer.writerow(data)
    

if __name__ == '__main__':
    All_links = get_Cars_Urls()
    print(f"Got {len(All_links)} different articles in total")

    all_specs_keys = set()  # A set to store unique spec keys
    all_car_data = []        # List to store all the car data

    for link in All_links:
        try:
            print(f"Scraping {link}...")
            Brand, Model, Price, Specs = get_car_details(link)

            # Add the spec keys to the headers set (this ensures uniqueness)
            all_specs_keys.update(Specs.keys())
            all_car_data.append((Brand, Model, Price, Specs))
            print(f"Data collected for {link}")

        except Exception as e:
            print(f"Error occurred while scraping {link}: {e}")
            continue
        
        time.sleep(1)

    # Create the final sorted header list (sorted order)
    headers = ['Brand', 'Model', 'Price'] + sorted(all_specs_keys)

    # Now, reorder the data to match the header order
    for car_data in all_car_data:
        Brand, Model, Price, Specs = car_data
        
        # Prepare the row, starting with Brand, Model, and Price
        row = [Brand, Model, Price]
        
        # Add spec values, ensuring missing specs are filled with 'None'
        for key in headers[3:]:  # Start from index 3, since the first 3 are 'Brand', 'Model', and 'Price'
            row.append(Specs.get(key, None))

        # Save the data to CSV
        save_to_csv(row, headers)

    print("Data saved to CSV.")


