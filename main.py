import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_city():        
    city = input("Gib eine Stadt ein (Stadtname, Bundesland, Land): ")
    return city
        

def request_api(city):
    API_KEY = os.getenv("API_KEY")
    URL = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=de"
    response = requests.get(URL)
    return response


def check_city(cityname, region, country):    
    while True:  
        answer = input(f"Meinst du {cityname} in {region}, {country}? (Ja/Nein): ").lower()

        if answer in ["ja", "j", "nein", "n"]:
            return answer
        else:
            print('Antworte bitte mit "Ja" oder "Nein"!')


def get_json(response):
    if response.status_code == 200:
        data = response.json()
        return data
    else: 
        print("Fehler! Überprüfe den API-Schlüssel oder den Stadtnamen.")


def read_data(data):
    cityname = data["location"]["name"]
    region = data["location"]["region"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_c"]

    return cityname, region, country, temperature


def main():

    while True:
        city = get_city()
        response = request_api(city)
        data = get_json(response)    
        cityname, region, country, temperature = read_data(data)
        answer = check_city(cityname, region, country)

        if answer in ["ja", "j"]:
            print(f"Die Temperatur in {city} liegt bei {temperature}°C")
            return


main()