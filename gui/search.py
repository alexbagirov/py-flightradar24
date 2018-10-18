from functools import partial
from urllib.request import urlopen, Request, HTTPError

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QGroupBox,
                             QPushButton, QLabel, QScrollArea, QFrame)

from flightradar.api import HEADERS
from gui.font import SMALL_FONT


class SearchPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.column = QVBoxLayout()

        self.query_field = QLineEdit()
        self.query_field.setPlaceholderText('Enter your query')
        self.query_field.setFont(SMALL_FONT)

        self.button = QPushButton(text='Search')
        self.button.setFont(SMALL_FONT)
        self.button.clicked.connect(self.search)

        self.results = QGroupBox('Results')
        self.results.setFont(SMALL_FONT)

        self.list = QVBoxLayout()
        self.list.setSpacing(0)
        self.list.setContentsMargins(0, 0, 0, 0)
        self.results.setLayout(self.list)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.results)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.horizontalScrollBar().hide()

        self.column.addWidget(self.query_field, 1)
        self.column.addWidget(self.button, 10)
        self.column.addWidget(self.scroll, 10)

        self.setLayout(self.column)

    def search(self):
        self.clear_search_results()
        for result, result_type in \
                self.parent().api.search(self.query_field.text()):
            group = QGroupBox()
            column = QVBoxLayout()
            text = ''

            if result_type == 'live':
                text = '<h3>{}</h3>\n{}'.format(result.iata,
                                                result.destination)
            elif result_type == 'airport':
                text = '<h3>{}</h3>'.format(result.label)

            label = QLabel()
            label.setText(text)
            label.setTextFormat(Qt.RichText)
            label.setFont(SMALL_FONT)
            label.setMargin(0)

            button = QPushButton('Open')
            button.clicked.connect(partial(self.parent().open_search_result,
                                           result))

            try:
                column.addWidget(self.load_search_logo(result.icao[:3]),
                                 alignment=Qt.AlignCenter)
            except (HTTPError, AttributeError):
                pass
            column.addWidget(label)
            column.addWidget(button)
            group.setLayout(column)
            self.list.addWidget(group, 0)

    @staticmethod
    def load_search_logo(url: str):
        data = urlopen(Request('https://www.flightradar24.com/'
                               'static/images/data/operators/'
                               '{}_logo0.png'.format(url),
                               headers=HEADERS)).read()

        label = QLabel()
        image = QImage()
        image.loadFromData(data)
        pixmap = QPixmap(image)
        label.setPixmap(pixmap)

        return label

    def clear_search_results(self):
        while self.list.count():
            child = self.list.takeAt(0)
            child.widget().deleteLater()
