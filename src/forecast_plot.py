import matplotlib.pyplot as plt
from pathlib import Path
from os import mkdir
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


class Plot:
    def __init__(self, t_print, t_path, arg, figure: int):
        self.arg = arg
        self.figure = figure
        self.t_print = t_print
        self.t_path = t_path
        self.color_map = plt.cm.get_cmap('nipy_spectral')

    def init_plot(self, state, st_map):
        # Initialize the plot with the desired styling
        plt.figure(self.figure, figsize=(10, 10), facecolor="0.7")
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        ax.set_facecolor("#87ceeb")  # trying out sky-blue | default = 'white'
        st_map.plot(ax=ax, color="white")
        plt.title(f"{state} Hourly {self.arg}  {self.t_print}")

    def plot_point(self, loc, st_map, arg=None, wdir=None):
        # Plot each point
        lon_min, lon_max = float(min(st_map.bounds.minx)), float(max(st_map.bounds.maxx))
        lat_min, lat_max = float(min(st_map.bounds.miny)), float(max(st_map.bounds.maxy))
        plt.figure(self.figure)
        arg = str(arg).split(' ')[0].zfill(2)
        lat, lon = float(loc[["latitude"]]), float(loc[["longitude"]])

        if lat_max > lat > lat_min and lon_max > lon > lon_min:
            if arg and not wdir:
                color_map = plt.cm.get_cmap('nipy_spectral')
                plt.scatter(lon, lat, c=int(arg), s=200, vmin=-20, vmax=125, cmap=color_map, marker=f"${arg}$")

            elif arg and wdir:
                color_map = plt.cm.get_cmap('turbo')
                dir_dict = {'N': '↑', 'S': '↓', 'E': '→', 'W': '←',
                            'NE': '↗', 'NW': '↖', 'SE': '↘', 'SW': '↙',
                            'ESE': '↘', 'ENE': '↗', 'NNE': '↗', 'NNW': '↖',
                            'SSE': '↘', 'SSW': '↙', 'WNW': '↖', 'WSW': '↙'}
                plt.scatter(lon, lat, c=int(arg), s=250, vmin=0, vmax=70, cmap=color_map,
                            marker=f"${arg} {dir_dict[wdir]}$")

    async def finish_plot(self, st):
        # Setup color-bar
        plt.figure(self.figure)
        cbar = plt.colorbar(shrink=.5)
        cbar.set_label(f"{self.arg}")
        try:
            mkdir("maps/")
        except FileExistsError:
            # Directory already exists
            pass
        title = self.arg.replace(' ', '-')
        path = Path(f'maps/{st}-hourly-{title}-{self.t_path}.png')
        plt.savefig(path)
