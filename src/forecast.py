import time
import asyncio
from colorama import Fore
from datetime import datetime
from meteostat import Stations
from forecast_api import Forecast
from forecast_plot import Plot


async def main() -> int:
    data_q = asyncio.Queue()
    num_stats, stations = create_df()
    task1 = asyncio.create_task(fetch_data(stations, data_q))
    task2 = asyncio.create_task(plot_data(num_stats, data_q))
    await task1, task2
    return 0


def create_df():
    # create dataframe with all OK stations using meteostat
    stations = Stations()
    stations = stations.region('US', 'OK')
    stations = stations.fetch()
    exclude = ['KLTS',
               'KBKN',
               'KRCE',
               'KPWA',
               'N/A']
    stations = stations[~stations.icao.isin(exclude)]  # these stations cause clutter in map. comment out to see
    num_stats = len(stations.index)
    return num_stats, stations


async def fetch_data(stations, data_q: asyncio.Queue) -> None:
    # separate station coordinates from stations
    coords = stations[["latitude", "longitude"]]

    # fetch data from weather.gov api
    for row, st_id in enumerate(stations["icao"]):
        print(Fore.YELLOW + f"start fetch {st_id}", flush=True)
        loc = coords.iloc[row]
        api_req = Forecast(loc)
        forecast = await api_req.get_json()
        forecast = await api_req.get_forecast(forecast)
        await data_q.put([forecast, loc])
        print(Fore.YELLOW + f"end fetch {st_id}", flush=True)


async def plot_data(num_stats: int, data_q: asyncio.Queue) -> None:
    # Initialize mpl plot with desired styling
    plot = Plot(t_print, t_path)
    plot.init_plot()

    # get data from queue and plot
    while num_stats > 0:
        print(Fore.CYAN + f"start plot {num_stats}", flush=True)
        arg_loc = await data_q.get()
        plot.plot_point(arg_loc)
        print(Fore.CYAN + f"finish plot {num_stats}", flush=True)
        num_stats -= 1

    # Set up the color-bar, save file, show map
    plot.finish_plot()


if __name__ == '__main__':
    print(Fore.BLUE + "started", flush=True)
    t0 = datetime.now()  # start_time for benchmark
    t_path = time.strftime('%Y-%m-%d--%H-%M')
    t_print = time.strftime('%A %B %d, %Y %I:%M %p')  # displayable time

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error in main(): {e}")
    finally:
        dt = datetime.now() - t0  # elapsed time
        print(Fore.BLUE + f"finished in {dt}", flush=True)
