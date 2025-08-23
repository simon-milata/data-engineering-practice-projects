from pipeline.extract import get_city_info


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