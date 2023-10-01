#Use the forecast API to create a detailed, neatly formatted 5-day forecast, for anywhere the user chooses. 
#Ask the user for the location.
#Make sure your API key is not coded into your program. 
#Your program should read the key from an environment variable. 
#Use a query parameter dictionary in the request.
#Your forecast should show the temperature and unit (your choice of F or C), 
#weather description, and wind speed for every three hour interval, over the next 5 days.
#Your program should handle errors. What type of errors do you anticipate? How will you deal with them?

import requests
import os
import logging
from datetime import datetime

# https://docs.python.org/3/library/locale.html

# Configure your logger. filename - where to write to. otherwise logs write to the console
# level is the minimum log level that is recorded. DEBUG means log everything. 
# format sets the format of the string that is recorder for each log event. See docs for example format strings. 
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')


key = os.environ.get('WEATHER_KEY')

url = 'http://api.openweathermap.org/data/2.5/forecast'

def main():
    location = get_location()
    forecast_data, error = get_forecast_data(location, key)
    if error:
        print('Sorry, could not get weather.')
    else:
        forecasts_list = forecast_data['list']
        display_5_day_forecast(forecasts_list)


def get_location():
    city, country = '', ''
    while len(city) == 0 or not city.isalpha():
        city = input('Enter the name of the city: ').strip().lower()

    while len(country) !=2 or not country.isalpha():
        country = input('Enter the 2-letter country code: ').strip().lower()

    location = f'{city},{country}'
    return location

def get_forecast_data(location, key):
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key,}
        response = requests.get(url, params=query)
        response.raise_for_status() # raise exception for 400 or 500 errors
        data = response.json() # this may error too if response is not JSON
        return data, None
    except Exception as ex:
        logging.exception(ex)
        logging.exception(response.text)
        return None, ex

def display_5_day_forecast(forecasts_list):
    try:
        print('\nHere is your weather forecast for the next 5 days in 3 hour intervals:\n')
        print(f'{"Time":<24}{"Temperature":>16}{"Weather":>18}{"Winds":>20}\n')
        for forecast in forecasts_list:
            temp = forecast['main']['temp']
            timestamp = forecast['dt']
            forecast_date = datetime.fromtimestamp(timestamp) # time will be converted to minnesota CDT, this is so the user can easily read it vs looking at unix time. 
            weather = forecast['weather'][0]['description']
            wind = forecast['wind']['speed']
            print(f'{forecast_date} CDT{temp:>11}F{weather:>29}{wind:>12} MPH')
    except KeyError as e:
        logging.exception(e)


if __name__ == '__main__':
    main()
