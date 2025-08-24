import os
from typing import Literal

import requests
from zoneinfo import ZoneInfo
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


load_dotenv()
BASE_ARCHIVE_API_URL = os.getenv("BASE_ARCHIVE_API_URL")
BASE_GEOCODING_API_URL = os.getenv("BASE_GEOCODING_API_URL")


def get_city_info(city_name: str, country_code: str) -> tuple[float, float, str]:
    """
    Returns latitude, longitude, and timezone for a city.
    """
    url = f"{BASE_GEOCODING_API_URL}/search?name={city_name}&count=10&language=en&format=json&countryCode={country_code}"
    
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()["results"][0]
    
    return result["latitude"], result["longitude"], result["timezone"]


def build_weather_api_url(
    lat: float, long: float, start_date: str, end_date: str, timezone: str,
    hourly: str | None = None, daily: str | None = None
    ) -> str:
    params = [
        f"latitude={lat}",
        f"longitude={long}",
        f"start_date={start_date}",
        f"end_date={end_date}",
        f"timezone={timezone}",
    ]

    if hourly:
        params.append(f"hourly={hourly}")
    if daily:
        params.append(f"daily={daily}")
    
    return f"{BASE_ARCHIVE_API_URL}/archive?" + "&".join(params)


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


def get_current_date(time_zone: str) -> datetime:
    return datetime.now(ZoneInfo(time_zone)).date()


def get_start_date(current_date: datetime, last_n_months: int):
    return current_date - relativedelta(months=last_n_months)


def get_weather_data(url: str, data_type: Literal["hourly", "daily"] = "daily") -> dict:
    if data_type not in ("hourly", "daily"):
        raise ValueError(f"Invalid data_type: {data_type}. Must be 'hourly' or 'daily'.")

    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()[data_type]


def get_years_from_dates(start_date: datetime, end_date: datetime) -> list:
    """
        Returns a list of unique years from a range of datetimes including both ends.
    """
    if start_date > end_date: 
        raise ValueError(f"Invalid date range: start_date ({start_date}) must be <= end_date ({end_date})")

    num_of_years = end_date.year - start_date.year + 1
    return [start_date.year + i for i in range(num_of_years)]
