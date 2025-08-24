from datetime import datetime

import pytest

from pipeline.transform import group_weather_info, get_years_from_dates


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