## FlightRadar24 Client
One more Python project I'd like to make as a student.

![Website screen](https://media.kasperskydaily.com/wp-content/uploads/sites/90/2015/04/06045541/flightradar-featured-1024x672.jpg)

### Description
This is a autonomous PC client for FR24 service.

### API
This program gets all necessary information from FR24 api endpoint. After that all aircrafts are being painted as 
points and move based on direction and speed info. When needed, the information would be updated in order to refresh 
points' positions.


### Examples
##### Getting all available flights within the specific area
```
from flightradar/api import API
api = API()
for flight in api.get_flights(Area(57.06, 55.00, 32.97, 36.46)):
    print(flight)
```
Will output something like this:
> Flight AFL2155 from DUS to SVO. A320 (VP-BTC) at 55.8338, 33.0941 on altitude 35000. Speed: 442. Track: 103.

> Flight AFL2621 from AGP to SVO. B738 (VP-BGG) at 55.5042, 34.376 on altitude 34475. Speed: 438. Track: 81.

> Flight VAS816 from VKO to MUC. B734 (VQ-BVF) at 56.1504, 35.1726 on altitude 30450. Speed: 437. Track: 280.

> Flight UTA359 from VKO to LED. B735 (VQ-BJL) at 56.5925, 35.3859 on altitude 31975. Speed: 415. Track: 318.

> Flight AFL032 from SVO to LED. A320 (VP-BWE) at 56.6596, 35.5538 on altitude 26875. Speed: 424. Track: 314.

Which is a text description of all available flights. List of all flight fields:

| Name | Description |
| ---- | ----------- |
| id | Flight's unique ID within FR24 |
| mode_s | Aircraft Mode-S code |
| lat | Aircraft latitude |
| lon | Aircraft longitude |
| track | Aircraft direction in degrees |
| alt | Aircraft altitude in kilometers |
| speed | Aircraft speed in kilometers per hour |
| squawk | Aircraft squawk code |
| radar | Current control tower code |
| model | Aircraft model |
| registration | Aircraft registration |
| origin | Flight origin code |
| destination | Flight destination code |
| iata | Flight code in IATA format |
| icao | Flight code in ICAO format |
| vertical_speed | Aircraft vertical speed |
| airline | Airline code |

----------
##### Getting information about the specific flight
```
from flightradar/api import API
api = API()
print(api.get_flight('1d70550f'))
```
Will output something like this:
> Flight AFL2639 from Barcelona El Prat Airport to Moscow Sheremetyevo International Airport, B738 (VP-BCD).

Which is a brief description of the specified flight. List of all flight fields:

| Name | Description |
| ---- | ----------- |
| id | Flight's unique ID within FR24 |
| flight | Flight code in ICAO format |
| status | Flight text status |
| model | Aircraft model |
| registration | Aircraft registration |
| origin | Flight origin code |
| destination | Flight destination code |
| airline | Airline name |
| trail | List of all flight waypoints with latitude, longitude, speed and track |


### Requirements
* Python3.6

### Author
Alexandr Bagirov