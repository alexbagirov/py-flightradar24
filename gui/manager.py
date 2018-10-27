import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QWidget


class AircraftManager(QObject):
    def __init__(self, program: QWidget, initial_position):
        super().__init__()
        self.app = program
        self.active = False
        self.moving_thread = threading.Thread(target=self.move_aircrafts)
        self.fetching_thread = threading.Thread(target=self.fetch_new_data)
        self.initial_position = initial_position

    @pyqtSlot(name='paintAircrafts')
    def paint_aircrafts(self):
        self.app.map.get_bounds_and_update_map()

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
