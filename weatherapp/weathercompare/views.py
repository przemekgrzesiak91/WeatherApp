#from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests import get

def index(request):
    # fix for temp below 0°C
    # add links from google search
    result = []
    # onet
    URL = 'https://pogoda.onet.pl/prognoza-pogody/kepno-300790'
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('div', class_='mainBox widgetLeftCol'):
        temp_onet = main.find('div', class_='temp').get_text()[:-1]
        result.append('Onet - ' + temp_onet + '°C</br>')

    # interia
    URL = 'https://pogoda.interia.pl/prognoza-dlugoterminowa-kepno,cId,13329'
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('div', class_='weather-currently-middle-today'):
        temp_interia = main.find('div', class_='weather-currently-temp-strict').get_text()[:-2]
        result.append('Interia - ' + temp_interia + '°C</br>')

    # wp
    URL = 'https://pogoda.wp.pl/pogoda-dlugoterminowa/kepno/3096338'
    page = get(URL)

    bs = BeautifulSoup(page.content, features="html.parser")

    for main in bs.find_all('td', class_='main'):
        temp_wp = main.find('span', class_='temp').get_text()
        result.append('WP - ' + temp_wp + '°C </br>')

    avg_temp = (int(temp_wp) + int(temp_onet) + int(temp_interia)) / 3
    result.append('Average - ' + str(round(avg_temp, 2)) + '°C\n')

    return render(request, "index.html")
    #return HttpResponse(result)