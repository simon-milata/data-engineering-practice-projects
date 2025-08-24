from datetime import datetime

import pytest
from urllib.parse import urlparse, parse_qs

from pipeline.extract import (
    get_city_info, build_weather_api_url, group_weather_info, get_start_date,
    get_years_from_dates, build_url, get_holidays
)


def test_get_city_info_success(mocker):
    mock_response = {
        "results": [
            {"latitude": 60.16952, "longitude": 24.93545, "timezone": "Europe/Helsinki"}
        ]
    }
    
    mocker.patch("requests.get").return_value.json.return_value = mock_response
    
    lat, lon, tz = get_city_info(city_name="Helsinki", country_code="FI")
    
    assert lat == 60.16952
    assert lon == 24.93545
    assert tz == "Europe/Helsinki"


def test_build_weather_api_url():
    url = build_weather_api_url(
        lat=52.52, long=13.41,
        start_date="2025-08-07", end_date="2025-08-21", timezone="Europe/Helsinki",
        hourly="temperature_2m,relative_humidity_2m,soil_moisture_7_to_28cm"
    )
    parsed_params = parse_qs(urlparse(url).query)
    assert parsed_params["latitude"][0] == "52.52"
    assert parsed_params["longitude"][0] == "13.41"
    assert parsed_params["start_date"][0] == "2025-08-07"
    assert parsed_params["end_date"][0] == "2025-08-21"
    assert parsed_params["timezone"][0] == "Europe/Helsinki"
    assert parsed_params["hourly"][0] == "temperature_2m,relative_humidity_2m,soil_moisture_7_to_28cm"


def test_group_weather_info():
    test_dict = {
        "time": ["2025-08-07", "2025-08-08", "2025-08-09"],
        "temperature_2m_mean": [18.8, 20.8, 22.1],
        "temperature_2m_max": [24.2, 26.9, 28.6],
        "temperature_2m_min": [12.7, 15.5, 14.9]
    }
   
    expected_result = [
        {
            "time": "2025-08-07",
            "temperature_2m_mean": 18.8,
            "temperature_2m_max": 24.2,
            "temperature_2m_min": 12.7
        },
        {
            "time": "2025-08-08",
            "temperature_2m_mean": 20.8,
            "temperature_2m_max": 26.9,
            "temperature_2m_min": 15.5
        },
        {
            "time": "2025-08-09",
            "temperature_2m_mean": 22.1,
            "temperature_2m_max": 28.6,
            "temperature_2m_min": 14.9
        },
    ]

    assert group_weather_info(test_dict) == expected_result


def test_get_start_date_one_month():
    current_date = datetime(2025, 8, 23, 12, 0, 0)
    result = get_start_date(current_date, 1)
    assert result == datetime(2025, 7, 23, 12, 0, 0)


def test_get_start_date_multiple_months():
    current_date = datetime(2025, 8, 23, 12, 0, 0)
    result = get_start_date(current_date, 6)
    assert result == datetime(2025, 2, 23, 12, 0, 0)


def test_get_start_date_across_year_boundary():
    current_date = datetime(2025, 2, 23, 12, 0, 0)
    result = get_start_date(current_date, 3)
    assert result == datetime(2024, 11, 23, 12, 0, 0)


def test_get_start_date_zero_months():
    current_date = datetime(2025, 8, 23, 12, 0, 0)
    result = get_start_date(current_date, 0)
    assert result == current_date


def test_get_start_date_large_offset():
    current_date = datetime(2025, 8, 23, 12, 0, 0)
    result = get_start_date(current_date, 24)
    assert result == datetime(2023, 8, 23, 12, 0, 0)


def test_get_years_from_dates_five_years():
    start_date = datetime(2020, 8, 12)
    end_date = datetime(2025, 8, 12)

    expected = [2020, 2021, 2022, 2023, 2024, 2025]
    
    assert get_years_from_dates(start_date=start_date, end_date=end_date) == expected


def test_get_years_from_dates_same_year():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    assert get_years_from_dates(start_date, end_date) == [2023]


def test_get_years_from_dates_invalid_order():
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2020, 1, 1)
    with pytest.raises(ValueError):
        get_years_from_dates(start_date, end_date)


def test_get_years_from_dates_leap_year():
    start_date = datetime(2019, 12, 31)
    end_date = datetime(2020, 1, 1)
    assert get_years_from_dates(start_date, end_date) == [2019, 2020]


def test_build_url_no_trailing_leading_slashes():
    url = build_url(base="https://date.nager.at/api/v3", path="PublicHolidays/2025/AT")
    assert url == "https://date.nager.at/api/v3/PublicHolidays/2025/AT"


def test_build_url_trailing_leading_slashes():
    url = build_url(base="https://date.nager.at/api/v3/", path="/PublicHolidays/2025/AT")
    assert url == "https://date.nager.at/api/v3/PublicHolidays/2025/AT"


def test_build_url_multiple_trailing_leading_slashes():
    url = build_url(base="https://date.nager.at/api/v3////", path="///PublicHolidays/2025/AT")
    assert url == "https://date.nager.at/api/v3/PublicHolidays/2025/AT"


def test_get_holidays_single_year(mocker):
    mock_response = [{"date": "2025-01-01", "name": "New Year's Day"}]

    mock_requests = mocker.patch("pipeline.extract.requests.get")
    mock_requests.return_value.json.return_value = mock_response
    mock_requests.return_value.raise_for_status = lambda: None

    result = get_holidays("AT", [2025])

    assert result == mock_response
    assert len(result) == 1
    mock_requests.assert_called_once_with("https://date.nager.at/api/v3/PublicHolidays/2025/AT")


def test_get_holidays_multiple_years(mocker):
    mock_responses = [
        [{"date": "2025-01-01", "name": "New Year's Day"}],
        [{"date": "2026-01-01", "name": "New Year's Day"}],
    ]

    mock_get = mocker.patch("pipeline.extract.requests.get")
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.json.side_effect = mock_responses

    result = get_holidays("AT", [2025, 2026])

    assert result == [
        {"date": "2025-01-01", "name": "New Year's Day"},
        {"date": "2026-01-01", "name": "New Year's Day"},
    ]
    assert mock_get.call_count == 2
    mock_get.assert_any_call("https://date.nager.at/api/v3/PublicHolidays/2025/AT")
    mock_get.assert_any_call("https://date.nager.at/api/v3/PublicHolidays/2026/AT")


def test_get_holidays_multiple_items(mocker):
    mock_response = [
        {"date": "2025-01-01", "name": "New Year's Day"},
        {"date": "2025-12-25", "name": "Christmas Day"}
    ]

    mock_requests = mocker.patch("pipeline.extract.requests.get")
    mock_requests.return_value.json.return_value = mock_response
    mock_requests.return_value.raise_for_status = lambda: None

    result = get_holidays("AT", [2025])

    assert result == mock_response
    assert len(result) == 2


def test_get_holidays_duplicate_names(mocker):
    mock_response = [
        {"date": "2025-04-20", "name": "Easter"},
        {"date": "2025-04-21", "name": "Easter"},
    ]

    mock_requests = mocker.patch("pipeline.extract.requests.get")
    mock_requests.return_value.json.return_value = mock_response
    mock_requests.return_value.raise_for_status = lambda: None

    result = get_holidays("AT", [2025])

    assert len(result) == 2
    assert result[0]["name"] == "Easter"
    assert result[1]["name"] == "Easter"
    assert result[0]["date"] != result[1]["date"]
