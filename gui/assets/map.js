var map;
var aircrafts = {};

class Aircraft {
    constructor(marker, speed, track) {
        this.marker = marker;
        this.speed = speed;
        this.track = track;
    }

    move(newPoint) {
        this.marker.setPosition(newPoint);
    }

    hide() {
        this.marker.setMap(null);
    }
}

window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.loader = channel.objects.aircraftManager;

        map.addListener('tilesloaded', function() {
            window.loader.paintAircrafts();
        });

        window.loader.startService();
    });
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 56.8454603, lng: 60.6424976},
        zoom: 8,
        disableDefaultUI: true,
        clickableIcons: false,
        zoomControl: true
    });
}

function addAircrafts(data) {
    let newAircrafts = JSON.parse(data);
    Object.keys(aircrafts).forEach(function(aircraftId, index) {
        if (aircraftId in newAircrafts) {
            let newPoint = {
                lat: newAircrafts[aircraftId]['lat'],
                lng: newAircrafts[aircraftId]['lon']
            };
            aircrafts[aircraftId].move(newPoint);
        }
        else {
            removeAircraft(aircraftId);
        }
    });

    Object.keys(newAircrafts).forEach(function(aircraftId, index) {
        if (!(aircraftId in aircrafts)) {
            let aircraft = newAircrafts[aircraftId];
            aircrafts[aircraftId] = new Aircraft(
                new google.maps.Marker({
                    position: {lat: aircraft['lat'], lng: aircraft['lon']},
                    map: map,
                    icon: 'icons/' + aircraft['pic'] + '.png'
                }),
                aircraft['speed'],
                aircraft['track']
            );
        }
    });
}

function moveAircrafts() {
    Object.keys(aircrafts).forEach(function(key, index) {
        let newPoint = google.maps.geometry.spherical.computeOffset(
            aircrafts[key].marker.position,
            aircrafts[key].speed * 0.514444,
            aircrafts[key].track
        );
        aircrafts[key].move(newPoint);
    });
}

function removeAircraft(id) {
    aircrafts[id].hide();
    delete aircrafts[id];
}

function getBounds() {
    return map.getBounds();
}