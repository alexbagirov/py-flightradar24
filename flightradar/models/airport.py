AIRPORT_STRING = '{label} located at {lat}, {lon}.'


class Airport:
    """Class for storing airport info."""
    def __init__(self, label: str, lat: float, lon: float, size: int):
        self.label = label
        self.lat = lat
        self.lon = lon
        self.size = size

    def __str__(self) -> str:
        return AIRPORT_STRING.format(label=self.label,
                                     lat=self.lat, lon=self.lon)

    @staticmethod
    def create_from_search(detail: dict, **kwargs):
        """Static method for Airport instance creation from search results."""
        return Airport(kwargs['res_label'], detail['lat'], detail['lon'],
                       detail['size'])
