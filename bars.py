import sys
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
    return min(bars['features'], key=lambda x: round(geopy.distance.vincenty(
        (latitude, longitude), x['geometry']['coordinates']).km, 3))


def is_valid_coordinate(coordinate):
    try:
        float(coordinate)
    except ValueError:
        return False
    else:
        return True


def get_user_coordinate(coordinate):
    return is_valid_coordinate(coordinate)and float(coordinate) or (
        get_user_coordinate(input('Wrong format. Try again:')))


def get_bar_name(bar):
    return bar['properties']['Attributes']['Name']


def get_bar_seats_number(bar):
    return bar['properties']['Attributes']['SeatsCount']


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

        print('\nThe closest bar is "', get_bar_name(closest_bar), '".', sep='')

        print('The biggest bar is "', get_bar_name(biggest_bar), '". It has ',
              get_bar_seats_number(biggest_bar), ' seats.', sep='')

        print('The smallest bar is "', get_bar_name(smallest_bar), '". It has ',
              get_bar_seats_number(smallest_bar), ' seats.', sep='')


if __name__ == '__main__':
    main()
