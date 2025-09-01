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
BASE_HOLIDAY_API_URL = os.getenv("BASE_HOLIDAY_API_URL")


def get_city_info(city_name: str, country_code: str) -> tuple[float, float, str]:
    """
    Returns latitude, longitude, and timezone for a city.
    """
    url = build_url(
        base=BASE_GEOCODING_API_URL, 
        path=f"/search?name={city_name}&count=10&language=en&format=json&countryCode={country_code}"
    )

    response = requests.get(url)
    response.raise_for_status()
    result = response.json()["results"][0]
    
    return result["latitude"], result["longitude"], result["timezone"]


def build_weather_api_url(
        lat: float, long: float, start_date: str, end_date: str, timezone: str,
        frequency: Literal["daily", "hourly"], variables: str
    ) -> str:

    if frequency not in ("hourly", "daily"):
        raise ValueError(f"Invalid frequency: {frequency}. Must be 'hourly' or 'daily'.")
    
    params = [
        f"latitude={lat}",
        f"longitude={long}",
        f"start_date={start_date}",
        f"end_date={end_date}",
        f"timezone={timezone}",
        f"{frequency}={variables}"
    ]
    return f"{BASE_ARCHIVE_API_URL}/archive?" + "&".join(params)


def get_current_date(time_zone: str) -> datetime:
    return datetime.now(ZoneInfo(time_zone)).date()


def get_start_date(current_date: datetime, last_n_months: int):
    return current_date - relativedelta(months=last_n_months)


def get_weather_data(url: str, frequency: Literal["hourly", "daily"] = "daily") -> dict:
    if frequency not in ("hourly", "daily"):
        raise ValueError(f"Invalid frequency: {frequency}. Must be 'hourly' or 'daily'.")

    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()[frequency]


def build_url(base: str, path: str) -> str:
    """
    Join base URL with path, ensuring no double slashes.
    """
    base = base.strip("/")
    path = path.strip("/")
    return "/".join([base, path])


def get_holidays(country_code: str, years: list) -> list[dict]:
    data = []

    for year in years:
        url = build_url(base=BASE_HOLIDAY_API_URL, path=f"/PublicHolidays/{year}/{country_code}")
        response = requests.get(url)
        response.raise_for_status()
        data.extend(response.json())
    return data
