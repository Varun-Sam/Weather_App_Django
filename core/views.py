from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

# Create your views here.

def get_html_content(city):
    # these are used to bypass google to chrome or mozilla
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    #to replace empty space with + sign
    city = city.replace(" ", "+")
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content

def home(request):
    #to start with empty string
    weather_data = None
    if 'city' in request.GET:
        # next step fetch data
        city = request.GET.get('city')
        html_content = get_html_content(city)
        # print(html_content)
        # beautiful soup is used to render data from google
        soup = BeautifulSoup(html_content, 'html.parser')
        # a dictionary to store all weather info to display in html
        weather_data = dict()
        weather_data['region'] = soup.find('div', attrs={'id':'wob_loc'}).text
        weather_data['daytime'] = soup.find('div', attrs={'id':'wob_dts'}).text
        weather_data['status'] = soup.find('span', attrs={'id':'wob_dc'}).text
        weather_data['temperature'] = soup.find('span', attrs={'id':'wob_tm'}).text
        # print(temperature)
        # print(status)
        # print(daytime)
        # print(region)
        pass



    return render(request, 'core/home.html',{'weather' : weather_data})
