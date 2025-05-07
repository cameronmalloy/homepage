from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(city="San Francisco"):
    """
    Takes in a string city and searches for the current weather of that city via openweather API
    Gets the weather with 2 types of units: imperial and metric which requires 2 api calls
    """
    url_base = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("OPENWEATHER_API_KEY")}&q={city}&units=' + '{unit}'
    metric_types = ['imperial', 'metric']
    print(url_base)

    weather_data = {}
    for metric_type in metric_types:
        request_url = url_base.format(unit=metric_type)
        print(request_url)
        weather_data[type] = requests.get(request_url).json()
    
    return weather_data

def get_first_geo_loc(city):
    """
    Takes a string input city and outputs the latitude and longitude of that city
    Searches openweather api with a limit of 1 (so just whatever city openweather has first)
    https://openweathermap.org/api/geocoding-api
    """
    request_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={os.getenv("OPENWEATHER_API_KEY")}'
    response = requests.get(request_url).json()
    
    # ensure results
    if len(response) == 0:
        return 'City does not exist'

    city_data = response[0]
    coordinates = {'lat': city_data['lat'], 'lon': city_data['lon']}
    return coordinates

if __name__ == "__main__":
    # print('\n***Get Current Weather Condtions***\n')
    # city = input("\nEnter a city name: ")
    # weather_data = get_current_weather(city)
    # print("\n")
    # pprint(weather_data)
    print(get_first_geo_loc('Berkeley'))