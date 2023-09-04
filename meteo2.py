import requests

import datetime as dt

import json

import sys

from os.path import dirname, join, getmtime,exists

class WeatherForecast():
    def date(self):
        print("Input a date 'YYYY-MM-DD' in order to check precipitation: ")
        date_input = input("Input 'ok' if you want to check the today forecast or 'select' if you want to check a date: ")
        if date_input == 'ok':
            date = dt.date.today() + dt.timedelta(1)
            date_format = date.strftime('%Y-%m-%d')
            print(f"Checking for tomorrow date: {date_format}")
            return date_format
        elif not date_input:
            sys.exit()
        #if date input == select:
        else:
            try:
                date_input = dt.datetime.strptime(date_input, '%Y-%m-%d' )
                date_format = date_input.strftime ('%Y-%m-%d')
                return date_format
            except ValueError:
                print("invalid date input")
                sys.exit()

    def weather(self, search_date):
        latitude, longitude = 51.5085, 0.1257
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}'
        response = requests.get(url)
        return response.text
    
    def weather_cached(self, search_date):
        use_cache = True
        file_path = join('cache', search_date)
        if not exists(file_path):
            use_cache = False
        elif dt.datetime.fromtimestamp(getmtime(file_path)) < dt.datetime.now() - dt.timedelta(hours=24):
            use_cache = False
        if use_cache:
            print("Cache used")
            with open(file_path) as file:
                precipitation = json.load(file)
                precipitation_sum = float(precipitation["daily"]["precipitation_sum"][0])
                return precipitation_sum

        weather_txt = self.weather(search_date)

        with open (file_path, 'w') as file:
            file.write(weather_txt)
            print("Done")
            precipitation = json.loads(search_date)
            precipitation_sum = float(precipitation["daily"]["precipitation_sum"][0])
            return precipitation_sum
        
    def __getitem__(self, item):
        try:

            return self.weather_cached(item)
        
        except KeyError:

            return None
        
    def __setitem__(self, key, value):
        pass

wf = WeatherForecast()

print(wf['2023-09-05'])

#for file in listdir('cache'):
    #print(file)






