var map;
var aircrafts = {};

class Aircraft {
    constructor(marker, speed, track) {
        this.marker = marker;
        this.speed = speed;
        this.track = track;

        this.oldLat = marker.lat;
        this.oldLng = marker.lng;
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
            var newAircraft = newAircrafts[aircraftId];
            var newPoint = new google.maps.LatLng(newAircraft['lat'],
                                                  newAircraft['lon']);

            aircrafts[aircraftId].oldLat = aircrafts[aircraftId].marker.getPosition().lat();
            aircrafts[aircraftId].oldLng = aircrafts[aircraftId].marker.getPosition().lng();

            aircrafts[aircraftId].track = newAircraft['track'];
            aircrafts[aircraftId].speed = newAircraft['speed'];
            aircrafts[aircraftId].marker.setIcon('icons/' + newAircraft['pic'] + '.png');

            var currentPosition = aircrafts[aircraftId].marker.getPosition();
            var distanceToPrevious = calcDistance(newPoint,
                new google.maps.LatLng(aircrafts[aircraftId].oldLat,
                    aircrafts[aircraftId].oldLng));
            var distanceToCurrent = calcDistance(currentPosition, newPoint);
            var speedDelta = distanceToCurrent / aircrafts[aircraftId].speed;

            if (distanceToCurrent < distanceToPrevious) {
                aircrafts[aircraftId].speed += speedDelta;
            }
            else {
                aircrafts[aircraftId].speed -= speedDelta;
            }
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
            aircrafts[aircraftId].marker.addListener('click', function() {
                window.loader.handleClick(aircraftId);
            });
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

function calcDistance(p1, p2) {
    return google.maps.geometry.spherical.computeDistanceBetween(p1, p2);
}

function moveMap(lat, lon) {
    let center = new google.maps.LatLng(lat, lon);
    map.panTo(center);
}