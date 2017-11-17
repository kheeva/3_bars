import sys
from decimal import Decimal, InvalidOperation
import json
import geopy.distance


def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf8') as json_file:
        loaded_data = json.load(json_file)
    return loaded_data


def get_biggest_bar(bars):
    return max(bars['features'],
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars['features'],
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, latitude, longitude):
    return min(bars['features'], key=lambda x: Decimal(geopy.distance.vincenty(
                                (latitude, longitude),
                                x['geometry']['coordinates']).km))


def is_valid_coordinate(coordinate):
    try:
        Decimal(coordinate)
    except InvalidOperation:
        return False
    else:
        return True


def get_user_coordinate(coordinate):
    return is_valid_coordinate(coordinate)and Decimal(coordinate) or \
          get_user_coordinate(input('Wrong format. Try again:'))


def main():
    if len(sys.argv) != 2:
        exit("Usage: python bars.py path_to_file.")

    try:
        loaded_bars = load_json_data(sys.argv[1])
    except FileNotFoundError as error:
        exit(error)
    except json.JSONDecodeError as error:
        exit(error)
    else:
        user_latitude = get_user_coordinate(input('Input your latitude:'))
        user_longitude = get_user_coordinate(input('Input your longitude:'))

        closest_bar = get_closest_bar(loaded_bars,
                                      user_latitude,
                                      user_longitude)
        biggest_bar = get_biggest_bar(loaded_bars)
        smallest_bar = get_smallest_bar(loaded_bars)

        print('\nThe closest bar is "',
              closest_bar['properties']['Attributes']['Name'], '".', sep='')

        print('The biggest bar is "',
              biggest_bar['properties']['Attributes']['Name'], '". It has ',
              biggest_bar['properties']['Attributes']['SeatsCount'], ' seats.',
              sep='')

        print('The smallest bar is "',
              smallest_bar['properties']['Attributes']['Name'], '". It has ',
              smallest_bar['properties']['Attributes']['SeatsCount'], ' seats.',
              sep='')


if __name__ == '__main__':
    main()
