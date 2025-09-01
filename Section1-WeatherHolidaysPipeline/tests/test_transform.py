from datetime import datetime, date, time

import pytest
import pandas as pd
import pandas.testing as pdt
import numpy as np

from pipeline.transform import (
    group_weather_info, get_years_from_dates, split_date_time_columns,
    to_holiday_dates, cast_weather_data_types
)


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


def test_split_date_time_columns_date_and_time():
    data = [
        {"time": "2024-10-08T00:00"},
        {"time": "2024-10-08T01:00"},
        {"time": "2024-10-08T11:00"}
    ]
    
    expected_data = [
        {"timestamp": pd.Timestamp("2024-10-08T00:00"), "time": time(0, 0), "date": date(2024, 10, 8)},
        {"timestamp": pd.Timestamp("2024-10-08T01:00"), "time": time(1, 0), "date": date(2024, 10, 8)},
        {"timestamp": pd.Timestamp("2024-10-08T11:00"), "time": time(11, 0), "date": date(2024, 10, 8)},
    ]

    df_result = split_date_time_columns(pd.DataFrame(data))
    df_expected = pd.DataFrame(expected_data)
    
    pdt.assert_frame_equal(df_result, df_expected, check_like=True)


def test_split_date_time_columns_dates_only():
    data = [
        {"time": "2024-10-06"},
        {"time": "2024-10-07"},
        {"time": "2024-10-08"}
    ]
    
    expected_data = [
        {"timestamp": pd.Timestamp("2024-10-06"), "time": pd.NaT, "date": date(2024, 10, 6)},
        {"timestamp": pd.Timestamp("2024-10-07"), "time": pd.NaT, "date": date(2024, 10, 7)},
        {"timestamp": pd.Timestamp("2024-10-08"), "time": pd.NaT, "date": date(2024, 10, 8)},
    ]

    df_result = split_date_time_columns(pd.DataFrame(data))
    df_expected = pd.DataFrame(expected_data)
    
    pdt.assert_frame_equal(df_result, df_expected, check_like=True)


def test_to_holiday_dates():
    df = pd.DataFrame({"date": ["2025-01-01", "2025-01-02"], "value": [1, 2]})
    result = to_holiday_dates(df)

    assert list(result.columns) == ["date", "is_holiday"]
    assert (result["is_holiday"] == True).all()
    assert len(result) == len(df)


def test_cast_weather_data_types():
    input_data = [
        {
            "timestamp": "2024-10-26", 
            "temperature_2m_mean": "10.7", 
            "temperature_2m_max": "11.2",
            "temperature_2m_min": "7",
            "precipitation_sum": "6.2",
            "weather_code": "51.0",
            "date": "2024-10-26"
        }
    ]
    df = pd.DataFrame(input_data)
    df = cast_weather_data_types(dataframe=df)

    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
    assert df["temperature_2m_mean"].dtype == "Float32"
    assert df["temperature_2m_max"].dtype == "Float32"
    assert df["temperature_2m_min"].dtype == "Float32"
    assert df["precipitation_sum"].dtype == "Float32"
    assert df["weather_code"].dtype == "Int32"
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_cast_weather_data_types_nans():
    input_data = [
        {
            "timestamp": pd.NaT, 
            "temperature_2m_mean": pd.NA, 
            "temperature_2m_max": pd.NA,
            "temperature_2m_min": pd.NA,
            "precipitation_sum": pd.NA,
            "weather_code": pd.NA, 
            "date": pd.NaT
        }
    ]
    df = pd.DataFrame(input_data)
    df = cast_weather_data_types(dataframe=df)

    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
    assert df["temperature_2m_mean"].dtype == "Float32"
    assert df["temperature_2m_max"].dtype == "Float32"
    assert df["temperature_2m_min"].dtype == "Float32"
    assert df["precipitation_sum"].dtype == "Float32"
    assert df["weather_code"].dtype == "Int32"
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
