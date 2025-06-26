print('hello world')
from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

areas: list =[]
clients:list=[]
workers:list=[]
data_areas=[]
data_workers=[]
data_clients=[]
area_markers = []

class Areas:
    def __init__(self, area_name, area_location):
        self.area_name = area_name
        self.area_location = area_location

    def get_coordinates(self) -> list:
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.area_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd podczas pobierania współrzędnych: {e}")
            return [0.0, 0.0]
