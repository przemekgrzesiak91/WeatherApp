#from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests import get
import re

def index(request):
    # add links from google search
    # add google here

    data = {}
    list = []
    data['list'] = list

    list.append(('Serwis','Temperatura','Zachmurzenie','Ciśnienie', 'Wiatr'))

    # onet
    URL = 'https://pogoda.onet.pl/prognoza-pogody/kepno-300790'
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


    list.append(('Onet', temp_onet + '°C', cloud_onet, press_onet, wind_onet))

    # interia
    URL = 'https://pogoda.interia.pl/prognoza-dlugoterminowa-kepno,cId,13329'
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

    list.append(('Interia', temp_interia+'°C', cloud_interia, press_interia, wind_interia))
    # wp
    URL = 'https://pogoda.wp.pl/pogoda-dlugoterminowa/kepno/3096338'
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
    list.append(('WP', temp_wp + '°C', cloud_wp, press_wp, wind_wp))

    # avg_temp = (int(temp_wp) + int(temp_onet) + int(temp_interia)) / 3
    # list.append(('Average', str(round(avg_temp,2))+'°C'))



    return render(request, "index.html", data)
    #return HttpResponse(result)