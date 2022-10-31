import unittest
from src.forecast_plot import Plot


class TestPlot(unittest.TestCase):
    # 1. Does the class init with the proper values?
    def test_init(self) -> None:
        t_path = "2022-10-24--11-59"
        t_print = "Monday October 24, 2022 11:59 AM"
        arg_str = "Temperature"
        fig_id = 41
        plot = Plot(t_print, t_path, arg_str, fig_id)
        assert plot.t_path == t_path
        assert plot.t_print == t_print
        assert plot.arg_str == arg_str
        assert plot.fig_id == fig_id

    # 1. Does the function initialize a plot with the expected styling?
    def test_init_plot(self):
        pass

    # 1. does the point get plotted in the correct location in the graph?
    # 2. does it properly omit points that fall outside the designated lat/lon?
    # 3. does it correctly recognize temp vs wind?
    # 4. what if there are no args?
    def test_plot_point(self):
        pass

    # 1. Does the /maps folder get created correctly?
    # 2. Does the /day folder get created correctly?
    # 3. Does the file get saved in the correct folder?
    # 4. Does teh file have the correct name?
    def test_finish_plot(self):
        pass
