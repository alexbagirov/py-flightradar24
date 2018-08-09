from urllib.request import urlopen, Request
from coordinates import Area
from flights import BriefFlight, DetailedFlight
import logging
import json

FLIGHTS_API_PATTERN = ('https://data-live.flightradar24.com/zones'
                       '/fcgi/feed.js?bounds={},{},{},{}'
                       '&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1'
                       '&estimated=1&maxage=14400&gliders=1&stats=1')
FLIGHT_API_PATTERN = ('https://data-live.flightradar24.com/clickhandler/'
                      '?version=1.5&flight={}')
HEADERS = {'Connection': 'keep-alive',
           'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; '
                          'x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome')}


class API:
    """Main API class for FlightRadar24 interaction."""
    def __init__(self):
        self.logger = logging.getLogger('API')
        self.logger.setLevel(logging.INFO)
        log_handler = logging.StreamHandler()
        log_handler.setLevel(logging.INFO)
        log_fmt = logging.Formatter('[{name}]: {message}\n', style='{')
        log_handler.setFormatter(log_fmt)
        self.logger.addHandler(log_handler)

    def get_flights(self, area: Area):
        """Returns all available flights within the specified area."""
        self.logger.info('Getting flights in [{}]'.format(area))
        req = Request(FLIGHTS_API_PATTERN.format(*area),
                      headers=HEADERS)
        return self.parse_flights(json.loads(urlopen(req).read().decode()))

    @staticmethod
    def parse_flights(data: dict):
        """Finds all flights in the response and builds their instances."""
        for key in data:
            if type(data[key]) == list:
                yield BriefFlight.create(key, data[key])

    def get_flight(self, flight_id: str) -> DetailedFlight:
        """Gets more detailed info about the specified flight."""
        self.logger.info('Getting info for flight {}'.format(flight_id))
        req = Request(FLIGHT_API_PATTERN.format(flight_id),
                      headers=HEADERS)
        return DetailedFlight.create(json.loads(urlopen(req).read().decode()))


if __name__ == '__main__':
    api = API()
    print(api.get_flight('1d70550f'))
    for flight in api.get_flights(Area(57.06, 55.00, 32.97, 36.46)):
        print(flight)
