import os

import requests
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()
BASE_ARCHIVE_API_URL = os.getenv("BASE_ARCHIVE_API_URL")
BASE_GEOCODING_API_URL = os.getenv("BASE_GEOCODING_API_URL")


def get_city_info(city_name: str, country_code: str) -> tuple[float, float, str]:
    """
    Returns latitude, longitude, and timezone for a city.
    """
    url = f"{BASE_GEOCODING_API_URL}/search?name={city_name}&count=10&language=en&format=json&countryCode={country_code}"
    response = requests.get(url).json()
    result = response["results"][0]
    
    return result["latitude"], result["longitude"], result["timezone"]


def build_weather_api_url(lat: float, long: float, **kwargs) -> str:
    params = urlencode(kwargs)
    base_url = f"{BASE_ARCHIVE_API_URL}/archive?latitude={lat}&longitude={long}&{params}"

    return base_url


def group_weather_info(weather_data: dict) -> list[dict]:
    """
        Convert a dict of lists into a list of dicts, one per index.

        All keys in the input dict must map to lists of the same length.
    """
    grouped_data = []
    number_of_elements = len(weather_data["time"])

    for i in range(number_of_elements):
        data = {}
        for key, value in weather_data.items():
            data[key] = value[i]
        grouped_data.append(data)

    return grouped_data
