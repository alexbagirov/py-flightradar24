#!/bin/bash

pyinstaller gui/main.py -F \
--add-data gui/assets/map.html:gui/assets \
--add-data gui/assets/map.js:gui/assets \
--add-data gui/assets/icons/*.png:gui/assets/icons