import matplotlib.pyplot as plt
from colorama import Fore
from pathlib import Path
from os import mkdir


class Plot:
    def __init__(self, t_print: str, t_path: str, arg_str: str, fig_id: int) -> None:
        self.t_print = t_print
        self.t_path = t_path
        self.arg_str = arg_str
        self.fig_id = fig_id

    def init_plot(self, state, st_map) -> None:
        # Initialize the plot with the desired styling
        try:
            plt.figure(self.fig_id, figsize=(10, 8), facecolor="0.6")
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            ax.set_facecolor("#87ceeb")  # sky-blue
            st_map.plot(ax=ax, color="white")
            plt.title(f"{state} Hourly {self.arg_str}  {self.t_print}")
        except Exception as e:
            print(Fore.RED + f"Error in init_plot while working on {self.fig_id}: {e}", flush=True)

    def plot_point(self, loc, st_map, arg_val=None, wdir=None) -> None:
        # Plot each point
        try:
            plt.figure(self.fig_id)  # set mpl state to current object's figure
            lat_min, lat_max = float(min(st_map.bounds.miny)), float(max(st_map.bounds.maxy))  # latitude range
            lon_min, lon_max = float(min(st_map.bounds.minx)), float(max(st_map.bounds.maxx))  # longitude range
            lat, lon = float(loc[["latitude"]]), float(loc[["longitude"]])
            arg_val = str(arg_val).split(' ')[0].zfill(2)  # add leading 0 to make all markers same size

            if lat_max > lat > lat_min and lon_max > lon > lon_min:  # exclude outlying lat,lon
                if wdir:
                    color_map = plt.cm.get_cmap('turbo')
                    dir_dict = {'N': '↑', 'S': '↓', 'E': '→', 'W': '←',
                                'NE': '↗', 'NW': '↖', 'SE': '↘', 'SW': '↙',
                                'ESE': '↘', 'ENE': '↗', 'NNE': '↗', 'NNW': '↖',
                                'SSE': '↘', 'SSW': '↙', 'WNW': '↖', 'WSW': '↙'}
                    plt.scatter(lon, lat, c=int(arg_val), s=250, vmin=0, vmax=70, cmap=color_map,
                                marker=f"${arg_val} {dir_dict[wdir]}$")
                else:
                    color_map = plt.cm.get_cmap('nipy_spectral')
                    plt.scatter(lon, lat, c=int(arg_val), s=200, vmin=-20, vmax=125, cmap=color_map,
                                marker=f"${arg_val}$")

        except Exception as e:
            print(Fore.RED + f"Error in plot_point while working on {self.fig_id}: {e}", flush=True)

    def plot_null_point(self, loc, st_map):
        # If there is no arg data, simply plot a red dot at the station location
        try:
            plt.figure(self.fig_id)
            lat_min, lat_max = float(min(st_map.bounds.miny)), float(max(st_map.bounds.maxy))  # latitude range
            lon_min, lon_max = float(min(st_map.bounds.minx)), float(max(st_map.bounds.maxx))  # longitude range
            lat, lon = float(loc[["latitude"]]), float(loc[["longitude"]])

            if lat_max > lat > lat_min and lon_max > lon > lon_min:  # exclude outlying lat,lon
                if "Temp" in self.arg_str:
                    color_map = plt.cm.get_cmap('nipy_spectral')
                    plt.scatter(lon, lat, c=119, s=30, vmin=-20, vmax=125, cmap=color_map, marker=".")
                elif "Wind" in self.arg_str:
                    color_map = plt.cm.get_cmap('turbo')
                    plt.scatter(lon, lat, c=65, s=30, vmin=0, vmax=70, cmap=color_map, marker=".")

        except Exception as e:
            print(Fore.RED + f"Error in plot_null_point while working on {self.fig_id}: {e}", flush=True)

    async def finish_plot(self, state_abv: str) -> None:
        print(Fore.LIGHTBLUE_EX + f"finish_plot: {self.fig_id}", flush=True)
        try:
            # Setup color-bar
            plt.figure(self.fig_id)
            cbar = plt.colorbar(shrink=.5)
            cbar.set_label(f"{self.arg_str}")

            # create maps dir and save
            try:
                mkdir("maps/")
            except FileExistsError:
                # Directory already exists
                pass
            title = self.arg_str[:4]  # first 4 of Arg: 'Temp' or 'Wind'
            path = Path(f'maps/{state_abv}-hourly-{title}-{self.t_path}.png')
            plt.savefig(path)
            plt.close()
            print(Fore.LIGHTBLUE_EX + f"{self.fig_id} Done", flush=True)
        except Exception as e:
            print(Fore.RED + f"Error in finish_plot while working on {self.fig_id}: {e}", flush=True)
