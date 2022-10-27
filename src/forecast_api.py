import aiohttp
from colorama import Fore


class Forecast:
    def __init__(self, loc):
        self.lat = loc[0]  # latitude
        self.lon = loc[1]  # longitude

    async def get_json(self):
        # first api call, gets json which includes forecast url
        # two-step process is per api docs: <https://weather-gov.github.io/api/general-faqs>
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        print(Fore.WHITE + f'getting json - {url}', flush=True)
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get(url)  # get request
                forecast_url = await get.json()  # convert response to json
                if 'properties' in forecast_url:
                    return forecast_url['properties']['forecastHourly']  # return the forecastHourly link
        except Exception as e:
            print(Fore.RED + f"Error in get_json while requesting {url}: {e}", flush=True)

    async def get_forecast(self, forecast_url):
        # second api call, gets forecast from forecast url
        print(Fore.WHITE + f'getting forecast for {self.lat}, {self.lon} - {forecast_url}', flush=True)
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get(forecast_url)  # get request
                forecast = await get.json()  # convert response to json
            if 'properties' in forecast:
                args = ["temperature",
                        "windSpeed",
                        "windDirection"]
                parms = [forecast['properties']['periods'][0][arg] for arg in args]  # corresponding val for each arg
                return parms
            else:
                print(Fore.MAGENTA + f"{forecast}", flush=True)  # print json if Error in response
        except Exception as e:
            print(Fore.RED + f"Error in get_forecast while requesting {self.lat}, {self.lon}: {e}", flush=True)
