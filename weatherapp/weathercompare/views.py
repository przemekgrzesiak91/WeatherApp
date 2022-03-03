from django.shortcuts import render
from bs4 import BeautifulSoup
from requests import get
import re

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def index(request):
    data = []
    city = "Warszawa"
    context = {"data": data}

    if request.method == "POST":
        city = request.POST['city']

    data.append(('<span style="color: rgb(66, 164, 245)">'+city+'</span>', 'Temperatura', 'Zachmurzenie', 'Ciśnienie', 'Wiatr'))

    #search urls
    query = "pogoda " + city

    for url in search(query, tld="co.in", num=10, stop=10, pause=2):
        if 'onet' in url:
            URL_onet = url
        elif 'interia' in url and 'szczegolowa' in url:
            URL_interia = url
        elif 'wp' in url:
            URL_wp = url

    # onet
    data.append(scrap_onet(URL_onet))
    # interia
    data.append(scrap_interia(URL_interia))
    # wp
    data.append(scrap_wp(URL_wp))

    return render(request, "index.html", context)

def scrap_onet(URL):
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('div', class_='mainBox widgetLeftCol'):
        temp_onet = main.find('div', class_='temp').get_text()[:-1]
        cloud_onet = main.find('div', class_='forecastDesc').get_text()
        for span in main.find_all('span', class_='restParamValue'):
            if 'km/h' in span.get_text():
                wind_onet = span.get_text()
            if 'hPa' in span.get_text():
                press_onet = span.get_text()
    return ('Onet', temp_onet + '°C', cloud_onet, press_onet, wind_onet)

def scrap_wp(URL):
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('table', class_='table'):
        temp_wp = main.find('span', class_='temp').get_text()
        cloud_wp = main.find('small').get_text()
        for small in main.find_all('small'):
            if 'km/h' in small.get_text():
                wind_wp = small.get_text().split(' ')[1] + ' km/h'
            if 'hPa' in small.get_text():
                press_wp = small.get_text().split(' ')[1] + ' hPa'
    return ('WP', temp_wp + '°C', cloud_wp, press_wp, wind_wp)

def scrap_interia(URL):
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('div', class_='weather-currently-middle-today'):
        temp_interia = main.find('div', class_='weather-currently-temp-strict').get_text()[:-2]
        cloud_interia = main.find('li', class_='weather-currently-icon-description').get_text().strip()
        for span in main.find_all('span', class_='weather-currently-details-value'):
            if 'km/h' in span.get_text():
                wind_interia = re.sub(' +', ' ', span.get_text())
            if 'hPa' in span.get_text():
                press_interia = re.sub(' +', ' ', span.get_text())

    return ('Interia', temp_interia+'°C', cloud_interia, press_interia, wind_interia)
