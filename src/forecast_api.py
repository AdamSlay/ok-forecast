import aiohttp
from colorama import Fore


class Forecast:
    def __init__(self, loc):
        self.lat = loc[0]
        self.lon = loc[1]

    async def get_json(self):
        # first api call, gets json which includes forecast url
        # this two-step process is per api docs:
        # <https://weather-gov.github.io/api/general-faqs>
        print(Fore.WHITE + 'getting json', flush=True)
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        async with aiohttp.ClientSession() as session:
            get = await session.get(url)
            forecast_url = await get.json()
            return forecast_url['properties']['forecastHourly']

    async def get_forecast(self, forecast, arg="temperature"):
        # second api call, gets forecast from forecast url
        print(Fore.WHITE + 'getting forecast', flush=True)
        async with aiohttp.ClientSession() as session:
            get = await session.get(forecast)
            forecast = await get.json()
        if 'properties' in forecast:
            return forecast['properties']['periods'][0][arg]
