import os
import sys
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from gui.map import Map
from flightradar.api import API


class AircraftManager(QObject):
    def __init__(self, program: QWidget):
        super().__init__()
        self.app = program
        self.active = False
        self.moving_thread = threading.Thread(target=self.move_aircrafts)
        self.fetching_thread = threading.Thread(target=self.fetch_new_data)

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

    def stop_moves_thread(self):
        self.active = False


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)
        self.setWindowTitle('flightradar24')
        self.resize(900, 600)

        self.api = API()
        self.map = Map(self)

        self.channel = QWebChannel()
        self.manager = AircraftManager(self)
        self.channel.registerObject('aircraftManager', self.manager)
        self.map.page().setWebChannel(self.channel)

        self.column = QVBoxLayout()
        self.column.setContentsMargins(0, 0, 0, 0)
        self.column.addWidget(self.map)
        self.setLayout(self.column)

    def closeEvent(self, event):
        self.manager.stop_moves_thread()


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
