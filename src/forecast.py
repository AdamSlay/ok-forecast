import time
import asyncio
import geopandas
from colorama import Fore
from datetime import datetime
from meteostat import Stations
from forecast_api import Forecast
from forecast_plot import Plot

# State and abbreviation
state_abv = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}
state_fp_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}

us_states = ['Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
             'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
             'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
             'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
             'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
             'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

us_map = geopandas.read_file("data/states/cb_2018_us_county_500k.shp")  # crs already epsg:4326


async def main() -> int:
    await asyncio.gather(*map(wait, us_states))
    # for state, st in state_abv.items():
    #   await wait(state, st, us_map, fig_id)
    return 0


async def wait(state):
    st = state_abv[state]
    fig_id = state_fp_codes[st]
    data_q = asyncio.Queue()
    st_map = us_map[us_map["STATEFP"] == state_fp_codes[st]]
    num_stats, stations = create_df(st)
    task1 = asyncio.create_task(fetch_data(stations, data_q))
    task2 = asyncio.create_task(plot_data(num_stats, fig_id, state, st, st_map, data_q))
    await task1, task2


def create_df(st):
    # create dataframe with all OK stations using meteostat
    stations = Stations()
    stations = stations.region('US', st)
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
        forecast_url = await api_req.get_json()
        forecast = await api_req.get_forecast(forecast_url)
        await data_q.put([forecast, loc])
        print(Fore.YELLOW + f"end fetch {st_id}", flush=True)


async def plot_data(num_stats: int, fig_id, state, st, st_map, data_q: asyncio.Queue) -> None:
    # Initialize mpl plot with desired styling
    temp_plot = Plot(t_print, t_path, "Temperature (F)", fig_id)
    temp_plot.init_plot(state, st_map)
    wind_plot = Plot(t_print, t_path, "Wind Speed (mph)", fig_id * 3)
    wind_plot.init_plot(state, st_map)

    # get data from queue and plot
    while num_stats > 0:
        print(Fore.CYAN + f"start plot {num_stats}", flush=True)
        args_loc = await data_q.get()
        loc = args_loc[1]
        args = args_loc[0]
        if args:
            temp_plot.plot_point(loc, st_map, args[0])
            wind_plot.plot_point(loc, st_map, args[1], args[2])
        print(Fore.CYAN + f"finish plot {num_stats}", flush=True)
        num_stats -= 1

    # Set up the color-bar, save file, show map
    await temp_plot.finish_plot(st)
    await wind_plot.finish_plot(st)


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
