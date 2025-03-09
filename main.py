import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

City = input("Gib eine Stadt ein: ")

URL = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={City}&lang=de"

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    cityname = data["location"]["name"]
    region = data["location"]["region"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_c"]
    print(f"Die Temperatur in {City} liegt bei {temperature}°C")
    print(f"Stadt = {cityname} in {region}, {country}")
else:
    print("Fehler! Überprüfe den API-Schlüssel oder den Stadtnamen.")