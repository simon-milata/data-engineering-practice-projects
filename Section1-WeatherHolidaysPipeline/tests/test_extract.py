from urllib.parse import urlparse, parse_qs

from pipeline.extract import get_city_info, build_weather_api_url


def test_get_city_info_success(mocker):
    mock_response = {
        "results": [
            {"latitude": 60.16952, "longitude": 24.93545, "timezone": "Europe/Helsinki"}
        ]
    }
    
    mocker.patch("requests.get").return_value.json.return_value = mock_response
    
    lat, lon, tz = get_city_info("Helsinki")
    
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
