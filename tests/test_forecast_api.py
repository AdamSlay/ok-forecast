import unittest
from src.forecast_api import Forecast


class Test_Forecast(unittest.TestCase):

    # Question: Does the class init with the proper values?
    def test_init(self) -> None:
        loc = [35, 94]
        fore = Forecast(loc)
        assert fore.lat == loc[0]
        assert fore.lon == loc[1]

    # Question: Is the correct forecast_url being returned?
    # Tests:
    # 1. patch the 'get' variable with a get response, then make sure the right forecast_url is extracted from the json
    # 2. does it properly recognize an invalid get response?
    # 3. does it properly recognize when a valid get response does not have a forecast_url?
    def test_get_json(self):
        pass

    # Question: Are the correct forecast parms being returned?
    # Tests:
    # 1. patch 'get' variable with get response, then make sure the right forecast data is being extracted from the json
    # 2. does it properly recognize an invalid get response?
    # 3. does it properly recognize when a valid response does not have the desired parms?
    def test_get_forecast(self):
        pass
