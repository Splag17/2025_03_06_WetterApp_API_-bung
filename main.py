import requests
import os
import sys
import json
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
    URL = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&lang=de"
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


def read_datatoday(data):
    cityname = data["location"]["name"]
    region = data["location"]["region"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"] 
    windspeed = data["current"]["wind_kph"]

    return cityname, region, country, temperature, condition, windspeed


def read_dataforecast(data):
    print("\n\n\033[92mVorhersage über die nächsten 7 Tage:\033[0m\n")

    for day in data["forecast"]["forecastday"]: 
        date = day["date"]
        avg_temp = day["day"]["avgtemp_c"]
        rain_prob = day["day"]["daily_chance_of_rain"]

        print(f"\033[92m{date}: {avg_temp}°C | Regenwahrscheinlichkeit {rain_prob}%\033[0m")


def save_to_json(data, filename="wetterdaten.json"):
    # Wichtige Daten extrahieren
    weatherdata = {
        "stadt": data["location"]["name"],
        "region": data["location"]["region"],
        "land": data["location"]["country"],
        "aktuell": {
            "temperatur": data["current"]["temp_c"],
            "wetter": data["current"]["condition"]["text"],
            "windgeschwindigkeit": data["current"]["wind_kph"]
        },
        "vorhersage": []
    }

    # 7-Tage-Vorhersage extrahieren
    for day in data["forecast"]["forecastday"]:
        weatherdata["vorhersage"].append({
            "datum": day["date"],
            "durchschnittstemperatur": day["day"]["avgtemp_c"],
            "regenwahrscheinlichkeit": day["day"]["daily_chance_of_rain"]
        })

    # Daten in eine JSON-Datei speichern
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(weatherdata, file, indent=4, ensure_ascii=False)
    print(f"\n\033[94mDie Wetterdaten wurden in '{filename}' gespeichert.\033[0m")


def main():

    while True:
        clear_console()
        city = get_city()
        response = request_api(city)
        data = get_json(response)

        if data != None:    
            cityname, region, country, temperature, condition, windspeed = read_datatoday(data)
            answer = check_city(cityname, region, country)

            if answer in ["ja", "j"]:
                print(f"\n\033[92mDie Temperatur in {cityname}, {region} liegt bei {temperature}°C\033[0m")
                print(f"\033[92mEs ist {condition} und die Windgeschwindigkeit beträgt {windspeed} Kilometer pro Stunde.\033[0m")                
                read_dataforecast(data)

                save_to_json(data) 
                return     



main()