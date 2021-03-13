import googlemaps
import json
import pprint
import time

# Define the API Key.
API_KEY = 'AIzaSyBSH21aLNUkkW2I0eOu1tR8YA0JkdJkzWk'

# Define the Client
gmaps = googlemaps.Client(key = API_KEY)


places_result  = gmaps.places_nearby(location='8.7600805,-75.8812715', radius = 40000, open_now =False , type = 'hotels')

time.sleep(3)

places_result  = gmaps.places_nearby(page_token = places_result['next_page_token'])

store_result = []

for place in places_result['results']:
    my_place_id = place['place_id']
    my_fields = ['name']
    places_details  = gmaps.place(place_id= my_place_id , fields= my_fields)
    print(places_details)