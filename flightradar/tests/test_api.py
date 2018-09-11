import os
import sys
from time import sleep
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from api import API, Area, BriefFlight, DetailedFlight


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def test_area_flights_loading(self):
        for flight in self.api.get_area(Area(57.06, 55.00, 32.97, 36.46)):
            self.assertIsInstance(flight, BriefFlight)

    def test_get_flight(self):
        flights = [flight for flight in
                   self.api.get_area(Area(57.06, 55.00, 32.97, 36.46))]
        sleep(4)
        self.assertIsInstance(self.api.get_flight(flights[0].id),
                              DetailedFlight)
