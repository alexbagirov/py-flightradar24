from coordinates import Waypoint


FIELDS = ['mode_s', 'lat', 'lon', 'track', 'alt', 'speed',
          'squawk', 'radar', 'model', 'registration', 'undefined',
          'origin', 'destination', 'iata', 'undefined2',
          'vertical_speed', 'icao', 'undefined3', 'airline']
FLIGHT_STRING = ('Flight {flight} from {origin} to {destination}. '
                 '{model} ({registration}) at {lat}, {lon} on altitude {alt}. '
                 'Speed: {speed}. Track: {track}.')


class BriefFlight:
    """Class for storing info for all flights on the map."""
    def __init__(self, flight_id, lat, lon, model, registration, origin,
                 destination, iata, icao, airline, mode_s=None, track=None,
                 alt=None, speed=None, squawk=None, radar=None,
                 vertical_speed=None, undefined=None, undefined2=None,
                 undefined3=None):
        self.id = flight_id
        self.mode_s = mode_s
        self.lat = lat
        self.lon = lon
        self.track = track
        self.alt = alt
        self.speed = speed
        self.squawk = squawk
        self.radar = radar
        self.model = model
        self.registration = registration
        self.undefined = undefined
        self.origin = origin
        self.destination = destination
        self.iata = iata
        self.undefined2 = undefined2
        self.vertical_speed = vertical_speed
        self.icao = icao
        self.undefined3 = undefined3
        self.airline = airline

    def __str__(self) -> str:
        return FLIGHT_STRING.format(flight=self.icao,
                                    origin=self.origin,
                                    destination=self.destination,
                                    model=self.model,
                                    registration=self.registration,
                                    lat=self.lat, lon=self.lon,
                                    alt=self.alt, speed=self.speed,
                                    track=self.track)

    @staticmethod
    def create(flight_id: str, data: list):
        """Static method for Flight instance creation."""
        return BriefFlight(flight_id=flight_id, **dict(zip(FIELDS, data)))

    @staticmethod
    def create_from_search(id: str, detail: dict, **_):
        """Static method for Flight instance creation from search results."""
        return BriefFlight(flight_id=id, lat=detail['lat'], lon=detail['lon'],
                           origin=detail['schd_from'],
                           destination=detail['schd_to'],
                           model=detail['ac_type'], registration=detail['reg'],
                           icao=detail['callsign'], iata=detail['flight'],
                           airline=detail['operator'])


class DetailedFlight:
    """Class for storing info of selected flight.
    Must be displayed separately."""
    def __init__(self, flight_id, flight, status, model, registration, airline,
                 origin, destination, trail):
        self.id = flight_id
        self.flight = flight
        self.status = status
        self.model = model
        self.registration = registration
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.trail = self.collect_trail(trail)

    @staticmethod
    def collect_trail(waypoints: list) -> list:
        """Converts JSON list of points into list of Waypoint instances."""
        return [Waypoint(point['lat'],
                         point['lng'],
                         point['alt'],
                         point['spd'],
                         point['hd']) for point in waypoints]

    @staticmethod
    def create(data: dict):
        """Static method for Flight instance creation."""
        return DetailedFlight(flight_id=data['identification']['id'],
                              flight=data['identification']['callsign'],
                              status=data['status']['text'],
                              model=data['aircraft']['model']['code'] if
                              data['aircraft']['model']['code'] else None,
                              registration=data['aircraft']['registration'],
                              airline=data['airline']['name'],
                              origin=data['airport']['origin']['name'],
                              destination=data['airport']['destination']['name'],
                              trail=data['trail'])

    def __str__(self) -> str:
        return 'Flight {} from {} to {}, {} ({}).'.format(self.flight,
                                                          self.origin,
                                                          self.destination,
                                                          self.model,
                                                          self.registration)
