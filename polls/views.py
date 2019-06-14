from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
import time
import requests
import zipcodes

def get_avg_temperature(request):
    sum, count, latitude, longitude = 0, 0, 0, 0 # global sum and count for calculating avg  

    # Validate lat/lon value with Google Maps API
    #Google Map API_key 
    gmKey = 'AIzaSyBppiO9jO5ZvtF9EzNPZh4OEr_wmfaTS1s'
    
    #Google Map API url
    gmUrl = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    # Set response content-type as json
    headers = {'content-type': 'application/json'}
    
    try:
        #check if zipcode was provided
        #if yes, then get latitude and longitude from zipcode
        if('zipcode' in request.GET):
            zipcode = request.GET.get('zipcode')
            
            #check if zipcode is real or not
            #if not throw error
            if(not zipcodes.is_real(zipcode)):
                data = build_error('Invalid Zipcode Provided')
                return HttpResponse(json.dumps(data), headers,status=400)

            #retrieve latitude and longitude values
            zipcode_data = zipcodes.matching(zipcode)
            
            #append query parameters zipcode and api key 
            gmZipcodeUrl = gmUrl+'?address=' +zipcode+'&key='+gmKey

            #connect to Google Maps url and get json response
            api_response_dict = requests.get(url = gmZipcodeUrl).json()
        
            latitude, longitude = float(api_response_dict['results'][0]['geometry']['location']['lat']), float(api_response_dict['results'][0]['geometry']['location']['lat']) 
         

        #else just retrieve longitude and latitude value from the request params
        else:
            # latitude, longitude = float(request.GET.get('latitude')), float(request.GET.get('longitude'))
            latitude, longitude = request.GET.get('latitude'), request.GET.get('longitude')

            #append query parameters lat and lon to url 
            gmValidationUrl = gmUrl+'?latlng=' +str(latitude)+','+str(longitude)+'&key='+gmKey
        
            #connect to Google Maps url and get json response
            is_valid_latlon = requests.get(url = gmValidationUrl).json()

            # if error message in response, then throw error for invalid lat/long values
            if 'error_message' in json.dumps(is_valid_latlon):
                data = build_error('Latitude and Longitude params should be valid float values')
                return HttpResponse(json.dumps(data), headers, status=400)

    
    # if zipcodes is not fully 4 digit code, throw ValueError Exception        
    except ValueError:
        data = build_error('Invalid Zipcode Provided')
        return HttpResponse(json.dumps(data), headers, status=400)

    #throw general exception message for any other error        
    except:
        data = build_error('Latitude and Longitude params should be valid float values')
        return HttpResponse(json.dumps(data), headers, status=400)

    

    # Get list of filters from query params
    filters = request.GET.getlist('filters')

    # check if filters are provided, if not send back error response
    if not filters:
        data = build_error('Please enter valid filters')
        return HttpResponse(json.dumps(data), headers, status=400)
    
    # else iterate over filters and call following flask api service
    else:
        for service in filters:

            #if service is for noaa
            if 'noaa' == service:
                url = 'http://127.0.0.1:5000/noaa?latlon='+str(latitude)+','+str(longitude)
                url_data = get_json(url)
                sum += int(url_data['today']['current']['fahrenheit'])
                count += 1

            #if service is for accuweather    
            elif 'accuweather' == service:
                url = 'http://127.0.0.1:5000/accuweather?latitude='+str(latitude)+'&longitude='+str(longitude)
                url_data = get_json(url)
                sum += int(url_data['simpleforecast']['forecastday'][0]['current']['fahrenheit'])
                count += 1 

            #if service is for weather.com    
            elif 'weather.com' == service:
                url = 'http://127.0.0.1:5000/weatherdotcom'
                params = json.dumps({"lat" : latitude, "lon" : longitude})
                headers = {'content-type': 'application/json'}
                url_data = post_json(url,params,headers)
                sum += int(url_data['query']['results']['channel']['condition']['temp'])
                count += 1   

    # if count is 0, then no valid filters were provided that match our flask service
    if count == 0:
        data = build_error('Please send valid filters')
        return HttpResponse(json.dumps(data), headers, status=400)

    # else calculate avg of total temperature calculated    
    else:
        data = {}
        data['avg_current_temperature'] = float(sum/count)

    
    # send the Httpresponse back
    return HttpResponse(json.dumps(data), headers)
    

def get_json(url):
    data = requests.get(url)
    data = data.json()
    return data    

def post_json(Url,Params, Headers):
    data = requests.post(url = Url, data = Params, headers = Headers)
    data = data.json()
    return data

def build_error(error_message):
    data = {}
    data['error'] = error_message
    return data