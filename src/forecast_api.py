import aiohttp
from colorama import Fore


class Forecast:
    def __init__(self, loc):
        self.lat = loc[0]  # latitude
        self.lon = loc[1]  # longitude

    async def get_json(self):
        # first api call, gets json which includes forecast url
        # two-step process is per api docs: <https://weather-gov.github.io/api/general-faqs>
        print(Fore.WHITE + 'getting json', flush=True)
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        async with aiohttp.ClientSession() as session:
            get = await session.get(url)
            forecast_url = await get.json()
            if 'properties' in forecast_url:
                return forecast_url['properties']['forecastHourly']

    async def get_forecast(self, forecast_url, arg="temperature"):
        # second api call, gets forecast from forecast url
        print(Fore.WHITE + 'getting forecast', flush=True)
        print(forecast_url)
        if forecast_url:
            async with aiohttp.ClientSession() as session:
                get = await session.get(str(forecast_url))
                forecast = await get.json()
            if 'properties' in forecast:
                args = ["temperature",
                        "windSpeed",
                        "windDirection"]
                parms = [forecast['properties']['periods'][0][arg] for arg in args]
                return parms
            else:
                print(Fore.MAGENTA + f"{forecast}", flush=True)
