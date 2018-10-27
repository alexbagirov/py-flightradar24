import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from models.flight import BriefFlight, DetailedFlight, get_image_id, \
    flights_to_json
from models.airport import Airport
from models.operator import Operator
from coordinates import Waypoint


class TestModels(unittest.TestCase):
    def test_brief_flight_create(self):
        flight = BriefFlight.create('123',
                                    ['4CA6E6', 56.4135, 58.7894, 84, 34975,
                                     506, '2737', 'T-UWUF7', 'A332',
                                     'EI-FSE', 1539972060, 'VKO', 'CGO',
                                     'I49821', 0, 0, 'RSY9821', 0, 'RSY'])
        self.assertIsInstance(flight, BriefFlight)
        self.assertEquals(flight.id, '123')
        self.assertEquals(flight.lat, 56.4135)
        self.assertEquals(flight.lon, 58.7894)
        self.assertEquals(flight.registration, 'EI-FSE')
        self.assertEquals(flight.icao, 'RSY9821')
        self.assertEquals(flight.origin, 'VKO')
        self.assertEquals(flight.destination, 'CGO')
        self.assertEquals(flight.iata, 'I49821')

        self.assertEquals(str(flight), 'Flight RSY9821 from VKO to CGO. '
                                       'A332 (EI-FSE) at 56.4135, '
                                       '58.7894 on altitude 34975. '
                                       'Speed: 506. Track: 84.')

        self.assertEquals(flights_to_json([flight]),
                          '{"123": {"id": "123", "lat": 56.4135, '
                          '"lon": 58.7894, "track": 84, '
                          '"speed": 506, "pic": "7"}}')

    def test_create_brief_flight_from_search(self):
        flight = BriefFlight.create_from_search(
            {'lat': 46.9,
             'lon': 39.2,
             'schd_from': 'DME',
             'schd_to': 'SIP',
             'ac_type': 'A320',
             'route': 'Moscow (DME) ⟶ Simferopol (SIP)',
             'logo': 'fr24:SVR_logo0.png',
             'reg': 'VP-BFZ',
             'callsign': 'SVR35',
             'flight': 'U635',
             'operator': 'SVR'},
            res_id='1e452b1f')

        self.assertEquals(flight.lat, 46.9)
        self.assertEquals(flight.lon, 39.2)
        self.assertEquals(flight.iata, 'U635')
        self.assertEquals(flight.airline, 'SVR')
        self.assertEquals(flight.id, '1e452b1f')
        self.assertEquals(flight.registration, 'VP-BFZ')
        self.assertEquals(flight.model, 'A320')

    def test_detailed_flight_create(self):
        flight = DetailedFlight.create(
            {'identification':
                {'id': '1e44d5e7',
                 'row': 4827800814,
                 'number': {'default': 'LH718',
                            'alternative': None},
                 'callsign': 'DLH718'},
             'status':
                 {'live': True,
                  'text': 'Estimated- 09:30',
                  'icon': 'green',
                  'estimated': None,
                  'ambiguous': False,
                  'generic':
                      {'status':
                          {'text': 'estimated',
                           'color': 'green',
                           'type': 'arrival'},
                       'eventTime':
                           {'utc': 1539995454,
                            'local': 1540027854}}},
             'level': 'limited',
             'aircraft':
                 {'model':
                      {'code': 'A359', 'text': 'Airbus A350-941'},
                  'registration': 'D-AIXK',
                  'hex': '3c670b',
                  'age': None,
                  'msn': None,
                  },
             'airline':
                 {'name': 'Lufthansa',
                  'short': 'Lufthansa',
                  'code': {'iata': 'LH', 'icao': 'DLH'},
                  'url': 'lufthansa-dlh'},
             'owner': None,
             'airspace': None,
             'airport':
                 {'origin':
                     {'name': 'Munich Airport',
                      'code': {'iata': 'MUC', 'icao': 'EDDM'},
                      'position': {'latitude': 48.353779,
                                   'longitude': 11.78608,
                                   'altitude': 1487,
                                   'region': {'city': 'Munich'}}},
                  'destination':
                      {'name': 'Seoul Incheon International Airport',
                       'code': {'iata': 'ICN', 'icao': 'RKSI'},
                       'position': {'latitude': 37.46907,
                                    'longitude': 126.4505,
                                    'altitude': 23,
                                    'region': {'city': 'Seoul'}}}
                  },
             'trail': [{'lat': 56.412552,
                        'lng': 59.906784,
                        'alt': 38975,
                        'spd': 536,
                        'ts': 1539973827,
                        'hd': 92},
                       {'lat': 56.419189,
                        'lng': 59.635288,
                        'alt': 39000,
                        'spd': 534,
                        'ts': 1539973765,
                        'hd': 92},
                       {'lat': 56.424942,
                        'lng': 59.359901,
                        'alt': 39025,
                        'spd': 535,
                        'ts': 1539973703,
                        'hd': 92},
                       {'lat': 56.428162,
                        'lng': 59.082474,
                        'alt': 39000,
                        'spd': 534,
                        'ts': 1539973641,
                        'hd': 86},
                       {'lat': 56.414471,
                        'lng': 58.809643,
                        'alt': 39000,
                        'spd': 530,
                        'ts': 1539973579,
                        'hd': 84},
                       {'lat': 56.399479,
                        'lng': 58.529408,
                        'alt': 39000,
                        'spd': 530,
                        'ts': 1539973516,
                        'hd': 84},
                       {'lat': 56.38216,
                        'lng': 58.218185,
                        'alt': 39000,
                        'spd': 531,
                        'ts': 1539973446,
                        'hd': 84}]
             })

        self.assertEquals(flight.id, '1e44d5e7')
        self.assertEquals(flight.origin, 'Munich')
        self.assertEquals(flight.destination, 'Seoul')
        self.assertEquals(flight.flight, 'DLH718')
        self.assertEquals(flight.airline, 'Lufthansa')
        self.assertEquals(flight.model, 'A359')

        trail = [Waypoint(56.412552, 59.906784, 38975, 536, 92),
                 Waypoint(56.419189, 59.635288, 39000, 534, 92),
                 Waypoint(56.424942, 59.359901, 39025, 535, 92),
                 Waypoint(56.428162, 59.082474, 39000, 534, 86),
                 Waypoint(56.414471, 58.809643, 39000, 530, 84),
                 Waypoint(56.399479, 58.529408, 39000, 530, 84),
                 Waypoint(56.38216, 58.218185, 39000, 531, 84)]

        self.assertEquals(flight.trail, trail)
        self.assertEquals(str(flight),
                          'Flight DLH718 from Munich to Seoul, A359 (D-AIXK).')

    def test_aircraft_image_by_track(self):
        for i in range(0, 25):
            self.assertEquals(get_image_id(15 * i), str(i + 1))

    def test_airport_create(self):
        airport = Airport.create_from_search({'lat': 56.743099,
                                              'lon': 60.802719,
                                              'size': 60606},
                                             res_id='SVX',
                                             res_label='Yekaterinburg '
                                                       'Koltsovo Airport '
                                                       '(SVX / USSS)')
        self.assertEquals(airport.lat, 56.743099)
        self.assertEquals(airport.lon, 60.802719)
        self.assertEquals(airport.size, 60606)
        self.assertEquals(airport.label, 'Yekaterinburg Koltsovo Airport '
                                         '(SVX / USSS)')

        self.assertEquals(str(airport),
                          'Yekaterinburg Koltsovo Airport (SVX / USSS) '
                          'located at 56.743099, 60.802719.')

    def test_operator_create(self):
        operator = Operator.create_from_search({'iata': 'SU',
                                                'logo': 'su.jpg'},
                                               res_label='Aeroflot',
                                               res_name='Aeroflot - '
                                                        'Russian Airlines')

        self.assertEquals(operator.iata, 'SU')
        self.assertEquals(operator.logo, 'su.jpg')
        self.assertEquals(operator.name, 'Aeroflot - Russian Airlines')
        self.assertEquals(operator.label, 'Aeroflot')

        self.assertEquals(str(operator), 'Aeroflot')
