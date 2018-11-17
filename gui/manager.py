import json
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QWidget
from geopy.distance import distance


class AircraftManager(QObject):
    def __init__(self, program: QWidget, initial_position):
        super().__init__()
        self.app = program
        self.active = False
        self.moving_thread = threading.Thread(target=self.move_aircrafts)
        self.fetching_thread = threading.Thread(target=self.fetch_new_data)
        self.initial_position = initial_position
        self.aircrafts = {}

    @pyqtSlot(name='paintAircrafts')
    def paint_aircrafts(self):
        self.app.map.get_bounds_and_update_map()

    def add_aircrafts(self, data: str):
        data = json.loads(data)
        remove_queue = []

        for aircraft in self.aircrafts:
            if aircraft not in data:
                remove_queue.append(aircraft)
            else:
                updated_aircraft = data[aircraft]
                self.aircrafts[aircraft].old_lon = self.aircrafts[aircraft].lon
                self.aircrafts[aircraft].old_lat = self.aircrafts[aircraft].lat
                self.aircrafts[aircraft].track = updated_aircraft['track']
                self.aircrafts[aircraft].speed = updated_aircraft['speed']

                new_point = (updated_aircraft['lat'], updated_aircraft['lon'])
                cur_point = (self.aircrafts[aircraft].lat,
                             self.aircrafts[aircraft].lon)
                old_point = (self.aircrafts[aircraft].old_lat,
                             self.aircrafts[aircraft].old_lon)

                distance_to_old = distance(new_point, old_point).km
                distance_to_cur = distance(new_point, cur_point).km

                speed_delta = 0 if self.aircrafts[aircraft].speed == 0 \
                    else distance_to_cur / self.aircrafts[aircraft].speed
                if distance_to_cur < distance_to_old:
                    self.aircrafts[aircraft].speed += speed_delta
                else:
                    self.aircrafts[aircraft].speed -= speed_delta

                data[aircraft]['speed'] = self.aircrafts[aircraft].speed

        for aircraft in remove_queue:
            del self.aircrafts[aircraft]

        for aircraft in data:
            if aircraft not in self.aircrafts:
                self.aircrafts[aircraft] = Marker(data[aircraft]['lon'],
                                                  data[aircraft]['lat'],
                                                  data[aircraft]['track'],
                                                  data[aircraft]['speed'])

        self.app.map.add_aircrafts(json.dumps(data))

    def move_aircrafts(self):
        while self.active:
            self.app.map.move_aircrafts()
            sleep(1)

    def fetch_new_data(self):
        while self.active:
            self.paint_aircrafts()
            sleep(15)

    @pyqtSlot(name='startService')
    def start_service(self):
        self.active = True
        self.moving_thread.start()
        self.fetching_thread.start()
        if self.initial_position:
            self.app.map.page().runJavaScript(
                "moveMap({}, {});".format(*self.initial_position))

    def stop_moves_thread(self):
        self.active = False

    @pyqtSlot(str, name='handleClick')
    def show_flight_details(self, flight_id: int):
        threading.Thread(target=self.app.set_info,
                         args=(self.app.api.get_flight(flight_id),)).start()


class Marker:
    def __init__(self, lon: float, lat: float, track: int, speed: int):
        self.lon = lon
        self.lat = lat
        self.old_lon = lon
        self.old_lat = lat

        self.track = track
        self.speed = speed
