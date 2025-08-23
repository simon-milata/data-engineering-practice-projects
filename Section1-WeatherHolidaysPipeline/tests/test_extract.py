from urllib.parse import urlparse, parse_qs

from pipeline.extract import get_city_info, build_weather_api_url, group_weather_info


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
        start="2025-08-07", end="2025-08-21",
        hourly="temperature_2m,relative_humidity_2m,soil_moisture_7_to_28cm"
    )
    parsed_params = parse_qs(urlparse(url).query)
    assert parsed_params["latitude"][0] == "52.52"
    assert parsed_params["longitude"][0] == "13.41"
    assert parsed_params["start"][0] == "2025-08-07"
    assert parsed_params["end"][0] == "2025-08-21"
    assert parsed_params["hourly"][0] == "temperature_2m,relative_humidity_2m,soil_moisture_7_to_28cm"


def test_build_weather_api_url_no_additional_params():
    url = build_weather_api_url(
        lat=52.52, long=13.41
    )
    parsed_params = parse_qs(urlparse(url).query)
    assert parsed_params["latitude"][0] == "52.52"
    assert parsed_params["longitude"][0] == "13.41"


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