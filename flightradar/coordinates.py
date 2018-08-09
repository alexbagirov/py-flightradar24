class Area:
    def __init__(self, min_lat: float, max_lat: float,
                 min_lon: float, max_lon: float):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon

    def __str__(self) -> str:
        """Allows to unpack data this way: *area"""
        return '{}, {}, {}, {}'.format(self.min_lat, self.max_lat,
                                       self.min_lon, self.max_lon)

    def __iter__(self):
        return (coord for coord in (self.min_lat, self.max_lat,
                                    self.min_lon, self.max_lon))


class Waypoint:
    """Class for collecting aircraft checkins on the map."""
    def __init__(self, latitude, longitude, altitude, speed, heading):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.heading = heading

    def __str__(self) -> str:
        return '{} {}'.format(self.latitude, self.longitude)
