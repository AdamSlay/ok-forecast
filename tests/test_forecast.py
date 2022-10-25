import unittest
from unittest import mock
from src.forecast_api import Forecast
from src.forecast_plot import Plot


class Test_Forecast(unittest.TestCase):
    def test_init(self) -> None:
        loc = [35, 94]
        fore = Forecast(loc)
        assert fore.lat == loc[0]
        assert fore.lon == loc[1]
        pass

    # @mock.patch()
    # def test_get_json(self):
    #    pass


class Test_Plot(unittest.TestCase):
    def test_init(self) -> None:
        t_path = "2022-10-24--11-59"
        t_print = "Monday October 24, 2022 11:59 AM"
        plot = Plot(t_print, t_path)
        assert plot.t_path == t_path
        assert plot.t_print == t_print


def test_create_df():
    pass


def test_fetch_data():
    pass


def test_plot_data():
    pass
