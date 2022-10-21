import geopandas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


class Plot:
    def __init__(self, t_print):
        self.t_print = t_print
        self.fig = plt.figure(figsize=(12, 7), facecolor="0.1")
        self.ax = self.fig.add_subplot(111)
        self.color_map = None

    def init_plot(self):
        # Initialize the plot with the desired styling
        self.color_map = plt.cm.get_cmap('nipy_spectral')
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.set_facecolor("#87ceeb")  # trying out sky-blue | default = 'white'
        ok_map = geopandas.read_file("data/cb_2018_40_bg_500k.shp")  # crs already epsg:4326
        ok_map.plot(ax=self.ax, color="gray")
        plt.title(f"Oklahoma Hourly Temperature (°F)  {self.t_print.replace('-', ', ')}", color="white")

    def plot_point(self, arg_loc):
        # Plot each point
        arg, loc = arg_loc[0], arg_loc[1]
        lat, lon = loc[["latitude"]], loc[["longitude"]]
        if arg:
            plt.scatter(lon, lat, c=arg, s=250, vmin=-20, vmax=125, cmap=self.color_map, marker=f"${arg}°$")

    def set_colorbar(self):
        # Setup color-bar
        cbax = inset_axes(self.ax, width="3%", height="50%", loc='center left')
        cbar = plt.colorbar(cax=cbax, shrink=.5)
        cbar.set_label("Temperature °F")
