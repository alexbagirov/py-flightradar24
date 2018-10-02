import os
import sys
from urllib.request import urlopen, HTTPError, Request
from threading import Lock

from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QApplication)
from PyQt5.QtGui import QImage, QPixmap

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from gui.map import Map
from gui.details import DetailsPanel
from gui.manager import AircraftManager
from flightradar.api import API, HEADERS
from flightradar.models.flight import DetailedFlight


LOGO_URL = ('https://s3.eu-central-1.amazonaws.com/images.flightradar24.com'
            '/assets/airlines/logotypes/{}_{}.png')
ALT_LOGO_URL = ('https://www.flightradar24.com/'
                'static/images/data/operators/{}_logo0.png')


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)
        self.setWindowTitle('flightradar24')
        self.resize(1400, 800)

        self.api = API()
        self.map = Map(self)
        self.details = DetailsPanel(self)

        self.channel = QWebChannel()
        self.manager = AircraftManager(self)
        self.channel.registerObject('aircraftManager', self.manager)
        self.map.page().setWebChannel(self.channel)

        self.row = QHBoxLayout()
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.addWidget(self.map, 2)
        self.row.addWidget(self.details, 1)
        self.setLayout(self.row)

    def closeEvent(self, event):
        self.manager.stop_moves_thread()

    def set_info(self, flight: DetailedFlight):
        with Lock():
            self.details.widgets['airline'].setText(flight.airline)
            self.details.widgets['flight'].setText(flight.flight)
            self.details.widgets['route'].setText(
                '{} → {}'.format(flight.origin, flight.destination))

            self.details.widgets['registration'].setText(
                'Registration: {}'.format(flight.registration))
            self.details.widgets['altitude'].setText(
                'Altitude: {}'.format(str(flight.trail[0].altitude)))
            self.details.widgets['track'].setText(
                'Track: {}'.format(str(flight.trail[0].heading)))
            self.details.widgets['speed'].setText(
                'Speed: {}'.format(str(flight.trail[0].speed)))
            self.details.widgets['latitude'].setText(
                'Latitude: {}'.format(str(flight.trail[0].latitude)))
            self.details.widgets['longitude'].setText(str(
                'Longitude: {}'.format(flight.trail[0].longitude)))
            self.load_airline_logo(flight.iata, flight.icao)

    def load_airline_logo(self, iata: str, icao: str):
        try:
            data = urlopen(LOGO_URL.format(iata, icao)).read()
        except HTTPError:
            data = urlopen(Request(ALT_LOGO_URL.format(icao),
                                   headers=HEADERS)).read()
        image = QImage()
        image.loadFromData(data)
        pixmap = QPixmap(image)
        self.details.widgets['logo'].setPixmap(pixmap)


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
