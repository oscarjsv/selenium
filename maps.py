import googlemaps
import time

gmaps = googlemaps.Client(key='')

def print_Hotels(searchString, next=''):
    '''Simple google maps scraper (still experimental)'''
    count = 0
    try:
        places_result = gmaps.places(searchString, page_token=next)
    except ex as e:
        print(e)
    else:
        for result in places_result['results']:
            count += 1
            print(result['name'], count)
    time.sleep(2)
    try:
        places_result['next_page_token']
    except KeyError as e:
        print('Complete')
    else:
        print_Hotels(searchString, next=places_result['next_page_token'])


if __name__ == '__main__':
    print_Hotels('hoteles monteria Cordoba')
