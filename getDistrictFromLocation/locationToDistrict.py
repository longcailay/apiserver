#File này truyền vào tọa độ, sẽ cho ra xã/phường tại tọa độ đó
import requests

def locationToDistrict(lat, lon):
    URL = "https://nominatim.openstreetmap.org/reverse?format=json&lat=10.78790855&lon=106.63598633&zoom=18&addressdetails=1"
    # sending get request and saving the response as response object 
    res = requests.get(url = URL)
    # extracting data in json format 
    data = res.json()
    district = data['address']['neighbourhood']
    return district

# printing the output 
print(locationToDistrict(10.78790855,106.63598633)) 
