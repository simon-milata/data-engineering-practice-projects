from datetime import datetime, time

import pandas as pd


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


def get_years_from_dates(start_date: datetime, end_date: datetime) -> list:
    """
        Returns a list of unique years from a range of datetimes including both ends.
    """
    if start_date > end_date: 
        raise ValueError(f"Invalid date range: start_date ({start_date}) must be <= end_date ({end_date})")

    num_of_years = end_date.year - start_date.year + 1
    return [start_date.year + i for i in range(num_of_years)]


def split_date_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
        Renames the original 'time' column to 'timestamp'
        and creates 'date' and 'time' columns from 'timestamp'.
    """
    df = df.copy()
    df = df.rename(columns={"time": "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # If all times are 00:00 set time to NaT
    if (df["timestamp"].dt.time == time(0, 0)).all():
        df["time"] = pd.NaT
    else:
        df["time"] = df["timestamp"].dt.time

    return df


def to_holiday_dates(dataframe: pd.DataFrame):
    """
        Return a DataFrame with only a 'date' column and a new 
        'is_holiday' column set to True for all rows.
    """
    df = dataframe.copy()
    df = df[["date"]]
    df["is_holiday"] = True

    return df


def cast_weather_data_types(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()

    df["temperature_2m_mean"] = df["temperature_2m_mean"].astype("Float32")
    df["temperature_2m_max"] = df["temperature_2m_max"].astype("Float32")
    df["temperature_2m_min"] = df["temperature_2m_min"].astype("Float32")
    df["precipitation_sum"] = df["precipitation_sum"].astype("Float32")

    df["weather_code"] = df["weather_code"].astype("Float32").round().astype("Int32")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = pd.to_datetime(df["date"])

    return df