import pandas as pd
import requests
import os
from services.graph_metadata import WeatherGraphMetadata
# from graph_metadata import WeatherGraphMetadata

TEST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'testing')

def get_lat_lon(city_name):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'weather-app'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        raise ValueError("City not found")

def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    headers = {"User-Agent": "weather-app"}
    
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    address = data.get("address", {})
    city = (address.get("city") or
            address.get("town") or
            address.get("village") or
            address.get("hamlet"))
    state = address.get("state")
    country = address.get("country")
    
    return city, state, country

def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,weathercode,precipitation"
        "&forecast_days=4&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    return_df = pd.DataFrame(data['hourly'])
    return return_df

def construct_weather_dataframe(city_name):
    lat, lon = get_lat_lon(city_name)
    print(lat, lon)
    city, state, country = reverse_geocode(lat, lon)
    print(city, state, country)
    weather_data = get_weather(lat, lon)
    print('got weather data')
    # title_map = {
    #     "temperature_2m": "Temperature (°C)",
    #     "apparent_temperature": "Feels Like (°C)",
    #     "relative_humidity_2m": "Relative Humidity (%)",
    #     "precipitation": "Precipitation (mm)"
    # }
    # weather_data = weather_data.rename(columns=title_map)
    metadata = WeatherGraphMetadata(
        title = f'{city}, {state} - {country}',
        x_axis = 'time',
        y_axis = 'temperature_2m',
        num_points = 24
    )
    return weather_data, metadata

if __name__ == "__main__":
    city = "Berkeley"
    weather_data, metadata = construct_weather_dataframe(city)


