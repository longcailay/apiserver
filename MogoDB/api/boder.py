import requests
import flask
import pandas as pd
import json
import difflib
from flask import request, jsonify, make_response, Blueprint




def locationToDistrict(lat, lon):
    URL = "https://nominatim.openstreetmap.org/reverse?format=json&lat=" + lat + "&lon=" + lon  + "&zoom=18&addressdetails=1"
    print(URL)
    # sending get request and saving the response as response object 
    res = requests.get(url = URL)
    # extracting data in json format 
    data = res.json()
    address = 'Not Found!'
    district = 'Undefined'
    if 'address' in data:
        address = data['address']
        if 'neighbourhood' in address:
            district = address['neighbourhood']
        else:
            if 'suburb' in address:
                district = address['suburb']
    print("OpenStreetMap bổ sung phường/xã:  " + str(district))
    return district

print(locationToDistrict(str(10.042770274726003), str(105.75097055588688)))