import requests
from bs4 import BeautifulSoup
import time
import re
import csv

BASE_URL = 'http://www.tunisie-annonce.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def get_Cars_Urls():
    Cars = []

    for i in range (1,13):
        brand_url = f'http://www.tunisie-annonce.com/AnnoncesAuto.asp?rech_cod_cat=2&rech_cod_rub=201&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_cod_energ=&rech_photo=&rech_order_by=31&rech_page_num={str(i)}'
        response = requests.get(brand_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('tr', class_='Tableau1', valign='middle')
        for article in articles:
            marque_model_td = article.find_all('td', onmouseover=lambda x: x and 'Marque' in x)

            marque =  marque_model_td[0].text.strip()
            modele =  marque_model_td[1].text.strip()
            
            links = article.find_all('a', href=True)

            url = [link['href'] for link in links if 'DetailsAnnonceAuto.asp' in link['href']]
            Cars.append({'url': url[0], 'marque': marque, 'model': modele})
            
    return Cars

def get_car_details(car_url):
    brand_url = f'{BASE_URL}/{car_url}'
    response = requests.get(brand_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    car_details = {}
    labels = ['Energie', 'Puissance Fiscale', 'Kilométrage', 'Mise en Circulation', 'Couleur', 'Boite de vitesse', 'Prix']
    for label in labels:
        row = soup.find('td', string=label)  
        if row:
            value = row.find_next('td').text.strip()
            cleaned_value = value.replace('\xa0', ' ')  
            car_details[label] = cleaned_value  
        else :
            print(f'Eroor in {car_url}')
    return car_details



    
def save_to_csv(data, headers, filename='Data/TuniseAnnonce_Data.csv'):
    """ Write data to CSV, dynamically handling the headers """
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers if the file is empty
        if file.tell() == 0:
            writer.writerow(headers)
        # Write each car's data as a new row
        for row in data:
            writer.writerow(row)
    

if __name__ == '__main__':
    All_links = get_Cars_Urls()
    print(f'Got {len(All_links)} article')

    all_car_data = []
    all_specs_keys = ['Brand','Model','Puissance Fiscale','Energie', 'Kilométrage', 'Mise en Circulation', 'Couleur', 'Boite de vitesse', 'Prix']
    for link in All_links:
        Car_details = get_car_details(link['url'])
        car=[]
        for spec in all_specs_keys:
            if spec == 'Brand':
                car.append(link['marque'])  # Fixed here
            elif spec == 'Model':
                car.append(link['model'])  # Fixed here
            else:
                car.append(Car_details.get(str(spec), 'N/A'))  # Safely access dictionary keys
        all_car_data.append(car)

    save_to_csv(all_car_data, all_specs_keys)
    
    print(f"Data saved to 'Data/TuniseAnnonce_Data.csv.csv'.")


        
    