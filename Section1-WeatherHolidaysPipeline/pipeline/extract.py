import os

import requests
from dotenv import load_dotenv

load_dotenv()
CITY = os.getenv("CITY")

def get_city_info(city_name: str) -> tuple[float, float, str]:
    """
    Returns latitude, longitude, and timezone for a city.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url).json()
    result = response["results"][0]
    
    return result["latitude"], result["longitude"], result["timezone"]
