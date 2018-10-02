from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox,
                             QGridLayout)
from PyQt5.QtGui import QFont


class DetailsPanel(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self, parent=main_window)
        self.column = QVBoxLayout()
        self.widgets = {key: QLabel() for key in ('logo', 'airline', 'flight',
                                                  'route', 'registration',
                                                  'altitude', 'track', 'speed',
                                                  'radar', 'latitude',
                                                  'longitude')}

        for widget in self.widgets:
            self.widgets[widget].setFont(QFont("Manjari", 16))

        self.column.addWidget(self.widgets['logo'], 1, Qt.AlignCenter)
        self.widgets['route_group'] = QGroupBox('Route')
        self.widgets['aircraft_group'] = QGroupBox('Aircraft')
        self.widgets['route_group'].setFont(QFont("Manjari", 12))
        self.widgets['aircraft_group'].setFont(QFont("Manjari", 12))
        self.column.addWidget(self.widgets['route_group'], 1)
        self.column.addWidget(self.widgets['aircraft_group'], 2)

        route_grid = QGridLayout()
        route_grid.addWidget(self.widgets['airline'], 0, 0, Qt.AlignCenter)
        route_grid.addWidget(self.widgets['flight'], 0, 1, Qt.AlignCenter)
        route_grid.addWidget(self.widgets['route'], 1, 0, 1, 2, Qt.AlignCenter)
        self.widgets['route_group'].setLayout(route_grid)

        aircraft_grid = QGridLayout()
        aircraft_grid.addWidget(self.widgets['registration'], 0, 0)
        aircraft_grid.addWidget(self.widgets['altitude'], 1, 0)
        aircraft_grid.addWidget(self.widgets['track'], 2, 0)
        aircraft_grid.addWidget(self.widgets['speed'], 3, 0)
        aircraft_grid.addWidget(self.widgets['latitude'], 4, 0)
        aircraft_grid.addWidget(self.widgets['longitude'], 4, 1)
        self.widgets['aircraft_group'].setLayout(aircraft_grid)

        self.setLayout(self.column)
