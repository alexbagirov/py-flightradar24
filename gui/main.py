import os
import sys
from threading import Lock
from urllib.request import urlopen, HTTPError, Request

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QApplication)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from flightradar.api import API, HEADERS
from flightradar.models.flight import DetailedFlight, BriefFlight
from flightradar.models.airport import Airport
from gui.details import DetailsPanel
from gui.manager import AircraftManager
from gui.map import Map
from gui.search import SearchPanel
from gui.argparser import AP

LOGO_URL = ('https://s3.eu-central-1.amazonaws.com/images.flightradar24.com'
            '/assets/airlines/logotypes/{}_{}.png')
ALT_LOGO_URL = ('https://www.flightradar24.com/'
                'static/images/data/operators/{}_logo0.png')


class MainWindow(QWidget):
    def __init__(self, initial_position):
        QWidget.__init__(self, parent=None)
        self.setWindowTitle('flightradar24')
        self.resize(1400, 800)

        self.api = API()
        self.map = Map(self)
        self.details = DetailsPanel(self)
        self.search = SearchPanel(self)

        self.channel = QWebChannel()
        self.manager = AircraftManager(self, initial_position)
        self.channel.registerObject('aircraftManager', self.manager)
        self.map.page().setWebChannel(self.channel)

        _row = QHBoxLayout()
        _row.setContentsMargins(0, 0, 0, 0)
        _row.addWidget(self.map, 2)
        _row.addWidget(self.details, 1)
        _row.addWidget(self.search, 1)
        self.setLayout(_row)

        self.logos = {}

    def closeEvent(self, _):
        self.manager.stop_moves_thread()

    def set_info(self, flight: DetailedFlight):
        lock = Lock()
        with lock:
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
        logo = (iata, icao)

        if logo in self.logos:
            self.details.widgets['logo'].setPixmap(self.logos[logo])

        try:
            data = urlopen(LOGO_URL.format(iata, icao)).read()
        except HTTPError:
            try:
                data = urlopen(Request(ALT_LOGO_URL.format(icao),
                                       headers=HEADERS)).read()
            except HTTPError:
                pass
        image = QImage()
        image.loadFromData(data)
        pixmap = QPixmap(image)

        self.logos[logo] = pixmap
        self.details.widgets['logo'].setPixmap(pixmap)

    def open_search_result(self, result: (BriefFlight, Airport)):
        self.map.focus_on_point(result.lat, result.lon)
        if hasattr(result, 'id'):
            self.manager.show_flight_details(result.id)


if __name__ == '__main__':
    parser = AP()
    coordinates = parser.parse()
    app = QApplication(sys.argv)
    window = MainWindow(coordinates if coordinates else None)
    window.show()
    sys.exit(app.exec_())
