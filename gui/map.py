import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from flightradar.coordinates import Area, Point
from flightradar.api import API


class Map(QWebEngineView, QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.map_page = MapPage()
        self.setPage(self.map_page)
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'assets/map.html'))
        self.load(QUrl.fromLocalFile(html_path))

        self.api = API()

    def get_bounds_and_update_map(self):
        self.page().runJavaScript("getBounds()", self.update_map)

    def update_map(self, data: dict):
        area = Area(Point(data['f']['f'], data['f']['b']),
                    Point(data['b']['b'], data['b']['f']))
        aircrafts = self.api.get_area(area)
        self.add_aircrafts(aircrafts)

    def add_aircrafts(self, data: str) -> None:
        self.page().runJavaScript("addAircrafts('{}')".format(data))

    def move_aircrafts(self):
        self.page().runJavaScript("moveAircrafts()")


class MapPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, source):
        print('Message at line {}: {}'.format(line, msg))