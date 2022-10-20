from colorama import Fore
from meteostat import Stations
from forecast_api import Forecast
from datetime import datetime
import matplotlib.pyplot as plt
import geopandas
import asyncio


async def main() -> int:
    data_q = asyncio.Queue()
    num_stats, stations = create_df()
    task1 = asyncio.create_task(fetch_api(stations, data_q))
    task2 = asyncio.create_task(plot_data(num_stats, data_q))
    await task1, task2
    return 0


def create_df():
    # create dataframe with all OK stations using meteostat
    stations = Stations()
    stations = stations.region('US', 'OK')
    num_stats = stations.count()
    stations = stations.fetch()
    stations = stations[(stations["icao"] != "N/A")]
    return num_stats, stations


async def fetch_api(stations, data_q: asyncio.Queue) -> None:
    # separate station coordinates from stations
    stations_loc = stations[["latitude", "longitude"]]

    # fetch data from weather.gov api
    for row, st_id in enumerate(stations["icao"]):
        print(Fore.YELLOW + f"start fetch {st_id}", flush=True)
        loc = stations_loc.iloc[row]  # lat and lon
        api_req = Forecast(loc)
        forecast = await api_req.get_json()
        forecast = await api_req.get_forecast(forecast)
        await data_q.put([forecast, loc])
        print(Fore.YELLOW + f"end fetch {st_id}", flush=True)


async def plot_data(num: int, data_q: asyncio.Queue) -> None:
    # create mpl plot
    ok_map = geopandas.read_file("data/cb_2018_40_bg_500k.shp")
    ok_map = ok_map.to_crs("epsg:4326")
    ok_map.plot(figsize=(12, 6))
    plt.title("Oklahoma Hourly Temperature (°F)")

    # get data from queue and plot
    while num > 0:
        print(Fore.CYAN + f"start plot {num}", flush=True)
        arg_loc = await data_q.get()
        arg, loc = arg_loc[0], arg_loc[1]
        lat, lon = loc[["latitude"]], loc[["longitude"]]
        plt.plot(lon, lat, color="black", marker=f"${arg}°F$", markersize=20)
        print(Fore.CYAN + f"finish plot {num}", flush=True)
        num -= 1


if __name__ == '__main__':
    print(Fore.BLUE + "started", flush=True)
    t0 = datetime.now()

    try:
        asyncio.run(main())
        plt.show()
    except Exception as e:
        print(f"Error in main(): {e}")

    dt = datetime.now() - t0
    print(Fore.BLUE + f"finished in {dt}", flush=True)
