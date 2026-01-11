import requests
from bs4 import BeautifulSoup

class Jednostki:
    def __init__(self, name: str, city: str, street: str, map_widget=None, marker_icon=None):
        self.name = name
        self.city = city
        self.street = street
        self.coords = self.get_coordinates()
        if self.coords and map_widget and marker_icon:
            self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name, icon=marker_icon,
                                                text_color="#ff8c00")
        else:
            self.marker = None

    def get_coordinates(self):
        url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude_elements = response_html.select('.latitude')
        longitude_elements = response_html.select('.longitude')

        if len(latitude_elements) < 2 or len(longitude_elements) < 2:
            print(f"Ostrzeżenie: Nie znaleziono współrzędnych dla {self.city}")
            return None

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

class Pracownicy:
    def __init__(self, name: str, surname: str, city: str, map_widget=None, marker_icon=None):
        self.name = name
        self.surname = surname
        self.city = city
        self.coords = self.get_coordinates()
        if self.coords and map_widget and marker_icon:
            self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name, icon=marker_icon,
                                                text_color="#4169e1")
        else:
            self.marker = None

    def get_coordinates(self):
        url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude_elements = response_html.select('.latitude')
        longitude_elements = response_html.select('.longitude')

        if len(latitude_elements) < 2 or len(longitude_elements) < 2:
            print(f"Ostrzeżenie: Nie znaleziono współrzędnych dla {self.city}")
            return None

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]


class Incydenty:
    def __init__(self, name: str, place: str, map_widget=None, marker_icon=None):
        self.name = name
        self.place = place
        self.coords = self.get_coordinates()
        if self.coords and map_widget and marker_icon:
            self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name, icon=marker_icon,
                                                text_color="#8a2be2")
        else:
            self.marker = None

    def get_coordinates(self):
        url: str = f'https://pl.wikipedia.org/wiki/{self.place}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude_elements = response_html.select('.latitude')
        longitude_elements = response_html.select('.longitude')

        if len(latitude_elements) < 2 or len(longitude_elements) < 2:
            print(f"Ostrzeżenie: Nie znaleziono współrzędnych dla {self.place}")
            return None

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]