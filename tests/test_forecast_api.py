from src import forecast_api as f_api
import pytest
import json


class ClientSession:
    # this is a class that mocks aiohttp.ClientSession
    def __init__(self, text):
        self.text = text

    async def json(self):
        # had to throw a json() method in there because it is called in the function that's being tested
        return self.text

    async def get(self, url):
        return self


def test_init() -> None:
    loc = [35, 94]
    mock_data = json.load(open('tests/test_data/mock_get_json_resp.json'))
    resp = ClientSession(mock_data)
    fore = f_api.Forecast(loc, resp)
    assert fore.lat == loc[0]
    assert fore.lon == loc[1]
    assert fore.session == resp


@pytest.mark.asyncio
async def test_get_json():
    mock_data = json.load(open('tests/test_data/mock_get_json_resp.json'))
    resp = ClientSession(mock_data)
    f = f_api.Forecast([39.2187, -75.6005], resp)
    task_1 = await f.get_json()
    assert task_1 == 'https://api.weather.gov/gridpoints/PHI/38,40/forecast/hourly'


@pytest.mark.asyncio
async def test_get_json_fail():
    with pytest.raises(Exception):
        resp = "exception"
        f = f_api.Forecast([39.2187, -75.6005], resp)
        await f.get_json()


@pytest.mark.asyncio
async def test_get_json_none():
    mock_data = {}  # empty json response
    resp = ClientSession(mock_data)
    f = f_api.Forecast([39.2187, -75.6005], resp)
    task_1 = await f.get_json()
    assert task_1 is None


@pytest.mark.asyncio
async def test_get_forecast():
    p = json.load(open('tests/test_data/mock_get_forecast_resp.json'))
    resp = ClientSession(p)
    f = f_api.Forecast([39.2187, -75.6005], resp)
    task_1 = await f.get_forecast("url")
    assert task_1 == [58, "5 mph", "S"]


@pytest.mark.asyncio
async def test_get_forecast_none():
    mock_data = {}  # empty json response
    resp = ClientSession(mock_data)
    f = f_api.Forecast([39.2187, -75.6005], resp)
    task_1 = await f.get_forecast("url")
    assert task_1 is None


@pytest.mark.asyncio
async def test_get_forecast_fail():
    with pytest.raises(Exception):
        resp = "exception"
        f = f_api.Forecast([39.2187, -75.6005], resp)
        await f.get_forecast("url")
