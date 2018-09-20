var map;
var aircrafts = {};

class Aircraft {
    constructor(marker, speed, track) {
        this.marker = marker;
        this.speed = speed;
        this.track = track;
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
    removeAircrafts();

    let newAircrafts = JSON.parse(data);
    newAircrafts.forEach(function(aircraft) {
        aircrafts[aircraft['id']] = new Aircraft(
            new google.maps.Marker({
                position: {lat: aircraft['lat'], lng: aircraft['lon']},
                map: map,
                icon: 'icons/' + aircraft['pic'] + '.png'
            }),
            aircraft['speed'],
            aircraft['track']
        );
    });
}

function moveAircrafts() {
    Object.keys(aircrafts).forEach(function(key, index) {
        let newPoint = google.maps.geometry.spherical.computeOffset(
            aircrafts[key].marker.position,
            aircrafts[key].speed * 0.514444,
            aircrafts[key].track
        );
        aircrafts[key].marker.setPosition(newPoint);
    });
}

function removeAircrafts() {
    Object.keys(aircrafts).forEach(function(key, index) {
        aircrafts[key].marker.setMap(null);
        delete aircrafts[key];
    });
}

function getBounds() {
    return map.getBounds();
}