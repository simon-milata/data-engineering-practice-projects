from datetime import datetime


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