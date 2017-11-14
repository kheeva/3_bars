from decimal import Decimal, InvalidOperation
import json
import geopy.distance


filepath = 'bars.json'


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf8') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError as error:
        print(error)
    except json.JSONDecodeError as error:
        print(error)
    else:
        return json_data
    return {}

# I wanted to do all of parsing job in one cycle.
def parse_json_data(json_data, user_latitude, user_longitude):
    bars_data = []
    for json_bar in json_data['features']:
        bars_data.append([
            json_bar['properties']['Attributes']['Name'],
            json_bar['properties']['Attributes']['SeatsCount'],
            round(geopy.distance.vincenty((user_latitude, user_longitude), json_bar['geometry']['coordinates']).km, 3),])
    return sorted(bars_data, key=lambda x: x[1])


def get_biggest_bar(parsed_bars_data):
    max_seats = parsed_bars_data[-1][1]
    # seeking for the longest name of bars with max Seatscount
    list_of_biggest_bars = filter(lambda x: x[1] == max_seats, parsed_bars_data)
    return max(list_of_biggest_bars, key=lambda x: x[0])


def get_smallest_bar(parsed_bars_data):
    min_seats = parsed_bars_data[0][1]
    # seeking for the lowest name of bars with min Seatscount
    list_of_lowest_bars = filter(lambda x: x[1] == min_seats, parsed_bars_data)
    return min(list_of_lowest_bars, key=lambda x: x[0])


def get_closest_bar(parsed_bars_data):
    return min(parsed_bars_data, key=lambda x: x[2])


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
    bars_json_data = load_data(filepath)
    if not bars_json_data:
        print('No data!')
        exit(1)

    print('Input your latitude:')
    user_latitude = input_coordinate()
    print('Input your longitude:')
    user_longitude = input_coordinate()

    parsed_bars_data = parse_json_data(bars_json_data, user_latitude, user_longitude)
    closest_bar = get_closest_bar(parsed_bars_data)
    biggest_bar = get_biggest_bar(parsed_bars_data)
    smallest_bar = get_smallest_bar(parsed_bars_data)

    print('The closest bar is ', closest_bar[0], '. It is in ', closest_bar[2], ' kilometers.', sep='')
    print('The biggest bar is ', '"', biggest_bar[0], '. It has ', biggest_bar[1], ' seats".', sep='')
    print('The smallest bar is ', '"', smallest_bar[0], '. It has ', smallest_bar[1], ' seats".', sep='')


if __name__ == '__main__':
    main()
