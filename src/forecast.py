import time
import asyncio
import geopandas
from colorama import Fore
from datetime import datetime
from meteostat import Stations
from forecast_api import Forecast
from forecast_plot import Plot

# State, Abbreviation, FP code
us_states = [
    ["Alabama", "AL", "01"], ["Arizona", "AZ", "04"], ["Arkansas", "AR", "05"], ["California", "CA", "06"],
    ["Colorado", "CO", "08"], ["Connecticut", "CT", "09"], ["Delaware", "DE", "10"], ["Florida", "FL", "12"],
    ["Georgia", "GA", "13"], ["Idaho", "ID", "16"], ["Illinois", "IL", "17"], ["Indiana", "IN", "18"],
    ["Iowa", "IA", "19"], ["Kansas", "KS", "20"], ["Kentucky", "KY", "21"], ["Louisiana", "LA", "22"],
    ["Maine", "ME", "23"], ["Maryland", "MD", "24"], ["Massachusetts", "MA", "25"], ["Michigan", "MI", "26"],
    ["Minnesota", "MN", "27"], ["Mississippi", "MS", "28"], ["Missouri", "MO", "29"], ["Montana", "MT", "30"],
    ["Nebraska", "NE", "31"], ["Nevada", "NV", "32"], ["New Hampshire", "NH", "33"], ["New Jersey", "NJ", "34"],
    ["New Mexico", "NM", "35"], ["New York", "NY", "36"], ["North Carolina", "NC", "37"], ["North Dakota", "ND", "38"],
    ["Ohio", "OH", "39"], ["Oklahoma", "OK", "40"], ["Oregon", "OR", "41"], ["Pennsylvania", "PA", "42"],
    ["Rhode Island", "RI", "44"], ["South Carolina", "SC", "45"], ["South Dakota", "SD", "46"],
    ["Tennessee", "TN", "47"], ["Texas", "TX", "48"], ["Utah", "UT", "49"], ["Vermont", "VT", "50"],
    ["Virginia", "VA", "51"], ["Washington", "WA", "53"], ["West Virginia", "WV", "54"], ["Wisconsin", "WI", "55"],
    ["Wyoming", "WY", "56"],
]

# Only load the full map once
us_map = geopandas.read_file("data/cb_2018_us_county_500k.shp")  # crs already epsg:4326


async def main() -> int:
    await asyncio.gather(*map(loop, us_states))
    return 0


async def loop(state: list) -> None:
    # main loop for each state
    state_abv = state[1]
    state_fp = state[2]
    st_map = us_map[us_map["STATEFP"] == state_fp]
    num_stats, stations = create_df(state_abv)

    data_q = asyncio.Queue()
    task_1 = asyncio.create_task(fetch_data(stations, data_q))
    task_2 = asyncio.create_task(plot_data(num_stats, state, st_map, data_q))
    await task_1, task_2


def create_df(state_abv: str):
    # create dataframe with all stations in state using meteostat
    stations = Stations()
    stations = stations.region('US', state_abv)
    stations = stations.fetch()
    exclude = ['N/A']
    stations = stations[~stations.icao.isin(exclude)]  # exclude invalid stations
    num_stats = len(stations.index)
    return num_stats, stations


async def fetch_data(stations, data_q: asyncio.Queue) -> None:
    # separate station coordinates from stations
    coords = stations[["latitude", "longitude"]]

    # fetch data from weather.gov api and put in Queue
    for row, st_id in enumerate(stations["icao"]):
        loc = coords.iloc[row]
        api_req = Forecast(loc)
        forecast_url = await api_req.get_json()
        forecast_args = await api_req.get_forecast(forecast_url)
        await data_q.put([forecast_args, loc])


async def plot_data(num_stats: int, state: list, st_map, data_q: asyncio.Queue) -> None:
    state_full = state[0]
    state_abv = state[1]
    fig_id = state[2]

    # Initialize mpl plot with desired styling
    temp_plot = Plot(t_print, t_path, "Temperature (F)", fig_id)
    wind_plot = Plot(t_print, t_path, "Wind Speed (mph)", fig_id * 100)  # * 100 to make a second unique ID
    temp_plot.init_plot(state_full, st_map)
    wind_plot.init_plot(state_full, st_map)

    # get data from Queue and plot each point
    while num_stats > 0:
        print(Fore.CYAN + f"{state_abv} - start plot {num_stats}", flush=True)
        args_loc = await data_q.get()  # gets [forecast_args, loc] from fetch_data()
        args = args_loc[0]
        loc = args_loc[1]
        if args:
            temp_plot.plot_point(loc, st_map, args[0])
            wind_plot.plot_point(loc, st_map, args[1], args[2])
        print(Fore.CYAN + f"{state_abv} - finish plot {num_stats}", flush=True)
        num_stats -= 1

    # Set up color-bar, save figs to /maps
    await temp_plot.finish_plot(state_abv)
    await wind_plot.finish_plot(state_abv)


if __name__ == '__main__':
    print(Fore.BLUE + "started", flush=True)
    t0 = datetime.now()  # start_time for benchmark
    t_path = time.strftime('%Y-%m-%d--%H-%M')
    t_print = time.strftime('%a %B %d, %Y %H:%M')  # displayable time

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Unexpected Error in main(): {e}")
    finally:
        dt = datetime.now() - t0  # elapsed time
        print(Fore.BLUE + f"finished in {dt}", flush=True)
