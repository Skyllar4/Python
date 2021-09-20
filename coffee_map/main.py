import json
import requests
import folium
import os
from flask import Flask
from geopy.distance import lonlat, distance

user_address = input("Введите свой адрес ")
apikey = os.environ["API"]
new_coffee_list = []
vis1 = json.loads(
    requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/vis1.json"
    ).text)

with open("coffee.json", "r", encoding="CP1251") as my_file:
    file_contents = my_file.read()
coffee_list = json.loads(file_contents)


def nearest_coffee_shop_find(new_coffee_list):
    return new_coffee_list['distance']


def marks_on_map(quantity):
    for index in range(quantity):
        folium.Marker(
            location=[
                coffee_by_5[index]['latitude'], coffee_by_5[index]['longitude']
            ],
            popup=folium.Popup(max_width=450).add_child(
                folium.Vega(vis1, width=450, height=250)),
        ).add_to(user_on_map)


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url,
                            params={
                                "geocode": address,
                                "apikey": apikey,
                                "format": "json",
                            })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


user_coordinates = fetch_coordinates(apikey, user_address)
user_coordinates_transform = list(user_coordinates)
user_coordinates_transform.reverse()

user_on_map = folium.Map(location=user_coordinates_transform, zoom_start=13)

for coffee_shops in coffee_list:
    coffee_coord = coffee_shops['geoData']['coordinates']
    new_list_element = {
        'title': coffee_shops['Name'],
        'distance': distance(lonlat(*user_coordinates),
                             lonlat(*coffee_coord)).km,
        'latitude': coffee_shops['geoData']['coordinates'][1],
        'longitude': coffee_shops['geoData']['coordinates'][0]
    }
    new_coffee_list.append(new_list_element)

coffee_by = sorted(new_coffee_list, key=nearest_coffee_shop_find)
coffee_by_5 = coffee_by[:5]


def generate_map():
    with open('index.html') as file:
        return file.read()


def main():

    marks_on_map(5)
    user_on_map.save("index.html")

    app = Flask(__name__)
    app.add_url_rule('/', 'hello', generate_map)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
