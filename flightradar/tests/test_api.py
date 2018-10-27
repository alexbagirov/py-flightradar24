import os
import json
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from api import API, Area
from coordinates import Point


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def test_area_flights_loading(self):
        area = Area(Point(57.06, 55.00), Point(32.97, 36.46))
        data = self.api.get_area(area)

        self.assertIsInstance(data, str)
        d = json.loads(data)
        self.assertIsInstance(d, dict)
