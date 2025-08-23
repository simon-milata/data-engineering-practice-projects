import os

import requests
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()
CITY = os.getenv("CITY")
BASE_API_URL = os.getenv("BASE_API_URL")


def get_city_info(city_name: str) -> tuple[float, float, str]:
    """
    Returns latitude, longitude, and timezone for a city.
    """
    url = f"{BASE_API_URL}/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url).json()
    result = response["results"][0]
    
    return result["latitude"], result["longitude"], result["timezone"]


def build_weather_api_url(lat: float, long: float, **kwargs) -> str:
    params = urlencode(kwargs)
    base_url = f"{BASE_API_URL}/archive?latitude={lat}&longitude={long}&{params}"

    return base_url
