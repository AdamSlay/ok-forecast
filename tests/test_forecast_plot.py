import unittest
from src.forecast_plot import Plot


class Test_Plot(unittest.TestCase):
    # Question: Does the class init with the proper values?
    def test_init(self) -> None:
        t_path = "2022-10-24--11-59"
        t_print = "Monday October 24, 2022 11:59 AM"
        plot = Plot(t_print, t_path)
        assert plot.t_path == t_path
        assert plot.t_print == t_print

    # Question: Does the function initialize a plot with the expected styling?
    # Tests:
    # 1. I honestly have no idea how to test this
    def test_init_plot(self):
        pass

    # Question: does the point get plotted in the correct location in the graph?
    # Tests:
    # 1. does it perform as expected?
    # 2. does it properly omit points that fall outside the designated lat/lon?
    # 3. does it correctly recognize temp vs wind?
    # 4. what if there are no args?
    def test_plot_point(self):
        pass

    # Question: Does the file get saved in the right place with the right name?
    # Tests:
    # 1. Does the /maps folder get created correctly?
    # 2. Does the /day folder get created correctly?
    # 3. Does the file get saved in the correct folder?
    # 4. Does teh file have the correct name?
    def test_finish_plot(self):
        pass
