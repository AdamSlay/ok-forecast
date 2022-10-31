from src import forecast_api as f_api
from unittest.mock import AsyncMock
import pytest
import json


def test_init() -> None:
    loc = [35, 94]
    fore = f_api.Forecast(loc)
    assert fore.lat == loc[0]
    assert fore.lon == loc[1]


class MockClientSession:
    # this is a class that mocks the return value of aiohttp.ClientSession.get
    def __init__(self, text, status):
        self.text = text
        self.status = status

    async def text(self):
        return self.text

    async def json(self):
        # had to throw a json() method in there because it is called in the function that's being tested
        return self.text

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self


@pytest.fixture()
def mock_get(mocker):
    async_mock = AsyncMock()
    mocker.patch('src.forecast_api.aiohttp.ClientSession.get', side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_get_json(mock_get):
    mock_data = json.load(open('tests/test_data/mock_get_json_resp.json'))
    resp = MockClientSession(mock_data, 200)
    f = f_api.Forecast([39.2187, -75.6005])
    mock_get.return_value = resp
    task_1 = await f.get_json()
    assert task_1 == 'https://api.weather.gov/gridpoints/PHI/38,40/forecast/hourly'


@pytest.mark.asyncio
async def test_get_json_fail(mock_get):
    with pytest.raises(Exception):
        mock_data = "hello"
        resp = MockClientSession(mock_data, 200)
        f = f_api.Forecast([39.2187, -75.6005])
        mock_get.return_value = resp.text
        await f.get_json()


@pytest.mark.asyncio
async def test_get_json_none(mock_get):
    mock_data = {}  # empty json response
    resp = MockClientSession(mock_data, 200)
    f = f_api.Forecast([39.2187, -75.6005])
    mock_get.return_value = resp
    task_1 = await f.get_json()
    assert task_1 is None


@pytest.mark.asyncio
async def test_get_forecast(mock_get):
    p = json.load(open('tests/test_data/mock_get_forecast_resp.json'))
    resp = MockClientSession(p, 200)
    f = f_api.Forecast([39.2187, -75.6005])
    mock_get.return_value = resp
    task_1 = await f.get_forecast("url")
    assert task_1 == [58, "5 mph", "S"]


@pytest.mark.asyncio
async def test_get_forecast_none(mock_get):
    mock_data = {}  # empty json response
    resp = MockClientSession(mock_data, 200)
    f = f_api.Forecast([39.2187, -75.6005])
    mock_get.return_value = resp
    task_1 = await f.get_forecast("url")
    assert task_1 is None


@pytest.mark.asyncio
async def test_get_forecast_fail(mock_get):
    with pytest.raises(Exception):
        mock_data = "hello"
        resp = MockClientSession(mock_data, 200)
        f = f_api.Forecast([39.2187, -75.6005])
        mock_get.return_value = resp.text
        await f.get_forecast("url")
