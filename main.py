import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def clear_console():
    if sys.platform in ["linux", "darwin", "cygwin", "msys"]:
        os.system('clear')
    elif sys.platform == "win32": 
        os.system('cls')
    else:
        print("\n" * 100)


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
        clear_console() 
        answer = input(f"Meinst du {cityname} in {region}, {country}? (Ja/Nein): ").lower()

        if answer in ["ja", "j", "nein", "n"]:
            return answer
        else:            
            print('\n\033[93mAntworte bitte mit "Ja" oder "Nein"!\033[0m')   
            input("")         


def get_json(response):
    if response.status_code == 200:
        data = response.json()
        return data
    else: 
        print("\033[91m\n >>>>> Fehler! Überprüfe den API-Schlüssel oder den Stadtnamen! <<<<<\n\033[0m")


def read_data(data):
    cityname = data["location"]["name"]
    region = data["location"]["region"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_c"]

    return cityname, region, country, temperature


def main():

    while True:
        clear_console()
        city = get_city()
        response = request_api(city)
        data = get_json(response)

        if data != None:    
            cityname, region, country, temperature = read_data(data)
            answer = check_city(cityname, region, country)

            if answer in ["ja", "j"]:
                print(f"\n\033[92mDie Temperatur in {cityname}, {region} liegt bei {temperature}°C\033[0m")                
                return            


main()