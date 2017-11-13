from decimal import Decimal
import json
import geopy.distance
from decimal import Decimal


filepath = 'bars.json'


def load_data(filepath):
    bars_data = list()
    with open(filepath, 'r', encoding='utf8') as json_file:
        json_data = json.load(json_file)
    for json_bar in json_data['features']:
        bars_data.append([
            json_bar.get('properties')['Attributes']['Name'],
            json_bar.get('properties')['Attributes']['SeatsCount'],
            json_bar.get('geometry')['coordinates'],])
    return sorted(bars_data, key=lambda x: x[1])


def get_biggest_bar(bars_data):
    max_seats = bars_data[-1][1]
    list_of_biggest_bars = filter(lambda x: x[1] == max_seats, bars_data)
    return sorted(list_of_biggest_bars, key=lambda x: x[0])[-1][0]


def get_smallest_bar(bars_data):
    min_seats = bars_data[0][1]
    list_of_lowest_bars = filter(lambda x: x[1] == min_seats, bars_data)
    return sorted(list_of_lowest_bars, key=lambda x: x[0])[0][0]


def get_closest_bar(bars_data, longitude, latitude):
    bars_distances = list()
    for bar in bars_data:
        bars_distances.append(geopy.distance.vincenty((latitude, longitude), bar[2]).km)
    return Decimal(min(bars_distances)).quantize(Decimal('.001'))


def input_coordinate():
    while True:
        coordinate = input()
        try:
            coordinate = Decimal(coordinate)
        except Exception:
            print('Wrong format! Correct format is [digits].[digits]')
            print('Try again:')
        else:
            break
    return coordinate


def main():
    bars_data = load_data(filepath)

    print('Input your latitude:')
    user_latitude = input_coordinate()
    print('Input your longitude:')
    user_longitude = input_coordinate()

    print('The closest bar in ', get_closest_bar(bars_data, user_longitude, user_latitude), ' kilometers.', sep='')
    print('The biggest bar is ', '"', get_biggest_bar(bars_data), '".', sep='')
    print('The lowest bar is ', '"', get_smallest_bar(bars_data), '".', sep='')


if __name__ == '__main__':
    main()
