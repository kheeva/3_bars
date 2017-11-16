import sys
from decimal import Decimal, InvalidOperation
import json
import geopy.distance


def load_data(file_path):
    error_msg = ''
    try:
        with open(file_path, 'r', encoding='utf8') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError as error:
        error_msg = error
    except json.JSONDecodeError as error:
        error_msg = error
    else:
        return json_data, error_msg
    return {}, error_msg


def get_biggest_bar(bars):
    return max(bars['features'],
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars['features'],
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, latitude, longitude):
    closest_bar = {}
    min_distance_to_bar = 20000

    for bar in bars['features']:
        distance_to_bar = round(geopy.distance.vincenty(
                                    (latitude, longitude),
                                    bar['geometry']['coordinates']).km, 3)
        if distance_to_bar <= min_distance_to_bar:
            min_distance_to_bar = distance_to_bar
            closest_bar = bar

    return closest_bar, min_distance_to_bar


def input_coordinate():
    while True:
        coordinate = input()
        try:
            coordinate = Decimal(coordinate)
        except InvalidOperation:
            print('Wrong format! Correct format is [digits].[digits]')
            print('Try again:')
        else:
            break
    return coordinate


def main():
    if len(sys.argv) != 2:
        exit("Usage: python lang_frequency.py path_to_file.")

    loaded_bars, load_error_msg = load_data(sys.argv[1])
    if not loaded_bars and load_error_msg:
        exit(load_error_msg)

    print('Input your latitude:')
    user_latitude = input_coordinate()
    print('Input your longitude:')
    user_longitude = input_coordinate()

    closest_bar, min_distance_to_bar = get_closest_bar(loaded_bars,
                                                       user_latitude,
                                                       user_longitude)
    biggest_bar = get_biggest_bar(loaded_bars)
    smallest_bar = get_smallest_bar(loaded_bars)

    print('The closest bar is ',
          closest_bar['properties']['Attributes']['Name'],
          '. It is in ', min_distance_to_bar,
          ' kilometers.', sep='')

    print('The biggest bar is "',
          biggest_bar['properties']['Attributes']['Name'],
          '". It has ', biggest_bar['properties']['Attributes']['SeatsCount'],
          ' seats.', sep='')

    print('The smallest bar is "',
          smallest_bar['properties']['Attributes']['Name'],
          '". It has ', smallest_bar['properties']['Attributes']['SeatsCount'],
          ' seats.', sep='')


if __name__ == '__main__':
    main()
