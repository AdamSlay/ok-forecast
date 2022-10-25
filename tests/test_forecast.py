import src
from src.forecast_api import Forecast
from src.forecast_plot import Plot
from meteostat import Stations


def test_Forecast() -> None:
    loc = [35, 94]
    fore = Forecast(loc)
    assert fore.lat == loc[0]
    assert fore.lon == loc[1]
    pass


def test_Plot():
    t_path = "2022-10-24--11-59"
    t_print = "Monday October 24, 2022 11:59 AM"
    plot = Plot(t_print, t_path)
    assert plot.t_path == t_path
    assert plot.t_print == t_print
    pass


def test_create_df():
    pass


def test_fetch_data():
    pass


def test_plot_data():
    pass
