from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
import requests
from pprint import pprint

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('path\\firebase-adminsdk.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'firebase id'
})

#--------------------------------------------------------------------------------------------------------------------

#Geofencing methods

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    print('Haversine result: ', c * r)
    return c * r

#--------------------------------------------------------------------------------------------------------------------

#Weather methods

def weather_data(lat,lon):
    # lat=str(lat)
    # lon=str(lon)
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lon+'&appid=api_key&units=metric')
    return res.json()

def print_weather(result):
    weather_list = [result['main']['temp'], result['weather'][0]['main']]
    return weather_list


#-------------------------------------------------------------------------------------------------------------------------

#GEOFENCING

#Input Values latitude and longitude
#Retrieve values from firebase

center = input('Enter center latitude and longitude: ')
test = input('Enter test latitude and longitude: ')
c = center.split(' ')
t = test.split(' ')
center_point = [{'lat': Decimal(c[0]), 'lng': Decimal(c[1])}]
test_point = [{'lat': Decimal(t[0]), 'lng': Decimal(t[1])}]

lat1 = center_point[0]['lat']
lon1 = center_point[0]['lng']
lat2 = test_point[0]['lat']
lon2 = test_point[0]['lng']

radius = 1.0 # in kilometer
a = haversine(lon1, lat1, lon2, lat2) #Return value from haversine function

print('Distance (KM) : ', a, 'KM')
if a > radius and a < radius + 0.200:
    status = 'Geofence in 200 metres'
    print('Geofence within 200 metres')
if a <= radius:
    status = 'Inside Geofence'
    print('Inside the area')
    #Send alert to firestore of geofence
else:
    status = 'Outside Geofence'
    print('Outside the area')
    #Send alert to firestore of geofence


#-------------------------------------------------------------------------------------------------------------------------

#WEATHER

w_data=weather_data(t[0], t[1])
weather_dict_list = print_weather(w_data)

#-------------------------------------------------------------------------------------------------------------------------


#Push data to Firebase

ref = db.reference('server')

users_ref = ref.child('users')

users_ref.child('user1').set({
    'date_of_birth': 'December 24, 1978',
    'full_name': 'Mike Dean',
    'age': '34',
    'car_model': 'Pagani Zonda',
    'lisence_number': 'EJHGD456SD',
    'current_latitude': t[0],
    'current_longitude': t[1],
    'geofence_status': status,
    'temperature': weather_dict_list[0],
    'weather_condition': weather_dict_list[1]
})

users_ref.child('user2').set({
    'date_of_birth': 'December 24, 1978',
    'full_name': 'Mike Dean',
    'age': '34',
    'car_model': 'Pagani Zonda',
    'lisence_number': 'EJHGD456SD',
    'current_latitude': t[0],
    'current_longitude': t[1],
    'geofence_status': status,
    'temperature': weather_dict_list[0],
    'weather_condition': weather_dict_list[1]
})
