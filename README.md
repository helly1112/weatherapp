# Django Weather Application

## Background

* This weather application is built on Django web framework and connects to flask application for fetching weather-related data based on Zipcode/Latitude-Longitude and Filters given. Application covers all the boundary conditions and validation for each set of inputs. In case of validation error, Http Response with code 400 and json object will be thrown. Also, application connects with google map api to validate input latitude and longitude. In case if zipcode is given, then application uses Google Maps API to validate and fetch required latitude-longitude values. 

## Routes

* http://127.0.0.1:8080/polls/current_temperature/

### Inputs (Query Parameters)

* zipcode (required if latitude and longitude are not given)
* latitude (required if zipcode is not given)
* longitude (required if zipcode is not given)
* filters (list of weather web services) (accuweather, noaa, weather.com)

## Requirements

* Python (tested on V3.7.2)
* Django (tested on V2.2)
* Flask (https://github.com/shipwell/mock-weather-api) application running on port 5000.
* Google Map API Key (Please generate API key and input in `gmKey` variable in polls/views.py file)

## Setup

1) Make sure Flask (https://github.com/shipwell/mock-weather-api) application is running on port 5000.
2) Run following command to run weather application

    ```
    git clone https://github.com/helly1112/weatherapp
    cd weatherapp
    python manage.py runserver 8080
    ```

## Usage

### Example of different endpoints and its response

#### Endpoint : http://127.0.0.1:8080/polls/current_temperature/?zipcode=60626&filters=weather.com&filters=noaa&filters=accuweather
```
{"avg_current_temperature": 49.0}
```

#### Endpoint : http://127.0.0.1:8080/polls/current_temperature/?latitude=29.34&longitude=10.0&filters=weather.com&filters=noaa
```
{"avg_current_temperature": 46.0}
```

#### Endpoint : http://127.0.0.1:8080/polls/current_temperature/?zipcode=60626as&filters=weather.com&filters=noaa
```
{"error": "Invalid Zipcode Provided"}
```

#### Endpoint : http://127.0.0.1:8080/polls/current_temperature/?latitude=10000000000&longitude=10.0&filters=weather.com&filters=noaa&filters=accuweather
```
{"error": "Latitude and Longitude params should be valid float values"}
```

#### Endpoint : http://127.0.0.1:8080/polls/current_temperature/?latitude=29.34&longitude=10.0
```
{"error": "Please enter valid filters"}
```


## Resources 

- https://docs.djangoproject.com/en/2.2/
- https://developers.google.com/maps/documentation/
- https://pypi.org/project/zipcodes/
- https://2.python-requests.org/en/master/



